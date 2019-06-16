
var url = "http://localhost:8000/api/v1/APIBranch/";
/*
var invocation = new XMLHttpRequest();
var data;
function getJson(url){
  if(invocation){
    invocation.onreadystatechange = state_Change;   
    invocation.open('GET', url, true);
    // invocation.withCredentials = true;
    invocation.send();
  }
}
function state_Change(){
  if(invocation.readyState == 4){
    alert(invocation.status);
    alert(invocation.responseText);
    if(invocation.status == 200){
      alert("200");
      alert("test"+invocation.responseText);
      data = invocation.responseText;
     }
    else {
      alert(invocation.status);
      alert("Problem retrieving XML data");
    }
  }
}

getJson(url);
var oldJson = JSON.parse(data);

function generateNewJson(oldJson){
  var newJson = [];
  // for(var i = 0; i < oldJson["data"].length; i ++){
  //   // string.city = oldJson["data"][i].city;
  //   // string.branchName = oldJson["data"][i].branchName;
  //   // console.log(string);
  //   newJson.push(oldJson["data"][i]);
  // }
  newJson = oldJson["data"]
  console.log(newJson);
  console.log(typeof(newJson));
  return newJson;
}

var newJson = generateNewJson(oldJson);
alert("newJson = " + newJson);
var $table = $('#table')

$(function(){
  // var data =  [{"city": "Tokyo", "branchName": "AAA"}, {"city": "Hefei", "branchName": "AHB"}, {"city": "Beijing", "branchName": "BJB"}, {"city": "Shanghai", "branchName": "SHB"}]

  $table.bootstrapTable({data: newJson})
})
*/

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
            xhr.open('GET', url + '?t=' + random, true);
        }
        xhr.send();
 
    } else if(type == 'POST'){
        xhr.open('POST', url, true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(data);
    }
 
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4){
            if(xhr.status == 200){
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





