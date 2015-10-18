$(function(){
    var path = window.location.pathname;

    var success_update = function(data) {
        if(data.state != 0) {
            location.reload(true);
        } else {
            // Remove the 'fresh' class from this element
            // Update the text for this element
            console.log($(this));
        }
    }

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
                console.log("External content loaded successfully!");
                success_update(data);
            }
            if(statusTxt == "error")
                console.log("Error: " + statusTxt);
         });
    });
});
