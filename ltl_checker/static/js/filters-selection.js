body = document.createElement('tbody')
filters.appendChild(body)
rowCounter = 0
leftBracketCounter = 0
rightBracketCounter = 0
emptyFilter = false
refresh = false

createFirstRow()

function createFirstRow() {

    var initialRow = document.createElement('tr')
    body.appendChild(initialRow)
    rowCounter += 1
    createNewRowBelow(initialRow)
}

function createNewRowBelow(previousRow){
    var row = document.createElement('tr')
    attributes = ["A","B","C","D"]
    firstAttibute = "D"

    // select option (,),OR, AND
    var col = document.createElement("td")
    col.colSpan = "1"
    var selectOption = createSelectOptionList()
    col.appendChild(selectOption)
    row.appendChild(col)
    

    // select filter
    col = document.createElement("td")
    col.colSpan = "9"
    var selectFilter = createSelectFilterList()
    col.appendChild(selectFilter)
    row.appendChild(col)

    // select first attribute
    col = document.createElement("td")
    col.colSpan = "3" 
    col.appendChild(createSelectFirstAttributeList(attributes))
    row.appendChild(col)

    // select second attribute
    col = document.createElement("td")
    col.colSpan = "3"
    col.appendChild(createSelectSecondAttributeList(attributes,firstAttibute))
    row.appendChild(col)
    
    // add button
    col = document.createElement("td")
    col.colSpan = "1"
    col.appendChild(createAddButton(row))
    row.appendChild(col)

    // delete button
    col = document.createElement("td")
    col.colSpan = "1"
    if(rowCounter!=1){
        col.appendChild(createDeleteButton(row))
    }
    row.appendChild(col)

    body.insertBefore(row, previousRow.nextSibling);
    rowCounter += 1
}


function createSelectOptionList (){
    var selectList = document.createElement('select')
    selectList.style.width = "100%"
    selectList.classList.add("selectList")
    selectList.classList.add("selectOption")
    //optionSelected(selectList)
    selectList.onchange = function(){optionSelected(selectList)}

    if(rowCounter == 1){
        var item = document.createElement('option')
        item.value = "empty"
        item.innerText = ""
        selectList.appendChild(item)

        item = document.createElement('option')
        item.value = "("
        item.innerText = "("
        selectList.appendChild(item)
    }

    if(rowCounter > 1){
        if(emptyFilter){
            var item = document.createElement('option')
            item.value = "("
            item.innerText = "("
            selectList.appendChild(item)
        }
        else{
            var item = document.createElement('option')
            item.value = "OR"
            item.innerText = "OR"
            selectList.appendChild(item)
        
            item = document.createElement('option')
            item.value = "AND"
            item.innerText = "AND"
            selectList.appendChild(item)
    
            item = document.createElement('option')
            item.value = "AND ("
            item.innerText = "AND ("
            selectList.appendChild(item)
        
            item = document.createElement('option')
            item.value = "OR ("
            item.innerText = "OR ("
            selectList.appendChild(item)
        }
    }

    if(leftBracketCounter - rightBracketCounter > 0 && !emptyFilter){
        var item = document.createElement('option')
        item.value = ")"
        item.innerText = ")"
        selectList.appendChild(item)
    }

    return selectList
}

function createSelectFilterList(){
    var selectList = document.createElement('select')
    selectList.style.width = "100%"
    selectList.classList.add("selectList")
    selectList.classList.add("selectFilter")
    //filterSelected(selectList)
    selectList.onchange = function(){filterSelected(selectList)}

    var item = document.createElement('option')
    item.value = "F"
    item.innerText = "Four eyes principle"
    selectList.appendChild(item)

    item = document.createElement('option')
    item.value = "A"
    item.innerText = "Attribute value different persons"
    selectList.appendChild(item)

    item = document.createElement('option')
    item.value = "E"
    item.innerText = "Eventually follows"
    selectList.appendChild(item)

    if(emptyFilter){
        item = document.createElement('option')
        item.value = "empty"
        item.innerText = ""
        selectList.appendChild(item)
    }

    return selectList
}

function createSelectFirstAttributeList(attributes){

    var selectList = document.createElement('select')
    selectList.style.width = "100%"
    selectList.classList.add("selectList")
    selectList.classList.add("selectFristAttribute")
    // firstAttributeSelected(selectList)
    selectList.onchange = function(){firstAttributeSelected(selectList)}
    
    attributes.forEach(function(attribute){

        var item = document.createElement('option')
        item.value = attribute
        item.innerText = attribute
        selectList.appendChild(item)

    })

    return selectList
}

function createSelectSecondAttributeList(attributes,firstAttibute){

    var selectList = document.createElement('select')
    selectList.style.width = "100%"
    selectList.classList.add("selectList")
    selectList.classList.add("selectSecondAttribute")
  //  secondAttributeSelected(selectList)
    selectList.onchange = function(){secondAttributeSelected(selectList)}
    
    attributes.forEach(function(attribute){

        if(attribute != firstAttibute){
            var item = document.createElement('option')
            item.value = attribute
            item.innerText = attribute
            selectList.appendChild(item)
        }
    })
    
    return selectList
}

function createAddButton(previousRow){
    var button = document.createElement("button")
    button.classList.add("addButton")
    button.onclick = function(){createNewRowBelow(previousRow)}
    var img = document.createElement("img")
    img.src = "static/images/plus.png"
    button.appendChild(img)
    return button
}

function createDeleteButton(row){
    var button = document.createElement("button")
    button.classList.add("deleteButton")
    button.onclick = function(){
        parent = row.parentElement
        parent.removeChild(row)
        rowCounter -= 1}
    var img = document.createElement("img")
    img.src = "static/images/bin.png"
    button.appendChild(img)
    return button
}


function optionSelected(selectList){
    var selected = selectList.value
    var row = selectList.parentElement.parentElement
    var filterSelectList = row.children[1].children[0]
    if(selected==")"){
        rightBracketCounter += 1
        //hide filters 
        row.children[1].style.visibility = "hidden"
        //hide first attribute
        row.children[2].style.visibility = "hidden"
        //hide second attribute
        row.children[3].style.visibility = "hidden"
        //delete empty
        for(const child of filterSelectList.children)
        {  
            if(child.value == "empty")
            filterSelectList.removeChild(child)
        }
        emptyFilter = false
    }
    else if (selected=="(" || selected =="AND (" || selected == "OR ("){
        leftBracketCounter += 1
        //add empty
        var item = document.createElement('option')
        item.value = "empty"
        item.innerText = ""
        filterSelectList.appendChild(item)
        //show filters 
        row.children[1].style.visibility = "visible"
        filterSelectList.onchange()

    }
    else{
        //show filters 
        row.children[1].style.visibility = "visible"
        //delete empty
        for(const child of filterSelectList.children)
        {  
            if(child.value == "empty")
            filterSelectList.removeChild(child)
        }
        filterSelectList.onchange()
    }
}

function filterSelected(selectList){
    var selected = selectList.value
    var row = selectList.parentElement.parentElement

    if(selected=="F") // four eyes principle
    {
        emptyFilter = false
        //show first attribute
        row.children[2].style.visibility = "visible"
        //show second attribute
        row.children[3].style.visibility = "visible"
    }
    else if(selected=="A") // attribute value different persons
    {
        emptyFilter = false
        //show first attribute
        row.children[2].style.visibility = "visible"
        //hide second attribute
        row.children[3].style.visibility = "hidden"
    }
    else if(selected=="E") //eventually follows
    {
        emptyFilter = false
        //show first attribute
        row.children[2].style.visibility = "visible"
        //show second attribute
        row.children[3].style.visibility = "visible"
    }
    else{
        emptyFilter = true
        //hide first attribute
        row.children[2].style.visibility = "hidden"
        //hide second attribute
        row.children[3].style.visibility = "hidden"
        leftBracketCounter += 1
        createNewRowBelow(row)
        emptyFilter = false
    }
    // if(!refresh){
    // refreshNextRows(row)}
}

function refreshRow(row){
    selectOption = row.children[0].children[0]
    selectFilter = row.children[0].children[0]
    selectOption.onchange()
    selectFilter.onchange()
}

// function refreshNextRows(row){
//     refresh = true
//     var parent = row.parentElement
//     var found = false
//     for(const child of parent.children){
//         if(child == row){
//             found = true
//             continue
//         }
//         if(refresh){
//             refreshRow(row)
//         }
//     }
//     refresh = false
// }