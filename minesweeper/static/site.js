$(function(){
    var path = window.location.pathname;

    $("td").mousedown(function(event){
        // Get the coordinates
        var coords = $(this).attr('id')
        var results = coords.split("-")
        var x = results[1]
        var y = results[2]
        console.log('X: ' + x + ' | Y: ' + y)
        var cell_path = path + '/cell/' + x + ',' + y;
        console.log(cell_path)

        // Ajax request to current url + /cell/x,y, POST 
        $.post(cell_path, {action: event.which}, function(data, statusTxt){
            if(statusTxt == "success"){
                if(data.state != 0) {
                    location.reload(true);
                } else {
                    // Remove the 'fresh' class from the cell
                    var cell_id = '#cell-' + x + '-' + y;
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
    });
});
