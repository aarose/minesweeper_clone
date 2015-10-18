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
        switch (event.which) {
            case 1:  // Left mouse button
                console.log('CLICKED ' + coords)
                // Ajax request to current url + /cell/x,y, POST 
                $(this).load("", function(responseTxt, statusTxt, xhr){
                    if(statusTxt == "success")
                        alert("External content loaded successfully!");
                    if(statusTxt == "error")
                        alert("Error: " + xhr.status + ": " + xhr.statusText);
                });
                break;
            case 3: // Right mouse button
                console.log('RIGHT MOUSE CLICK ' + coords)
                break;
        }
    });
});
