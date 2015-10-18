<%inherit file="base.html"/>
% if game:
    <table class="pure-table pure-table-bordered" id="mine-grid">
        <thead>
            <tr>
                <th colspan=${width} id="mine-count">10</th>
            </tr>
        </thead>

        <tbody>
            % for i in range(height):
            <tr>
                % for j in range(width):
                <td id="">${loop.parent.index},${loop.index}</td>
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
