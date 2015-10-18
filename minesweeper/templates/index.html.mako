<%inherit file="base.html"/>
% if game:
    <table class="pure-table" id="mine-grid">
        <thead>
            <tr>
                <th colspan=2 id="mine-count">Mines: ${mines}</th>
                <th colspan=${width-4}>
                    % if state is 1:
                        <i class="fa fa-smile-o"></i>
                    % elif state is -1:
                        <i class="fa fa-frown-o"></i>
                    % endif
                </th>
                <th colspan=2 id="state">
                    % if state is 0:
                        IN PROGRESS
                    % elif state is 1:
                        YOU WIN!
                    % elif state is -1:
                        GAME OVER
                    % endif
                </th>
            </tr>
        </thead>

        <tbody>
            % for row in grid:
            <tr>
                % for value in row:
                <td id="cell-${loop.parent.index}-${loop.index}"
                % if value == 0:
                    class="fresh">
                % else:
                    >
                % endif
                    % if (value-1) > 0:
                        % if value == 10:
                            % if state == 1:
                                <i class="fa fa-bomb safe"></i>
                            % else:
                                <i class="fa fa-bomb red"></i>
                            % endif
                        % else:
                            ${value-1}
                        % endif
                    % endif
                </td>
                % endfor
            </tr>
            % endfor
        </tbody>
    </table>

    % if state is not 0:
        <form class="pure-form" action='/' method="POST">
            <button type="submit" class="pure-button button-primary">
                New Game
            </button>
        </form>
    % endif

% else:
    <form class="pure-form" action='/' method="POST">
        <button type="submit" class="pure-button button-primary">
            New Game
        </button>
    </form>
% endif
