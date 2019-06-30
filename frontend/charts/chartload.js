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

Ajax('GET', 'http://localhost:8000/api/v1/APIBranch', null, 
    function(branch_data){
        //console.log(branch_data);
        var bdata = JSON.parse(branch_data)["data"];
        var branches = [];
        var bsel = document.getElementById("branchsel");
        //bsel.c
        for(var v in bdata){
            var bname = bdata[v]["branchName"];
            bsel.options.add(new Option(bname, bname));
        }
        $('#branchsel').selectpicker('refresh');

        Ajax('GET', 'http://localhost:8000/api/v1/APIStatistic/Deposit', null,
            function(dep_data){
                var ddata = JSON.parse(dep_data);
                var rem = ddata["data"]["remain_sum"];
                var count = ddata["data"]["count_account"];
                var rem_total = 0;
                var cnt_total = 0;
                var rmb_total = 0;
                for(var i in rem){
                    rem_total += rem[i]["sum_remain"];
                    if(rem[i]["currency"] == "RMB"){
                        rmb_total += rem[i]["sum_remain"];
                    }
                }
                for(var i in count){
                    cnt_total += count[i]["count_cusAccount"];
                }
                var db1 = document.getElementById("dep_board_1");
                db1.innerText = "￥" + rem_total;
                var db2 = document.getElementById("dep_board_2");
                db2.innerHTML = db2.innerHTML.replace('(rep)', rmb_total);
                var db3 = document.getElementById("dep_board_3");
                db3.innerHTML = db3.innerHTML.replace('(rep)', cnt_total);

                Ajax('GET', 'http://localhost:8000/api/v1/APIStatistic/Cheque', null,
                    function(che_data){
                        var ddata = JSON.parse(che_data);
                        var rem = ddata["data"]["remain_sum"];
                        var count = ddata["data"]["count_account"];
                        var rem_total = 0;
                        var cnt_total = 0;
                        for(var i in rem){
                            rem_total += rem[i]["sum_remain"];
                        }
                        for(var i in count){
                            cnt_total += count[i]["count_cusAccount"];
                        }
                        var db1 = document.getElementById("che_board_1");
                        db1.innerText = "￥" + rem_total;
                        var db2 = document.getElementById("che_board_2");
                        db2.innerHTML = db2.innerHTML.replace('(rep)', rem_total);
                        var db3 = document.getElementById("che_board_3");
                        db3.innerHTML = db3.innerHTML.replace('(rep)', cnt_total);

                        Ajax('GET', 'http://localhost:8000/api/v1/APIStatistic/Loan', null,
                            function(loan_data){
                                var ddata = JSON.parse(loan_data);
                                var rem = ddata["data"]["loan_sum"];
                                var count = ddata["data"]["loan_count"];
                                var pay = ddata["data"]["paid_sum"];
                                var rem_total = 0;
                                var pay_total = 0;
                                var cnt_total = 0;
                                for(var i in rem){
                                    rem_total += rem[i]["sum_loanAmount"];
                                }
                                for(var i in pay){
                                    pay_total += pay[i]["sum_loanPaid"];
                                }
                                for(var i in count){
                                    cnt_total += count[i]["count_loan"];
                                }
                                var db1 = document.getElementById("loan_board_1");
                                db1.innerText = "￥" + rem_total;
                                var db2 = document.getElementById("loan_board_2");
                                db2.innerHTML = db2.innerHTML.replace('(rep)', pay_total);
                                var db3 = document.getElementById("loan_board_3");
                                db3.innerHTML = db3.innerHTML.replace('(rep)', cnt_total);
                            }
                        );
                    }
                );

            }
        );
    }
);
