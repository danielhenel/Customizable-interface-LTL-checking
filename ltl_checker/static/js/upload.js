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
        // next button
        document.getElementById("nextButton").onclick = function(){
            form = document.getElementById("uploadFileForm")
            form.submit()
        }
        texttoshow = "the text related to first box should be displayed";
       //****//
       //remove parts of text
       var h = document.getElementsByTagName('h2');
        for (var i = h.length; i--; ) {
            h[i].style.display = 'none';
        }       
        document.getElementById("fail").style.visibility = "hidden";

        //hide upload button
        document.getElementById('browseFileButton').style.display = 'none';

        
        // Reload button
        let btn = document.createElement("rbutton");
        btn.innerHTML =  '<button id="rbutton" name="btn"> <img src="static/images/reload.png"  width="45" height="45" />   '; 
        btn.className = "rbutton";

        btn.addEventListener("click", function () {
            window.location.reload();
        });
       // btn.style.visibility = "hidden" //TODO
        document.body.appendChild(btn);
        
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
                document.getElementById("success").style.visibility = "visible";
                document.getElementById("filena").style.visibility = "visible";

         
       
         

        
    
    }else {
        // red color when the file is in the wrong format
        image.src = "./static/images/cloud-red.png";
        document.getElementById("nextButton").style.visibility = "hidden";
        //alert("The file should be in .csv or .xes format")
        //text for wrong file
        //fixing text
        
        document.getElementById("success").style.visibility = "hidden";
        document.getElementById("filena").style.visibility = "hidden";
        document.getElementById("fail").style.visibility = "visible";
        document.getElementById('browseFileButton').style.style.visibility = "visible";
        
        if (fail && fail.length > 1) {

           // Dont add another one
           return document.getElementById("fail").style.visibility = "hidden";
        }
        $('fail').one('fileFeild', function(e) {
           alert('You will only see this once.');
       });

        
  
        
   }
}
        fail.innerText += ' \n UPLOAD FAILED ! \n The file must be either *.csv or *.xes" ';
         // same as: document.getElementById('fail').innerText += 'textexample'

         
        



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
