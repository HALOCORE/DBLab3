var url = "http://localhost:8000/api/v1/APIBranch";
var response;


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
                alert("success");
                alert(typeof xhr.responseText)
                success(xhr.responseText);
            } 
            else {
                if(failed){
                    alert("failed")
                    failed(xhr.status);
                    failed(xhr.responseText);
                }
                else{
                    alert("API调用异常。\n状态：" + xhr.status);
                }
            }
        }
        // else if(xhr.status == 400){
        //     alert("400")
        //     alert(xhr.responseText);
        // }
    }
}

function myrefresh(){
    window.location.reload();
}

function success(response){
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
        return  row.branchName;
    })
    // $table.bootstrapTable('remove', {
    //     field: 'branchName',
    //     values: ids
    // })
    alert(ids);
    var url="http://localhost:8000/api/v1/APIBranch"
    for(var i = 0; i < ids.length; i ++){
        alert(url+"/"+ids[i]);
        alert(typeof ids[i]) 
        Ajax('DELETE', url+"/"+ids[i], '', alert, alert);
    }
    // $('#table').bootstrapTable('destroy');
    // Ajax('GET', url, '', success, alert);
    myrefresh();
}

function click_add(){
    var city = prompt("输入city", "Hefei");
    alert(city);
    var branchName = prompt("输入支行名", "AHB"); 
    alert(branchName)
    var data = '{ '+"\"city\":" + "\""+city + "\""+ ", " + "\"branchName\":" + "\"" + branchName + "\"" + ' }';
    alert(data);
    alert(typeof data);
    var obj = JSON.parse(data);
    alert("obj: " + obj);
    console.log(obj);
    var url="http://localhost:8000/api/v1/APIBranch"
    Ajax('POST', url, obj, alert, alert);

    // $('#table').bootstrapTable('destroy');
    // Ajax('GET', url, '', success, alert);
    alert("add successfully!")

    myrefresh();
}

function click_change(){
    var $table = $('#table')
    var ids = $.map($table.bootstrapTable('getSelections'), function(row){
        return  row.branchName;
    })
    alert(ids);
    var url="http://localhost:8000/api/v1/APIBranch/"
    for(var i = 0; i < ids.length; i ++){
        alert(url+ids[i]);
        var city = prompt("输入修改后的city");
        var data = '{' + "\"field\"" + ":" + "[" + "\'city\'" + "]" + ", " + 
                    "\"field_value\"" + ":" + "[" + "\'" + city + "\'" + "]" +
                    '}'
        alert(data);
        // var obj = JSON.parse(data);
        // console.log(obj);
        Ajax("PUT", url+ids[i], data, alert, alert);
    }
}



function searchByBranchName(){
    var url="http://localhost:8000/api/v1/APIBranch"
    $('#table').bootstrapTable('destroy');
    var searchContent = document.getElementById("searchContent");
    if(searchContent.value){
        Ajax('GET', url+"/"+searchContent.value, '', success, alert);
    }
    else{
        Ajax('GET', url, '', success, alert);
    }
}







