var url = "http://localhost:8000/api/v1/APILoan";



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
                    failed(xhr.status);
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
    document.getElementById("table").innerHTML =  "<thead> \
    <tr> \
    <th data-field=\"state\" data-checkbox=\"true\"></th> \
    <th data-field=\"loanIDX\">loanIDX</th>" + 
    "<th data-field=\"staf_staffID\">staf_staffID</th> \
    <th data-field=\"bran_branchName\">bran_branchName</th>\
    <th data-field=\"loanDate\">loanDate</th>\
    <th data-field=\"loanAmount\">loanAmount</th>\
    <th data-field=\"loanStatus\">loanStatus</th>\
    <th data-field=\"\loanPaid\">loanPaid</th>\
    </tr>" +
    "</thead>"
    var $table = $('#table')
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
        return  row.loanIDX;
    })
    console.log(ids);
    var url="http://localhost:8000/api/v1/APILoan"
    for(var i = 0; i < ids.length; i ++){
        console.log(url+ids[i]);
        console.log(typeof ids[i])
        Ajax('DELETE', url+"/"+ids[i], '', success, alert);
    }
    // 此时会有API调用异常，状态：0
    console.log("click success!")
    myrefresh();
}

function click_add(){
    window.open("add_Loan.html", "newwindow", 
                "height=400, width=800, top=0, left=0, \
                toolbar=no, menubar=no, scrollbars=no, \
                resizable=no, location=no, status=no");   
}

// TODO：change

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


function query(queryArray){
    $('#table').bootstrapTable('destroy');
    var queryString = "?";
    var isNull = true;
    for(var i = 0; i < queryArray.length; i ++){
        var queryVar = document.getElementById(queryArray[i]);
        if(queryVar == null || queryVar.value == ""){
            continue;
        }
        else {
            isNull = false;
            queryString += queryArray[i] +"="+ queryVar.value.trim();
            queryString += "&";
        }
        console.log(queryString);
        
    }
    var url = "http://localhost:8000/api/v1/APILoan";
    console.log(queryString)
    if(isNull){
        myrefresh();
    }
    else{
        Ajax('GET', url+queryString, '', success, console.log);
    }
}

function success_get_customer(response){
    document.getElementById("modalTable").innerHTML = "<thead> \
    <tr> \
    <th data-field=\"state\" data-checkbox=\"true\"></th> \
    <th data-field=\"customPhone\">customPhone</th> \
    <th data-field=\"customAddress\">customAddress</th> \
    <th data-field=\"customName\">customName</th> \
    <th data-field=\"relName\">relName</th> \
    <th data-field=\"relPhone\">relPhone</th> \
    <th data-field=\"relRelation\">relRelation</th> \
    </tr>"  +
    "</thead>";

    var newJson = []
    response = JSON.parse(response);
    newJson = response["data"];
    console.log("newJson: "+ newJson)

    $("#modalTable").bootstrapTable({
        data: newJson
    })
}

function getCustomer(){
    var url = "http://localhost:8000/api/v1/APILoan";
    var $table = $('#table')
    var $remove = $('#remove')
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.loanIDX;
    })
    $("#modalTable").bootstrapTable('destroy');
    $("#modalNegTable").bootstrapTable('destroy');
    $('#myModal').modal('toggle');
    for(var i = 0; i < ids.length; i ++){
        console.log(url + "/" + ids[i]);
        Ajax('GET', url + "/" + ids[i] + "/Customer", '', success_get_customer, console.log);
    }
}

function searchByLoanID(){
    $('#table').bootstrapTable('destroy');
    var searchByID = document.getElementById('searchByID');
    var url = "http://localhost:8000/api/v1/APILoan";
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

function success_get_payRecord(response){
    document.getElementById("modalTable").innerHTML = "<thead> \
    <tr> \
    <th data-field=\"state\" data-checkbox=\"true\"></th> \
    <th data-field=\"loan_loanIDX\">loan_loanIDX</th> \
    <th data-field=\"loanPayDate\">loanPayDate</th> \
    <th data-field=\"loanPayAmount\">loanPayAmount</th> \
    </tr>"  +
    "</thead>";
    var newJson = []
    response = JSON.parse(response);
    newJson = response["data"];
    console.log("newJson: "+ newJson)

    $("#modalTable").bootstrapTable({
        data: newJson
    })
}


function getPayRecord(){
    var url = "http://localhost:8000/api/v1/APILoan";
    var $table = $('#table')
    var $remove = $('#remove')
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.loanIDX;
    })
    $("#modalTable").bootstrapTable('destroy');
    $("#modalNegTable").bootstrapTable('destroy');
    $('#myModal').modal('toggle');
    for(var i = 0; i < ids.length; i ++){
        console.log(url + "/" + ids[i]);
        Ajax('GET', url + "/" + ids[i] + "/Pay", '', success_get_payRecord, console.log);
    }
}

function addCustomer(){
    var url = "http://localhost:8000/api/v1/APILoan";
    var $table = $('#table')
    var $remove = $('#remove')
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.loanIDX;
    })
    for(var i = 0; i < ids.length; i ++){
        var cust_customID = prompt("输入要添加的客户ID");
        var data = '{' + "\"cust_customID\"" + ":" + 
        "\""+ cust_customID + "\"" + 
        '}'
        console.log(data);
        var obj = JSON.parse(data);
        Ajax('POST', url + "/" + ids[i], obj, console.log, console.log);
    }
}

function currentTime(){
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    month = month < 10 ? ("0" + month) : month;
    day = day < 10 ? ("0" + day) : day;
    var Timer = year + '-' + month + '-' + day ;
    return  Timer;
}
    
function payLoan(){
    var url = "http://localhost:8000/api/v1/APILoan";
    var $table = $('#table')
    var $remove = $('#remove')
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.loanIDX;
    })
    for(var i = 0; i < ids.length; i ++){
        var time = currentTime();
        var loanPayAmount = prompt("输入于时间"+time+"的还款额");
        var data = '{' + "\"" + "loanPayDate" + "\":" +"\"" +time + "\"" + ","+ "\"" + "loanPayAmount"+"\"" +":" + loanPayAmount + '}'
        console.log(data);
        var obj = JSON.parse(data);
        Ajax('POST', url + "/" +ids[i] + "/" + "Pay", obj, console.log, alert);
        myrefresh();
    }
}

function click_change(){

}