$(function(){
    var path = window.location.pathname;
    console.log('CURRENT PATH: ' + path)

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
                console.log(data);
            }
            if(statusTxt == "error")
                console.log("Error: " + xhr.status + ": " + xhr.statusText);
         });
    });
});
