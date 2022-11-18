var file_field = document.getElementById('file_field')
file_field.onchange = change_cloud_color

function change_cloud_color(){
    var image = document.getElementById("cloud-image");

    // get file name
    var fullPath = document.getElementById('file_field').value;
    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var filename = fullPath.substring(startIndex);
        if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
            filename = filename.substring(1);
        }
    }

    format = filename.slice(-3)

    if (format == "csv" || format=="xes"){
        image.src = "./static/images/cloud-green.png";
    } else {
        image.src = "./static/images/cloud-red.png";
    }
}