function loadDataFromFile(data){

    data = JSON.parse(data)
    column_names = Object.keys(data)
    col_number = column_names.length
    row_number = Object.keys(data[column_names[0]]).length

    document.getElementById("previousButton").style.visibility = "visible";
    dataTable = document.getElementById("data")
    var header = document.createElement('thead');
    var body = document.createElement('tbody')
    var selectColumnsRow = document.createElement('tr')
    var renameColumnsRow = document.createElement('tr')
    
    for (var i = 0; i < row_number; i++ ){ // for each row
        if (i == 0){ // the first row is the header
            var headerRow = document.createElement('tr');
            header.appendChild(headerRow)

            for (var j = 0; j < col_number ; j++){ // for each column
                // header
                headerItem = document.createElement("th")
                headerItem.scope = "col"
                headerItem.innerText = column_names[j]
                headerRow.appendChild(headerItem)

                // select columns row
                selectColumnsItem = document.createElement("td")
                selectList = document.createElement('select')
                selectList.style.width = "100%"
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
                input.style.width = "100%"
                renameColumnsItem.appendChild(input)
                renameColumnsRow.appendChild(renameColumnsItem)
            }
        }
        else{
            var bodyRow = document.createElement('tr');
            body.appendChild(bodyRow)
            for (var j = 0; j < col_number ; j++){ // for each column
                bodyItem = document.createElement("td")
                bodyItem.innerText = data[column_names[j]][i]
                bodyRow.appendChild(bodyItem)
            }
        }
    }

    dataTable.appendChild(header)
    dataTable.appendChild(body)

    //select columns
    row = document.createElement("tr")
    col = document.createElement("td")
    col.colSpan = "7"
    selectColumnsLabel = document.createElement("div")
    selectColumnsLabel.innerText = "Select columns:"
    col.appendChild(selectColumnsLabel)
    row.appendChild(col)
    body.appendChild(row)
    body.appendChild(selectColumnsRow)

    //rename colums row
    row = document.createElement("tr")
    col = document.createElement("td")
    col.colSpan = "7"
    renameColumnsLabel = document.createElement("div")
    renameColumnsLabel.innerText = "Rename columns:"
    col.appendChild(renameColumnsLabel)
    row.appendChild(col)
    body.appendChild(row)
    body.appendChild(renameColumnsRow)
    verifyRequiredColumns()
}



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