loadDataFromFile(data)

function loadDataFromFile(data){

    var data = JSON.parse(data)
    maxPage = data[1]
    currentPage = data[2]
    deviations_description = data[3]
    messages = deviations_description[0]
    highlight_rows = deviations_description[1]
    var number = document.getElementById("number")
    number.insertAdjacentText('beforeend', currentPage + "/" + maxPage)
    data = JSON.parse(data[0])

    var column_names = Object.keys(data)
    var col_number = column_names.length
    var row_number = Object.keys(data[column_names[0]]).length
    
    // document.getElementById("previousButton").style.visibility = "visible";
    // document.getElementById("previousButton").onclick = function(){window.location.replace('/')}
    // document.getElementById("nextButton").onclick = function(){
    //     var message = prepare_message(data)
    //     fetch('/selectColumns/message', {
    //     method: 'POST',
    //     body: message
    //     }).then(function(){window.location.replace('/selectFilters')})
    // }
    
    dataTable = document.getElementById("data")
    var header = document.createElement('thead');
    var body = document.createElement('tbody')

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
            }
        }
        var bodyRow = document.createElement('tr');
        bodyRow.onmouseenter = function(){this.style.backgroundColor = "white"}
        bodyRow.onmouseleave = function(){this.style.backgroundColor = "#c9b6b6"}
        bodyRow.i = i
        if(highlight_rows.includes(i)){
            bodyRow.onclick = function(){
                var ul = document.createElement("ul")
                messages.forEach(element => {
                    msg = element[0]
                    rows = element[1]
                    if(rows.includes(this.i)){
                        var li = document.createElement("li")
                        li.textContent = msg
                        ul.appendChild(li)
                    }});
                    
                    var popup_html = `
                    <div id="popup_temp" class="modal fade" role="dialog">
                      <div class="modal-dialog modal-dialog-centered">
                              <div class="modal-content">
                                <div class="modal-header">
                                    <p class="modal-title title-style">Deviations found</p>
                                </div>
                                <div class="modal-body">
                                    <p id="dev">
                                    </p>
                                </div>
                                <div class="modal-footer">
                                  <button id="close_button" type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
                                </div>
                              </div>
                      </div>
                    </div>
                    `
                    
                    var popup = createElementFromHTML(popup_html)
                    document.body.appendChild(popup)
                    popup.style.position = "absolute"
                    popup.style.top = "0px !important" //window.scrollY + popup.getBoundingClientRect().top
                    var dev = document.getElementById("dev")
                    dev.appendChild(ul)

                    var close = document.getElementById("close_button")
                    close.onclick = function(){
                        document.getElementById("a_temp").remove()
                        document.getElementById("popup_temp").remove()
                    }

                    var a_html = '<a id="a_temp" data-toggle="modal" data-target="#popup_temp" href="#"></a>'
                    a = createElementFromHTML(a_html)

                    dropdown_list = document.getElementById("dropdown-list")
                    dropdown_list.appendChild(a)
                   
                    windowscrollY = window.scrollY
                    a.click()
                    popup.style.position = "absolute"
                    popup.style.top = windowscrollY + "px"
            }

        }
        body.appendChild(bodyRow)
        for (var j = 0; j < col_number ; j++){ // for each column
            var bodyItem = document.createElement("td")
            bodyItem.innerText = data[column_names[j]][i]
            if(highlight_rows.includes(i)){bodyItem.style.color = "red"; bodyItem.style.fontWeight = "bold";}
                
            bodyRow.appendChild(bodyItem)
    }
}

    dataTable.appendChild(header)
    dataTable.appendChild(body)

    dataHeight = document.getElementById("data").offsetHeight
    additional = dataHeight + 300
    document.getElementById("middle").style.height = additional.toString() + "px"
    var prev = document.getElementById("prevPage")
    if(currentPage > 1){prev.style.visibility = "visible"
    prev.href = "/results?page=" + (currentPage - 1)}
    else{prev.style.visibility = "hidden"}
    var next = document.getElementById("nextPage")
    if(currentPage < maxPage){
        next.style.visibility = "visible"
        next.href = "/results?page=" + (currentPage + 1)
    }
    else{next.style.visibility = "hidden"}
}


function createElementFromHTML(html_str){
    const temp = document.createElement("div");
    temp.innerHTML = html_str;
    return temp.firstElementChild;
}