var fileField = document.getElementById('fileField')
fileField.onchange = changeCloudColor

// the function changes the color of the cloud depending on the file format
function changeCloudColor(){
    var image = document.getElementById("cloud-image");

    // get file name
    var fullPath = document.getElementById('fileField').value;
    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var filename = fullPath.substring(startIndex);
        if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
            filename = filename.substring(1);
        }
    }

    format = filename.slice(-3)

    if (format == "csv" || format=="xes"){
        // green color when the file is in the required format
        image.src = "./static/images/cloud-green.png";
    } else {
        // red color when the file is in the wrong format
        image.src = "./static/images/cloud-red.png";
        alert("The file should be in .csv or .xes format")
    }
}


uploadArea = document.getElementById("uploadArea")

uploadArea.addEventListener('dragover',
function(ev) {
ev.preventDefault();
ev.dataTransfer.dropEffect = 'copy';
});

uploadArea.addEventListener('drop',
function(ev) {
ev.preventDefault();
var files = ev.dataTransfer.files;
if (files.length > 1){
    alert("You can only upload one file!")
}
else{
    fileField = document.getElementById('fileField')
    fileField.files = files
    fileField.onchange()
}
});
