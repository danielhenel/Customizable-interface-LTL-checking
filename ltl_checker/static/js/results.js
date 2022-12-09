loadDataFromFile(data)

function loadDataFromFile(data){

    var data = JSON.parse(data)
    numberOfRows = data[1]
    var number = document.getElementById("number")
    number.insertAdjacentText('beforeend', numberOfRows)
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
}