function loadDataFromFile(){
    dataTable = document.getElementById("data")
    selectColumnsTable = document.getElementById("selectColumnsTable")
    renameColumnsTable = document.getElementById("renameColumnsTable")

    var header = document.createElement('thead');
    var body = document.createElement('tbody')
    
    for (var i = 0; i < 5; i++ ){ // for each row
        if (i == 0){ // the first row is the header
            var headerRow = document.createElement('tr');
            header.appendChild(headerRow)

            var selectColumnsRow = document.createElement('tr')
            var selectColumnsBody = document.createElement('tbody')
            selectColumnsBody.appendChild(selectColumnsRow)
            selectColumnsTable.appendChild(selectColumnsBody)

            var renameColumnsRow = document.createElement('tr')
            var renameColumnsBody = document.createElement('tbody')
            renameColumnsBody.appendChild(renameColumnsRow)
            renameColumnsTable.appendChild(renameColumnsBody)

            for (var j = 0; j < 5 ; j++){ // for each column
                // header
                headerItem = document.createElement("th")
                headerItem.scope = "col"
                headerItem.innerText = "COLUMN NAME"
                headerRow.appendChild(headerItem)

                // select columns row
                selectColumnsItem = document.createElement("td")
                selectList = document.createElement('select')
                selectList.onchange = verifyRequiredColumns

                caseID = document.createElement('option')
                caseID.value = "caseID"
                caseID.innerText = "Case ID"
                selectList.appendChild(caseID)

                activityName = document.createElement('option')
                activityName.value = "activityName"
                activityName.innerText = "Activity Name"
                selectList.appendChild(activityName)

                timeStamp = document.createElement('option')
                timeStamp.value = "timeStamp"
                timeStamp.innerText = "Time Stamp"
                selectList.appendChild(timeStamp)

                resource = document.createElement('option')
                resource.value = "resource"
                resource.innerText = "Resource"
                selectList.appendChild(resource)

                additional = document.createElement('option')
                additional.value = "additional"
                additional.innerText = "Additional"
                selectList.appendChild(additional)

                drop = document.createElement('option')
                drop.value = "drop"
                drop.innerText = "Drop"
                selectList.appendChild(drop)

                selectColumnsItem.appendChild(selectList)
                selectColumnsRow.appendChild(selectColumnsItem)

                // rename columns row
                renameColumnsItem = document.createElement("td")
                input = document.createElement("input")
                input.type = "text"
                renameColumnsItem.appendChild(input)
                renameColumnsRow.appendChild(renameColumnsItem)
            }
        }
        else{
            var bodyRow = document.createElement('tr');
            body.appendChild(bodyRow)
            for (var j = 0; j < 5 ; j++){ // for each column
                bodyItem = document.createElement("td")
                bodyItem.innerText = "DATA"
                bodyRow.appendChild(bodyItem)
            }
        }
    }

    dataTable.appendChild(header)
    dataTable.appendChild(body)

    verifyRequiredColumns()
}

loadDataFromFile();

function verifyRequiredColumns(){
var requiredColumns = {
    "caseID" : 0,
    "activityName" : 0,
    "timeStamp" : 0,
    "resource" : 0
}

selectColumnsRow = document.getElementById("selectColumnsTable").firstChild.firstChild

selectColumnsRow.childNodes.forEach((selectColumnsItem) => {
selectList = selectColumnsItem.firstChild
selected = selectList.value
if (selected in requiredColumns){
    requiredColumns[selected] += 1
}
});

showNextButton = true

Object.keys(requiredColumns).forEach((key) => {
    label = document.getElementById(key)
    if (requiredColumns[key] == 1){
        label.style.color = "green"
    }
    else{
        label.style.color = "red"
        showNextButton = false
    }
});


if (showNextButton){
    document.getElementById("nextButton").style.visibility = "visible";
}
else{
    document.getElementById("nextButton").style.visibility = "hidden";
}

}