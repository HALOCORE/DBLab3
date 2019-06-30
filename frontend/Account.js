var cheque_url = "http://localhost:8000/api/v1/APIAccount/Cheque"
var deposit_url = "http://localhost:8000/api/v1/APIAccount/Deposit"

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
            xhr.open('DELETE', url + data, true);
            
        } else{
            xhr.open('DELETE', url, true);
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
                    console.log("failed")
                    failed(xhr.responseText);
                }
                else{
                    console.log("API调用异常。\n状态：" + xhr.status);
                }
            }
        }
    }
}

function success(response){
    var newJson = []
    response = JSON.parse(response);
    newJson = response["data"];
    console.log("newJson: "+ newJson)

    $("#table").bootstrapTable({
        data: newJson,
    })
}

function myrefresh(){
    window.location.reload();
}

function click_remove_deposit(url){
    var $table = $('#table')
    var $remove = $('#remove')

    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.accountIDX;
    })
    for(var i = 0; i < ids.length; i ++){
        console.log(url+ids[i]);
        console.log(typeof ids[i])
        Ajax('DELETE', url+"/"+ids[i], '', success, alert);
    }

    console.log("click success!")
    // myrefresh();
}

function searchByAccountID(url){
    $('#table').bootstrapTable('destroy');
    var searchByID = document.getElementById('searchByID');
    console.log(searchByID.value);
    if(searchByID == null || searchByID.value == ""){
        myrefresh();
    }
    else{
        Ajax('GET', url + '/' + searchByID.value, '',success, console.log);
    }
}

function generate_query(queryArray, url){
    $(function(){
      for(var i = 0; i < queryArray.length; i++){
          console.log(queryArray[i]);
          document.getElementById("search_content").innerHTML += queryArray[i] +": "+"<input type=\"text\" id=" + "\"" + queryArray[i] +"\"> ";
          if((i+1) % 3 == 0){
              document.getElementById("search_content").innerHTML += "<br>"
          }
      }
      document.getElementById("search_content").innerHTML += "<button id=\"search\" class=\"btn btn-large btn-primary\" onclick=query(queryArray,\""+url+"\")>Search</button>"
    })
  }
  
function query(queryArray, url){
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
    if(isNull){
        myrefresh();
    }
    else{
        Ajax('GET', url+queryString, '', success, console.log);
    }
}

function accountCustomer(url){
    var ids = $.map($('#table').bootstrapTable('getSelections'), function(row){
        return  row.accountIDX;
    })
    if(ids.length == 0){
        Ajax('GET', url, '', success, alert);
    }
    $('#table').bootstrapTable('destroy');
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

    for(var i = 0; i < ids.length; i ++){
        console.log(url+"/"+ids[i]);
        console.log(typeof ids[i])
        Ajax('GET', url + "/" + ids[i] + "/Customer", '', success, alert);
    }

}
function click_add_account_to_customer(url){
// {"status": "error", "describe": "可能是参数缺失造成参数字典KeyError. 'cust_customID'"}
    var ids = $.map($('#table').bootstrapTable('getSelections'), function(row){
        return  row.accountIDX;
    })
    if(ids.length == 0){
        Ajax('GET', url, '', success, alert);
    }
    $('#table').bootstrapTable('destroy');

    for(var i = 0; i < ids.length; i ++){
        var custom_ID = prompt("input customer ID: ");
        var data = "{" + "\"cust_customID\":" + "\""+ custom_ID + "\"" +"}";
        console.log(data);
        Ajax('POST', url + "/"+ ids[i], data, success, console.log);
    }
    console.log("click_add_account_to_customer");
}

function click_add_deposit(){
    window.open("add_Deposit.html","newwindow", 
    "height=400, width=400, top=0, left=0, \
    toolbar=no, menubar=no, scrollbars=no, \
    resizable=no, location=no, status=no" )
}

function click_add_cheque(){
    window.open("add_Cheque.html","newwindow", 
    "height=400, width=400, top=0, left=0, \
    toolbar=no, menubar=no, scrollbars=no, \
    resizable=no, location=no, status=no" )
}

function click_change_deposit(){
    var ids = $.map($('#table').bootstrapTable('getSelections'), function(row){
        return  row.accountIDX;
    })
    var deposit_url = "http://localhost:8000/api/v1/APIAccount/Deposit"
    for(var i = 0; i < ids.length; i ++){
        var remain_change = prompt("输入变更储蓄的金额");
        var data = '{' +  "\"field\":[\"cust_customID\", \"remain_change\"]," +
                    "\"field_value\":[" + ids[i] + "," + "\"" +remain_change +"\"" +"]";
        var obj = JSON.parse(data);
        Ajax('PUT', deposit_url + "/" + ids[i], obj, console.log, console.log);
    }
}