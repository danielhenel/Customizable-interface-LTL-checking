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
        // user can go forward
        document.getElementById("nextButton").style.visibility = "visible";
        texttoshow = "the text related to first box should be displayed";
       //****//
       //remove parts of text
       var h = document.getElementsByTagName('h2');
        for (var i = h.length; i--; ) {
            h[i].style.display = 'none';
        }       
        document.getElementById("fail").style.visibility = "hidden";

        //hide upload button DOES NOT WORK
        document.getElementById('fileField').style.display = 'none';

        
        //display file name
        success.innerText += ' File successfully uploaded ';
        var fullPath = document.getElementById('fileField').value;
            if (fullPath) {
                var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
                var filename = fullPath.substring(startIndex);
                    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
                        filename = filename.substring(1);
                     }
                    
                    filena.innerText += filename ;
            }

        // Reload button
        let btn = document.createElement("rbutton");
        btn.innerHTML =  '<button id="rbutton" name="btn"> <img src="static/images/reload.png"  width="45" height="45" />   '; 
        btn.className = "rbutton";

        btn.addEventListener("click", function () {
            window.location.reload();
        });
        
        document.body.appendChild(btn);

        

    } else {
        // red color when the file is in the wrong format
        image.src = "./static/images/cloud-red.png";
        document.getElementById("nextButton").style.visibility = "hidden";
        //alert("The file should be in .csv or .xes format")
        //text for wrong file
        fail.innerText += ' \n UPLOAD FAILED ! \n The file must be either *.csv or *.xes" ';
         // same as: document.getElementById('fail').innerText += 'textexample'
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