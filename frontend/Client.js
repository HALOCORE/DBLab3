var url = "http://localhost:8000/api/v1/APICustomer";



// url 后统一以'/'结尾
function Ajax(type, url, data, success, failed){
    var xhr = null;
    if(window.XMLHttpRequest){
        xhr = new XMLHttpRequest();
    } else {
        xhr = new ActiveXObject('Microsoft.XMLHTTP')
    }
 
    var type = type.toUpperCase();
    var random = Math.random();

    if(typeof data == 'object'){
        var str = '';
        for(var key in data){
            str += key+'='+data[key]+'&';
        }
        data = str.replace(/&$/, '');
    }
 
    if(type == 'GET'){
        if(data){
            xhr.open('GET', url + '?' + data, true);
        } else {
            xhr.open('GET', url, true);
        }
        xhr.send();
 
    } else if(type == 'POST'){
        xhr.open('POST', url, true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(data);
    } else if(type == 'DELETE'){  
        if(data){
            xhr.open('DELETE', url + data, false);
            
        } else{
            xhr.open('DELETE', url, false);
        }
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send();
    } else if(type == 'PUT'){
        xhr.open('PUT', url, true);
        xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
        xhr.send(data);
    }
    
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4){
            if(xhr.status == 200){
                console.log("success");
                console.log(typeof xhr.responseText)
                success(xhr.responseText);
            } else {
                if(failed){
                    failed(xhr.status);
                }
                else{
                    console.log("API调用异常。\n状态：" + xhr.status);
                }
            }
        }
    }
}

function myrefresh(){
    window.location.reload();
}

function success(response){
    document.getElementById("table").innerHTML = "<thead> \
                                                <tr> \
                                                <th data-field=\"state\" data-checkbox=\"true\"></th> \
                                                <th data-field=\"customID\">customID</th> \
                                                <th data-field=\"customPhone\">customPhone</th> \
                                                <th data-field=\"customAddress\">customAddress</th> \
                                                <th data-field=\"customName\">customName</th> \
                                                <th data-field=\"relName\">relName</th> \
                                                <th data-field=\"relPhone\">relPhone</th> \
                                                <th data-field=\"relEmail\">relEmail</th> \
                                                <th data-field=\"relRelation\">relRelation</th> \
                                                </tr>"  +
                                                "</thead>"

    var newJson = []
    response = JSON.parse(response);
    newJson = response["data"];
    console.log("newJson: "+ newJson)

    $("#table").bootstrapTable({
        data: newJson,
    })
}


function click_remove(){
    var $table = $('#table')
    var $remove = $('#remove')

    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.customID;
    })
    var url="http://localhost:8000/api/v1/APICustomer"
    for(var i = 0; i < ids.length; i ++){
        console.log(url+ids[i]);
        console.log(typeof ids[i])
        Ajax('DELETE', url+"/"+ids[i], '', success, console.log);
    }

    console.log("click success!")
    myrefresh();
}

function click_add(){
    window.open("add_Client.html", "newwindow", 
                "height=400, width=400, top=0, left=0, \
                toolbar=no, menubar=no, scrollbars=no, \
                resizable=no, location=no, status=no");   
    
}

// TODO：change

function success_all_accounts(response){
    document.getElementById("table").innerHTML = "<thead> \
    <tr> \
    <th data-field=\"state\" data-checkbox=\"true\"></th> \
    <th data-field=\"loanIDX\">loanIDX</th> \
    <th data-field=\"staf_staffID\">staf_staffID</th> \
    <th data-field=\"bran_branchName\">bran_branchName</th> \
    <th data-field=\"loanDate\">loanDate</th> \
    <th data-field=\"loanAmount\">loanAmount</th> \
    <th data-field=\"loanStatus\">loanStatus</th> \
    <th data-field=\"loanPaid\">loanPaid</th> \
    </tr>"  +
    "</thead>"
    var newJson0 = [];
    var newJson1 = [];
    response = JSON.parse(response);
    newJson0 = response["data"][0];
    console.log(JSON.stringify(newJson0));
    newJson1 = response["data"][1];
    console.log(JSON.stringify(newJson1));

    if(newJson0.length > 0){
        document.getElementById("table").innerHTML = "<thead> \
        <tr> \
        <th data-field=\"state\" data-checkbox=\"true\"></th> \
        <th data-field=\"accountIDX\">accountIDX</th> \
        <th data-field=\"bran_branchName\">bran_branchName</th> \
        <th data-field=\"staf_staffID\">staf_staffID</th> \
        <th data-field=\"remain\">remain</th> \
        <th data-field=\"visitTime\">visitTime</th> \
        <th data-field=\"openTime\">openTime</th> \
        <th data-field=\"accountType\">accountType</th> \
        <th data-field=\"cusA_accountIDX\">cusA_accountIDX</th> \
        <th data-field=\"currency\">currency</th> \
        <th data-field=\"interest\">interest</th> \
        </tr>"  +
        "</thead>";
        $("#table").bootstrapTable({
            data: newJson0,
        })
    }

    if(newJson1.length > 0){
        document.getElementById("neg_table").innerHTML = "<thead> \
        <tr> \
        <th data-field=\"state\" data-checkbox=\"true\"></th> \
        <th data-field=\"accountIDX\">accountIDX</th> \
        <th data-field=\"bran_branchName\">bran_branchName</th> \
        <th data-field=\"staf_staffID\">staf_staffID</th> \
        <th data-field=\"remain\">remain</th> \
        <th data-field=\"visitTime\">visitTime</th> \
        <th data-field=\"openTime\">openTime</th> \
        <th data-field=\"accountType\">accountType</th> \
        <th data-field=\"cusA_accountIDX\">cusA_accountIDX</th> \
        <th data-field=\"neg_limit\">neg_limit</th> \
        </tr>"  +
        "</thead>";
        $("#neg_table").bootstrapTable({
            data: newJson1,
        })
    }
}


function listAllAccounts(){
    var $table = $('#table')
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.customID;
    })
    var url="http://localhost:8000/api/v1/APICustomer"
    $('#table').bootstrapTable('destroy');
    for(var i = 0; i < ids.length; i ++){
        console.log(url + "/" + ids[i]);
        Ajax('GET', url + "/" + ids[i] + "/CusAccount", '', success_all_accounts, console.log);
    }
}

function success_all_loans(response){
    document.getElementById("table").innerHTML = "<thead> \
    <tr> \
    <th data-field=\"state\" data-checkbox=\"true\"></th> \
    <th data-field=\"loanIDX\">loanIDX</th> \
    <th data-field=\"staf_staffID\">staf_staffID</th> \
    <th data-field=\"bran_branchName\">bran_branchName</th> \
    <th data-field=\"loanDate\">loanDate</th> \
    <th data-field=\"loanAmount\">loanAmount</th> \
    <th data-field=\"loanStatus\">loanStatus</th> \
    <th data-field=\"loanPaid\">loanPaid</th> \
    </tr>"  +
    "</thead>"

    var newJson = []
    response = JSON.parse(response);
    newJson = response["data"];
    console.log("newJson: "+ newJson)

    $("#table").bootstrapTable({
        data: newJson,
    })
}

function listAllLoans(){
    var $table = $('#table');
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.customID;
    })
    $('#table').bootstrapTable('destroy');
    var url="http://localhost:8000/api/v1/APICustomer"
    if(ids.length == 0){
        Ajax('GET', url, '', success, alert);
    }
    for(var i = 0; i < ids.length; i ++){
        console.log(url + "/" + ids[i]);
        Ajax('GET', url + "/" + ids[i] + "Loan", '', success_all_loans, console.log);
    }
}

function query(queryArray){
    $('#table').bootstrapTable('destroy');
    var queryString = "?";
    var isNull = true;
    for(var i = 0; i < queryArray.length; i ++){
        var queryVar = document.getElementById(queryArray[i]);
        if(queryVar == null){
            queryString += queryArray[i] + "=" 
        }
        else {
            isNull = false;
            queryString += queryArray[i] +"="+ queryVar.value;
        }
        console.log(queryString);
        queryString += "&";
    }

    var url = "http://localhost:8000/api/v1/APICustomer";
    if(isNull){
        myrefresh();
    }
    else{
        Ajax('GET', url+queryString, '', success, console.log);
    }
}

function generate_query(queryArray){
  $(function(){
    for(var i = 0; i < queryArray.length; i++){
        console.log(queryArray[i]);
        document.getElementById("search_content").innerHTML += queryArray[i] +": "+"<input type=\"text\" id=" + "\"" + queryArray[i] +"\"> ";
        if((i+1) % 3 == 0){
            document.getElementById("search_content").innerHTML += "<br>"
        }
    }
    document.getElementById("search_content").innerHTML += "<button id=\"search\" class=\"btn btn-large btn-primary\" onclick=query(queryArray)>Search</button>"
  })
}

function searchByCustomerID(){
    $('#table').bootstrapTable('destroy');
    var searchByID = document.getElementById('searchByID');
    var url = "http://localhost:8000/api/v1/APICustomer";
    console.log(searchByID);
    if(searchByID == null){
        Ajax('GET', url, '', success, console.log);
    }
    else{
        Ajax('GET', url + '/' + searchByID.value, '',success, console.log);
    }
}

function myrefresh(){
    window.location.reload();
}

function click_change(){
    var ids = $.map($('#table').bootstrapTable('getSelections'), function(row){
        return  row.customID;
    })
    var phones = $.map($('#table').bootstrapTable('getSelections'), function(row){
        return  row.customPhone;
    })
    var addresses =  $.map($('#table').bootstrapTable('getSelections'), function(row){
        return  row.customAddress;
    })
    var url = "http://localhost:8000/api/v1/APICustomer";
    for(var i = 0; i < ids.length ;i ++){
        var customPhone = prompt("输入客户手机号");
        var customAddress = prompt("输入客户地址");
        if(customPhone == null || customPhone == ""){
            customPhone = phones[i];
        }
        if(customAddress == null || customAddress == ""){
            customAddress = addresses[i];
        }
        var data = 'field=customPhone&field=customAddress&field_value='+customPhone+"&field_value="+ customAddress;
        console.log(data);
        Ajax('PUT', url +"/" + ids[i], data, console.log, console.log);
    }
    myrefresh();
}

