var url = "http://localhost:8000/api/v1/APIStaff/";

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
                alert("success");
                alert(typeof xhr.responseText)
                success(xhr.responseText);
            } else {
                if(failed){
                    failed(xhr.status);
                }
                else{
                    alert("API调用异常。\n状态：" + xhr.status);
                }
            }
        }
    }
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
        return  row.staffID;
    })
    $table.bootstrapTable('remove', {
        field: 'staffID',
        values: ids
    })
    alert(ids);
    // var url="http://localhost:8000/api/v1/APICustomer/"
    // for(var i = 0; i < ids.length; i ++){
    //     alert(url+ids[i]);
    //     alert(typeof ids[i])
    //     Ajax('DELETE', url+ids[i], '', success, alert);
    // }
    // // 此时会有API调用异常，状态：0
    // alert("click success!")
}

function click_add(){
    window.open("add_Staff.html", "newwindow", 
                "height=400, width=800, top=0, left=0, \
                toolbar=no, menubar=no, scrollbars=no, \
                resizable=no, location=no, status=no");   
}

