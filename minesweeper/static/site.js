$(function(){
    $('td').on('contextmenu', function(){return false;})

    var path = window.location.pathname;

    // Draw in pre-existing flags and "unsures" IF the game is still going
    var state = $('#state').attr('state')
    if(state == 0){
        var flag_path = path + '/flags';
        $.get(flag_path, function(data, statusTxt){
            if(statusTxt == "success"){
                for(i = 0; i < data.flags.length; i++) {
                    var coords = data.flags[i];
                    var flag_id = 'f' + coords[0] + coords[1];
                    var cell_id = get_cell_id(coords[0], coords[1]);
                    $(cell_id).append("<i id='" + flag_id + "' class='fa fa-flag'></i>");
                }
                for(i = 0; i < data.unsures.length; i++) {
                    var coords = data.unsures[i];
                    var flag_id = 'f' + coords[0] + coords[1];
                    var cell_id = '#cell-' + coords[0] + '-' + coords[1];
                    $(cell_id).append("<i id='" + flag_id + "' class='fa fa-question'></i>");
                }
     
            } else {
                console.log(statusTxt);
            }
        });
    }


    var get_cell_id = function(x, y) {
        return '#cell-' + x + '-' + y;
    }

    var update_cell = function(x, y, value) {
        // Remove the 'fresh' class from the cell
        var cell_id = get_cell_id(x, y)
        $(cell_id).removeAttr('class');
        // Update the text for this element
        var new_value = (value - 1);
        if(new_value != 0) {
            $(cell_id).text(new_value);
        }
    }



    $("td").mousedown(function(event){
        // Get the coordinates
        var results = $(this).attr('id').split("-")
        var x = results[1]
        var y = results[2]
        var cell_path = path + '/cell/' + x + ',' + y;
        var cell_id = get_cell_id(x, y);
        var flag_id = '#f' + x + y;
        var fresh = $(cell_id).hasClass('fresh')

        // LEFT CLICK
        if(event.which == 1){
            // Not allowed to left-click if flag is on there
            // or if already revealed (no fresh class)
            if(($(flag_id).length == 0) && fresh) {

                // Ajax request to current url + /cell/x,y, POST 
                $.post(cell_path, {action: event.which}, function(data, statusTxt){
                    if(statusTxt == "success"){

                        if(data.state != 0) {
                            location.reload(true);
                        } else {
                            update_cell(x, y, data.value)
                            if(data.reveal.length > 0){
                                for(i = 0; i < data.reveal.length; i++){
                                    cell = data.reveal[i]
                                    update_cell(cell.x, cell.y, cell.value)
                                }
                            };
                        };

                    }
                    if(statusTxt == "error")
                        console.log("Error: " + statusTxt);
                 });
            }
        } else if(event.which == 3) {  //RIGHT CLICK
            // Don't POST if the square is already revealed
            if(fresh){
                $.post(cell_path, {action: event.which}, function(data, statusTxt){
                    if(statusTxt == "success"){
                        if(data.value == 11) {  // FLAG
                            $(cell_id).append("<i id='f" + x + y + "' class='fa fa-flag'></i>");
                        } else if(data.value == 12) { // UNSURE
                            $(flag_id).remove();
                            $(cell_id).append("<i id='f" + x + y + "' class='fa fa-question'></i>");
                        } else if(data.value == 0) {  // CLEAR
                            $(flag_id).remove();
                        }
                    }
                    if(statusTxt == "error")
                        console.log("Error: " + statusTxt);
                });
            }
        }
    });
});
