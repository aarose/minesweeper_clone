#!/usr/bin/python
from pyramid.view import (
    view_config,
    view_defaults,
    )
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from minesweeper.grids import constants as const
from minesweeper.grids import models
from minesweeper.grids.matrices import (
    Matrix,
    MineMatrix,
    bit_flip,
    multiply,
    )
from minesweeper.models_base import DBSession


@view_defaults(route_name='home')
class Home(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer=const.MAIN_TEMPLATE)
    def get(self):
        return {'game': False}

    @view_config(request_method='POST')
    def post(self):
        """ Creates a new Game, MineMap, and PlayerMaps. """
        # Create a MineMap
        mine_matrix = MineMatrix(const.DEFAULT_HEIGHT,
                                 width=const.DEFAULT_WIDTH,
                                 mine_number=const.DEFAULT_MINES)
        mine_map = mine_matrix.to_model()
        DBSession.add(mine_map)
        DBSession.flush()

        # Create a Game and PlayerMaps for it
        game = models.Game(mine_map=mine_map.id)
        game.player_maps = [
            models.PlayerMap(map_type=const.PlayerMapType.CLICK),
            models.PlayerMap(map_type=const.PlayerMapType.FLAG),
        ]
        DBSession.add(game)
        DBSession.flush()
        return HTTPFound(location=self.request.route_url('view_game',
                                                         game_id=game.id))


@view_config(route_name='view_game', request_method='GET',
             renderer=const.MAIN_TEMPLATE)
def view_game(request):
    """ Returns the game. """
    game = get_game_or_none(request)
    if game is None:
        return HTTPNotFound('No such game.')

    # Get the MineMap
    mine_map = DBSession.query(models.MineMap).get(game.mine_map)
    number_of_mines = DBSession.query(models.MineMapData).filter_by(
        mine_map_id=mine_map.id).count()

    # If the game is over, just send over the full map
    if game.state is const.GameState.IN_PROGRESS:
        grid = derive_grid(mine_map, game.id)
    else:
        grid = mine_map.to_matrix()

    response = {
        'game': True,
        'height': mine_map.height,
        'width': mine_map.width,
        'mines': number_of_mines,
        'state': game.state,
        'grid': grid,
    }
    return response


@view_config(route_name='get_flags', request_method='GET', renderer='json')
def get_flags(request):
    game = get_game_or_none(request)
    if game is None:
        return HTTPNotFound('No such game.')

    # Get the FlagMap
    flag_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game.id, map_type=const.PlayerMapType.FLAG).first()
    # Each entry is either a flag, or a question
    flag_entries = DBSession.query(models.PlayerMapData).filter_by(
        player_map_id=flag_map.id, value=const.PlayerMapDataValue.FLAG).all()
    unsure_entries = DBSession.query(models.PlayerMapData).filter_by(
        player_map_id=flag_map.id, value=const.PlayerMapDataValue.UNSURE).all()

    flags = [[flag.row_num, flag.col_num] for flag in flag_entries]
    unsures = [[unsure.row_num, unsure.col_num] for unsure in unsure_entries]
    return {'flags': flags, 'unsures': unsures}


@view_config(route_name='cell_get', request_method='POST', renderer='json')
def update_cell(request):
    """ Executes the provided action upon the cell, returns the state. """
    game = get_game_or_none(request)
    if game is None:
        return HTTPNotFound('No such game.')

    # If the game is not in progress (won or lost) then no action is allowed
    if game.state != const.GameState.IN_PROGRESS:
        return HTTPForbidden('The game is over.')

    try:
        x = int(request.matchdict['x'])
        y = int(request.matchdict['y'])
    except ValueError:
        return HTTPBadRequest('Cell parameters must be integers')

    # If there's a ClickMapData entry, the cell has already been clicked
    # It cannot be updated, so no further action is allowed
    click_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game.id, map_type=const.PlayerMapType.CLICK).first()
    click_data = DBSession.query(models.PlayerMapData).filter_by(
        player_map_id=click_map.id, row_num=x, col_num=y).first()
    if click_data:
        return HTTPForbidden('The cell has alread been revealed.')

    # Validate action
    try:
        action = int(request.POST.get('action'))
    except ValueError:
        return HTTPBadRequest('Action must be an integer')
    if action not in const.Action.choices():
        return HTTPBadRequest('That action is incorrect.')

    value = None
    reveal = []
    if action is const.Action.LEFT_CLICK:
        value, reveal, game = left_click(x, y, click_map, game)
    elif action is const.Action.RIGHT_CLICK:
        value, game = right_click(x, y, game)

    return {'state': game.state, 'value': value, 'reveal': reveal}


def get_game_or_none(request):
    game_id = int(request.matchdict['game_id'])
    game = DBSession.query(models.Game).get(game_id)
    return game


def derive_grid(mine_map, game_id):
    """ Returns the derived grid (mine matrix * click matrix) """
    mine_matrix = mine_map.to_matrix()
    click_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game_id, map_type=const.PlayerMapType.CLICK).first()
    click_matrix = click_map.to_matrix()  # Acts as a mask
    return multiply(mine_matrix, click_matrix)


def derive_win_matrix(game):
    mine_map = DBSession.query(models.MineMap).get(game.mine_map)
    mine_matrix = mine_map.to_matrix()
    mask = Matrix(mine_matrix.height, width=mine_matrix.width, init_value=0.1)
    return bit_flip(multiply(mine_matrix, mask))


def get_cell_mine_map_value(x, y, game):
    mine_map = DBSession.query(models.MineMap).get(game.mine_map)
    mine_matrix = mine_map.to_matrix()
    return mine_matrix[x][y]


def left_click(x, y, click_map, game):
    reveal = []

    # Record a successful click on the Click Map
    recorded_click = models.PlayerMapData(
        player_map_id=click_map.id, row_num=x, col_num=y,
        value=const.PlayerMapDataValue.CLICKED)
    DBSession.add(recorded_click)

    mine_map = DBSession.query(models.MineMap).get(game.mine_map)
    mine_matrix = mine_map.to_matrix()
    value = mine_matrix[x][y]

    # If the cell contains a mine, game over
    if value is const.MineMapDataValue.MINE:
        # Update game state
        game.state = const.GameState.LOSE
        DBSession.add(game)
        DBSession.flush()
        return (value, reveal, game)

    # If a blank space got revealed, time for a cascade reveal
    if value is const.MineMapDataValue.CLUE[0]:
        reveal = cascade_reveal(x, y, mine_map)
    DBSession.flush()

    # Compare the Click matrix to the Win matrix. If the same, the game is won
    click_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game.id, map_type=const.PlayerMapType.CLICK).first()
    click_matrix = click_map.to_matrix()
    win_matrix = derive_win_matrix(game)
    if click_matrix == win_matrix:
        # Update game state
        game.state = const.GameState.WIN
        DBSession.add(game)
        DBSession.flush()
    return (value, reveal, game)


def right_click(x, y, game):
    """ Set/increment/clear the flag in this cell. """
    flag_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game.id, map_type=const.PlayerMapType.FLAG).first()

    # Get the FlagMapData, if it exists
    flag_data = DBSession.query(models.PlayerMapData).filter_by(
        player_map_id=flag_map.id, row_num=x, col_num=y).first()

    if flag_data is None:
        # UNCLICKED --> FLAG
        recorded_flag = models.PlayerMapData(
            player_map_id=flag_map.id, row_num=x, col_num=y,
            value=const.PlayerMapDataValue.FLAG)
        DBSession.add(recorded_flag)
        value = const.PlayerMapDataValue.FLAG
    else:
        if flag_data.value == const.PlayerMapDataValue.FLAG:
            # FLAG --> UNSURE
            value = const.PlayerMapDataValue.UNSURE
            flag_data.value = value
            DBSession.add(flag_data)
        else:
            # UNSURE --> UNCLICKED
            value = const.CellStates.UNCLICKED
            DBSession.delete(flag_data)
            DBSession.flush()
    return (value, game)


def cascade_reveal(start_x, start_y, mine_matrix):
    """ Returns the list of dicts, representing the values to reveal. """
    # Where the revealed values go. The position records the x, y coordinates
    # Faster lookup than using the reveal list of dicts
    placeholder = Matrix(mine_matrix.height, width=mine_matrix.width,
                         init_value=None)
    blank_spaces = [(start_x, start_y)]  # queue of spaces to explore
    reveal = []

    # Look around each blank space
    while(blank_spaces):
        (focus_x, focus_y) = blank_spaces.pop()
        for x in Matrix._adjacent_indices(focus_x, placeholder.height-1):
            for y in Matrix._adjacent_indices(focus_y, placeholder.width-1):
                # If there isn't an entry in the placeholder for this cell,
                # we haven't "revealed" this yet.
                if (x, y) != (focus_x, focus_y) and placeholder[x][y] is None:
                    value = mine_matrix[x][y]
                    reveal.append({'x': x, 'y': y, 'value': value})
                    placeholder[x][y] = value
                    # Save a ClickMap entry for this cell
                    # TODO: save
                    # If the value is another blank space, save to look later
                    if value is const.CellStates.CLUE[0]:
                        blank_spaces.append((x, y))

    return reveal
