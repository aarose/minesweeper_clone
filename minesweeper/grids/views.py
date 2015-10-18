#!/usr/bin/python
from pyramid.view import (
    view_config,
    view_defaults,
    )
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from minesweeper.grids import constants as const
from minesweeper.grids import models
from minesweeper.grids.matrices import (
    MineMatrix,
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


@view_config(route_name='view_game', request_method='GET', http_cache=3600,
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

    grid = derive_grid(mine_map, game.id)

    response = {
        'game': True,
        'height': mine_map.height,
        'width': mine_map.width,
        'mines': number_of_mines,
        'state': game.state,
        'grid': grid,
    }
    return response


@view_config(route_name='cell_get', request_method='POST', renderer='json')
def update_cell(request):
    """ Executes the provided action upon the cell, returns the state. """
    game = get_game_or_none(request)
    if game is None:
        return HTTPNotFound('No such game.')

    # If the game is not in progress (won or lost) then no action is allowed
    if game.state != const.GameState.IN_PROGRESS:
        return HTTPForbidden('The game is over.')

    # See if there's an entry for x,y in the Click Map of this Game
    x = request.matchdict['x']
    y = request.matchdict['y']
    click_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game.id, map_type=const.PlayerMapType.CLICK).first()

    # If there's a click data entry, the cell has already been clicked
    # No further action is allowed
    click_data = DBSession.query(models.PlayerMapData).filter_by(
        player_map_id=click_map.id, row_num=x, col_num=y).first()
    if click_data:
        return HTTPForbidden('The cell has alread been revealed.')

    value = None
    reveal = []

    action = request.POST.get('action')
    if action is const.Action.LEFT_CLICK:
        value, reveal = left_click(x, y, click_map, game)

    elif action is const.Action.RIGHT_CLICK:
        value, reveal = right_click(x, y, game)

    return {'state': game.state, 'value': value, 'reveal': reveal}


def get_game_or_none(request):
    game_id = request.matchdict['game_id']
    game = DBSession.query(models.Game).get(game_id)
    return game


def derive_grid(mine_map, game_id):
    """ Returns the derived grid (mine matrix * click matrix) """
    mine_matrix = mine_map.to_matrix()
    click_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game_id, map_type=const.PlayerMapType.CLICK).first()
    click_matrix = click_map.to_matrix()  # Acts as a mask
    return multiply(mine_matrix, click_matrix)


def left_click(x, y, click_map, game):
    # Record a successful click on the Click Map, and reveal the cell
    recorded_click = models.PlayerMapData(
        player_map_id=click_map.id, row_num=x, col_num=y,
        value=const.PlayerMapDataValue.CLICKED)
    DBSession.add(recorded_click)

    # Get this cell's true contents
    mine_data = DBSession.query(models.MineMapData).filter_by(
        mine_map_id=game.mine_map, row_num=x, col_num=y).first()
    value = mine_data.value

    # If the cell contains a mine, it's game over
    if value is const.MineMapDataValue.MINE:
        # Update game state
        game.state = const.GameState.LOSE
        DBSession.add(game)
        DBSession.flush()
    else:
        # TODO: how to cascade reveal
        if value is const.MineMapDataValue.CLUE[0]:
            # Cascade reveal.
            pass
            # For each adjacent cell, store the coordinates and the value
            # contained in the MineMap
    # TODO: How to check for winning condition after a cascade or reveal
    # that isn't a mine
    # if, after all the reveal click records are noted, the click map
    # matches the winning map (mine_matrix * 0.1)', then the game is won


def right_click(x, y, game):
    # Set/increment/clear the flag in this cell
    flag_map = DBSession.query(models.PlayerMap).filter_by(
        game_id=game.id, map_type=const.PlayerMapType.FLAG).first()
    # Check to see if there's a flag set for this cell
    flag_data = DBSession.query(models.PlayerMapData).filter_by(
        player_map_id=flag_map.id, row_num=x, col_num=y).first()

    # If there was no entry, so add flag
    if flag_data is None:
        recorded_flag = models.PlayerMapData(
            player_map_id=flag_map.id, row_num=x, col_num=y,
            value=const.PlayerMapDataValue.FLAG)
        DBSession.add(recorded_flag)
        value = const.PlayerMapDataValue.FLAG
    else:
        # There was an entry, so we either increment or delete
        # If it was a FLAG, increment to an UNSURE
        if flag_data.value == const.PlayerMapDataValue.FLAG:
            value = const.PlayerMapDataValue.UNSURE
            flag_data.value = value
            DBSession.add(flag_data)
        else:
            # If an UNSURE, delete
            value = const.CellStates.UNCLICKED
            raise NotImplementedError('DELETE HERE')
