<%inherit file="base.html"/>
% if game:
    <table class="pure-table" id="mine-grid">
        <thead>
            <tr>
                <th id="mine-count">${mines}</th>
                <th colspan=${width-2}></th>
                <th id="state">${state}</th>
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
                            <i class="fa fa-bomb red"></i>
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
% else:
    <form class="pure-form" action='/' method="POST">
        <button type="submit" class="pure-button button-primary">
            New Game
        </button>
    </form>
% endif
