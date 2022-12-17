body = document.createElement('tbody')
filters.appendChild(body)
rowCounter = 0
leftBracketCounter = 0
rightBracketCounter = 0
emptyFilter = false
refresh = false
attributes = data

document.getElementById("previousButton").style.visibility = "visible";
document.getElementById("previousButton").onclick = function(){window.location.replace('/selectColumns2')}
document.getElementById("nextButton").onclick = function(){
    var message = prepare_message()
    fetch('/selectFilters/message', {
    method: 'POST',
    body: message
    }).then(function(){window.location.replace('/results')})   
}

createFirstRow()

function createFirstRow() {

    var initialRow = document.createElement('tr')
    body.appendChild(initialRow)
    rowCounter += 1
    createNewRowBelow(initialRow)
}

function createNewRowBelow(previousRow){
    var row = document.createElement('tr')

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
    col.appendChild(createSelectAttributeList(attributes))
    row.appendChild(col)

    // select second attribute
    col = document.createElement("td")
    col.colSpan = "3"
    col.appendChild(createSelectAttributeList(attributes))
    row.appendChild(col)
    
    if(attributes.length > 2){
        // select third attribute
        col = document.createElement("td")
        col.colSpan = "3"
        col.appendChild(createSelectAttributeList(attributes))
        row.appendChild(col)

        // select fourth attribute
        col = document.createElement("td")
        col.colSpan = "3"
        col.appendChild(createSelectAttributeList(attributes))
        row.appendChild(col)
    }

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

    filterSelected(selectFilter)
    check_formula()
}


function createSelectOptionList (){
    var selectList = document.createElement('select')
    selectList.style.width = "100%"
    selectList.classList.add("selectList")
    selectList.classList.add("selectOption")
    //optionSelected(selectList)
    selectList.onchange = function(){optionSelected(selectList) 
        check_formula()}

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
            item.value = "|"
            item.innerText = "OR"
            selectList.appendChild(item)
        
            item = document.createElement('option')
            item.value = "&"
            item.innerText = "AND"
            selectList.appendChild(item)
    
            item = document.createElement('option')
            item.value = "& ("
            item.innerText = "AND ("
            selectList.appendChild(item)
        
            item = document.createElement('option')
            item.value = "| ("
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
    selectList.onchange = function(){filterSelected(selectList)
        check_formula()}

    var item = document.createElement('option')
    item.value = "four_eyes_principle"
    item.innerText = "Four eyes principle"
    selectList.appendChild(item)

    item = document.createElement('option')
    item.value = "attribute_value_different_persons"
    item.innerText = "Attribute value different persons"
    selectList.appendChild(item)

    item = document.createElement('option')
    item.value = "eventually_follows_2"
    item.innerText = "Eventually follows AB"
    selectList.appendChild(item)

    item = document.createElement('option')
    item.value = "eventually_follows_3"
    item.innerText = "Eventually follows ABC"
    selectList.appendChild(item)

    item = document.createElement('option')
    item.value = "eventually_follows_4"
    item.innerText = "Eventually follows ABCD"
    selectList.appendChild(item)

    if(emptyFilter){
        item = document.createElement('option')
        item.value = "empty"
        item.innerText = ""
        selectList.appendChild(item)
    }
    
    return selectList
}

function createSelectAttributeList(attributes){

    var selectList = document.createElement('select')
    selectList.style.width = "100%"
    selectList.classList.add("selectList")
    selectList.classList.add("selectFristAttribute")

    selectList.onchange = function(){check_formula()}
    
    attributes.forEach(function(attribute){

        var item = document.createElement('option')
        item.value = attribute
        item.innerText = attribute
        selectList.appendChild(item)

    })
    return selectList
}

function createAddButton(previousRow){
    var button = document.createElement("button")
    button.classList.add("addButton")
    button.onclick = function(){createNewRowBelow(previousRow)}
    var img = document.createElement("img")
    img.classList.add("addButtonIMG")
    img.src = "static/images/plus.png"
    button.appendChild(img)
    return button
}

function createDeleteButton(row){
    var button = document.createElement("button")
    button.classList.add("deleteButton")
    button.onclick = function(){
        var parent = row.parentElement
        var fields = row.children
        var option = fields[0].firstChild.value
        if(option == ")"){
            rightBracketCounter --
        }
        else if(option == "(" || option == "| (" || option == "| ("){
            leftBracketCounter --
        }
        parent.removeChild(row)
        rowCounter -= 1
    }
    var img = document.createElement("img")
    img.src = "static/images/bin.png"
    img.classList.add("deleteButtonIMG")
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
        //hide third attribute
        row.children[4].style.visibility = "hidden"
        //hide fourth attribute
        row.children[5].style.visibility = "hidden"
        //delete empty
        for(const child of filterSelectList.children)
        {  
            if(child.value == "empty")
            filterSelectList.removeChild(child)
        }
        emptyFilter = false
    }
    else if (selected=="(" || selected =="& (" || selected == "| ("){
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

    visibility = {
        "four_eyes_principle":["visible","visible","hidden","hidden"],
        "attribute_value_different_persons":["visible","hidden","hidden","hidden"],
        "eventually_follows_2":["visible","visible","hidden","hidden"],
        "eventually_follows_3":["visible","visible","visible","hidden"],
        "eventually_follows_4":["visible","visible","visible","visible"],
    }

    if(selected in visibility){
        emptyFilter = false
        //first attribute
        row.children[2].style.visibility = visibility[selected][0]
        //second attribute
        row.children[3].style.visibility = visibility[selected][1]
        //third attribute
        row.children[4].style.visibility = visibility[selected][2]
        //fourth attribute
        row.children[5].style.visibility = visibility[selected][3]
    }
    else{
        emptyFilter = true
        //hide first attribute
        row.children[2].style.visibility = "hidden"
        //hide second attribute
        row.children[3].style.visibility = "hidden"
        //hide third attribute
        row.children[4].style.visibility = "hidden"
        //hide fourth attribute
        row.children[5].style.visibility = "hidden"
        leftBracketCounter += 1
        createNewRowBelow(row)
        emptyFilter = false
    }
}

function prepare_message(){
    
    var rows = body.children
    
    var expression = ""
    var dictionary = {}
    var terms = {}
    var currentTerm = 64

    for(var i=1; i<rows.length; i++){
        // 6 fields
        var fields = rows[i].children
        var option = null
        var filter = null
        var attributes = []
        var key = ""
        var rightBracket = false
        for(var j=0; j<6; j++){
            
            var select = fields[j].firstChild
            
            if(j==0){
                option = select.value
                if(option!="empty"){
                expression = expression.concat(" ", option)
                if(option == ")"){
                    rightBracket = true
                    break
                }
                }
            }
            else if(j==1){
                filter = select.value
                key = key.concat(filter)
            }
            else{
                if(fields[j].style.visibility != "hidden")
                {
                    attribute = select.value
                    attributes.push(attribute)
                    key = key.concat(attribute)
                }
            }
        }
        if(rightBracket){continue}
        // check if the term exists
        if(key in dictionary){
            var term = terms[key]
            expression = expression.concat(" ",term)
        }
        else{
            //create new term
            currentTerm += 1
            if(currentTerm == 91){ //Z
                currentTerm = 97 //a
            }
            var newTerm = String.fromCharCode(currentTerm)
            terms[key] = newTerm
            expression=expression.concat(" ",newTerm)
            dictionary[key] = [filter,attributes]
        }
    }


    var result_dict = {}
    Object.keys(dictionary).forEach(
        (key) => {
            result_dict[terms[key]] = dictionary[key]
        }
    )

    var message = [result_dict,expression]
    return JSON.stringify(message)
}

function check_formula(){
    
    var rows = body.children
    var right = 0
    var left = 0

    for(var i=1; i<rows.length; i++){
        var fields = rows[i].children
        var attributes = []
        for(var j=0; j<6; j++){
            var select = fields[j].firstChild
            
            if(j==0){
                if(select.value == "(" || select.value == "| (" || select.value == "& ("){
                    left ++
                }
                else if(select.value == ")"){
                    right ++
                }
            }
            else if (j>1){
                if(fields[j].style.visibility != "hidden")
                {
                    var attribute = select.value
                    attributes.push(attribute)
                }
            }

            for(var k=0; k<attributes.length; k++)
            {
                for(var l=0; l<attributes.length; l++){
                    if(k!=l){
                        if(attributes[k] == attributes[l]){
                        }
                    }
                }
            }
        }
    }

    if(left==right){
        document.getElementById("nextButton").style.visibility = "visible";
    }
    else{
        document.getElementById("nextButton").style.visibility = "hidden";
    }
}