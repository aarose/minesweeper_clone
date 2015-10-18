$(function(){
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
                    var cell_id = '#cell-' + coords[0] + '-' + coords[1];
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


    $("td").mousedown(function(event){
        // Get the coordinates
        var results = $(this).attr('id').split("-")
        var x = results[1]
        var y = results[2]
        var cell_path = path + '/cell/' + x + ',' + y;
        var cell_id = '#cell-' + x + '-' + y;
        var flag_id = '#f' + x + y;

        // LEFT CLICK
        if(event.which == 1){
            // Not allowed to left-click if flag is on there
            if($(flag_id).length == 0) {
                // Ajax request to current url + /cell/x,y, POST 
                $.post(cell_path, {action: event.which}, function(data, statusTxt){
                    if(statusTxt == "success"){
                        if(data.state != 0) {
                            location.reload(true);
                        } else {
                            // Remove the 'fresh' class from the cell
                            $(cell_id).removeAttr('class');
                            // Update the text for this element
                            var new_value = data.value -1;
                            if(new_value!=0) {
                                $(cell_id).text(data.value-1);
                            }
                        };
                    }
                    if(statusTxt == "error")
                        console.log("Error: " + statusTxt);
                 });
            }
        } else if(event.which == 3) {  //RIGHT CLICK
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
    });
});
