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

function parse_depdata(depdata){
    var ddata = depdata;
    if(typeof ddata == "string") ddata = JSON.parse(ddata);
    var remda = ddata["data"]["remain_sum"];
    var count = ddata["data"]["count_account"];
    var rem_total = 0;
    var cnt_total = 0;
    var rmb_total = 0;
    var currency_total ={};
    for(var i in remda){
        var rem = remda[i]["sum_remain"];
        var currency = remda[i]["currency"];

        rem_total += rem;

        if(currency == "RMB"){
            rmb_total += rem;
        }
        if(currency in currency_total){
            currency_total[currency] += rem;
        }
        else{
            currency_total[currency] = 0;
        }
    }
    for(var i in count){
        cnt_total += count[i]["count_cusAccount"];
    }
    return {
        "rem_total": rem_total, 
        "rmb_total":rmb_total, 
        "cnt_total":cnt_total,
        "currency_total": currency_total
    };
}

function parse_chedata(chedata){
    var ddata = chedata;
    if(typeof ddata == "string") ddata = JSON.parse(ddata);
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
    return {"rem_total": rem_total, "cnt_total":cnt_total};
}

function parse_loandata(loandata){
    var ddata = loandata;
    if(typeof ddata == "string") ddata = JSON.parse(ddata);
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
    return {"loan_total": rem_total, "pay_total":pay_total, "cnt_total":cnt_total};
}

function updatePart(part){
    //alert("将开始拉取统计.");
    console.log(" ====== updatePart ======");
    var selbranch = document.getElementById("branchsel");
    var sellevel = document.getElementById("levelsel");
    var seldatestart = document.getElementById("startdatesel");
    var seldateend = document.getElementById("enddatesel");
    var branch = selbranch.value;
    var level = sellevel.value;
    var datestart = seldatestart.value;
    var dateend = seldateend.value;
    if(level && datestart && dateend && datestart != dateend){
        var month_start = parseInt(datestart.split('/')[0]);
        var year_start = parseInt(datestart.split('/')[2]);
        var month_end = parseInt(dateend.split('/')[0]);
        var year_end = parseInt(dateend.split('/')[2]);
        
        var time_seq = [];
        var name_seq = [];

        console.log("开始更新chart...");

        function genquery(part, idx){
            var prefix = "openTime";
            if(part == "Loan") prefix = "loanDate";
            var qstr = "http://localhost:8000/api/v1/APIStatistic/"
                     + part + "?bran_branchName=" + branch + "&" 
                     + prefix + "from=" + time_seq[idx] + "&"
                     + prefix + "to=" + time_seq[idx+1];
            return qstr;
        }

        function query_a_part(part){
            var results = [];
            for(var i=0; i<name_seq.length; i++){
                var qurl = genquery(part, i);
                console.log(qurl);
                var result;
                $.ajax({
                    url : qurl,
                    async : false,
                    success: function(data){
                        console.log("得到一个结果.");
                        result = data;
                    }
                });
                results.push(result);
            }
            return results;
        }
        
        if(level == "月"){
            alert("不支持.");
        }
        if(level == "季度"){
            for(var curyear=year_start; curyear <= year_end; curyear++){
                if(curyear != year_end){
                    time_seq.push(curyear + "-01-01");
                    name_seq.push(curyear + "春");
                    time_seq.push(curyear + "-04-01");
                    name_seq.push(curyear + "夏");
                    time_seq.push(curyear + "-07-01");
                    name_seq.push(curyear + "秋");
                    time_seq.push(curyear + "-10-01");
                    name_seq.push(curyear + "冬");
                }
                else{
                    time_seq.push(curyear + "-01-01");
                }
                
            }
        }
        if(level == "年"){
            for(var curyear=year_start; curyear <= year_end; curyear++){
                if(curyear != year_end) name_seq.push(curyear);
                time_seq.push(curyear + "-01-01");
            }
        }
        
        if(part == "Deposit"){
            var dep_data_results = query_a_part("Deposit");
            var count_line = [];
            var rem_line = [];
            for(var i in dep_data_results){
                var pdata = parse_depdata(dep_data_results[i]);
                count_line.push(pdata.cnt_total);
                rem_line.push(pdata.rem_total);
            }
            setDepositData(name_seq, count_line, rem_line);
        }
        if(part == "Cheque"){
            var che_data_results = query_a_part("Cheque");
            var count_line = [];
            var rem_line = [];
            for(var i in che_data_results){
                var pdata = parse_chedata(che_data_results[i]);
                count_line.push(pdata.cnt_total);
                rem_line.push(pdata.rem_total);
            }
            setChequeData(name_seq, count_line, rem_line);
        }
        
        if(part == "Loan"){
            var loan_data_results = query_a_part("Loan");
            var count_line = [];
            var loan_line = [];
            var pay_line = [];
            for(var i in loan_data_results){
                var pdata = parse_loandata(loan_data_results[i]);
                count_line.push(pdata.cnt_total);
                loan_line.push(pdata.loan_total);
                pay_line.push(pdata.pay_total);
            }
            setLoanData(name_seq, count_line, loan_line, pay_line);
        }
    }
    

}

function onBranchChange(){
    console.log("branch change");
    var selbranch = document.getElementById("branchsel");
    var branchName = selbranch.value;

    Ajax('GET', 'http://localhost:8000/api/v1/APIStatistic/Deposit?bran_branchName=' + branchName, null,
        function(dep_data){
            var ddata = parse_depdata(dep_data);
            
            var db1 = document.getElementById("brdep_board_1");
            db1.innerText = "￥" + ddata.rem_total;
            var db2 = document.getElementById("brdep_board_2");
            db2.innerText = ddata.rmb_total;
            var db3 = document.getElementById("brdep_board_3");
            db3.innerText = ddata.cnt_total;

            var bycur = ddata.currency_total;
            var asdatas = [];
            for(var cur in bycur){
                asdatas.push({name:cur,value:bycur[cur]});
            }
            setAssetData(asdatas);

            Ajax('GET', 'http://localhost:8000/api/v1/APIStatistic/Cheque?bran_branchName=' + branchName, null,
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
                    var db1 = document.getElementById("brche_board_1");
                    db1.innerText = "￥" + rem_total;
                    var db2 = document.getElementById("brche_board_2");
                    db2.innerText = rem_total;
                    var db3 = document.getElementById("brche_board_3");
                    db3.innerText = cnt_total;

                    Ajax('GET', 'http://localhost:8000/api/v1/APIStatistic/Loan?bran_branchName=' + branchName, null,
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
                            var db1 = document.getElementById("brloan_board_1");
                            db1.innerText = "￥" + rem_total;
                            var db2 = document.getElementById("brloan_board_2");
                            db2.innerText = pay_total;
                            var db3 = document.getElementById("brloan_board_3");
                            db3.innerText = cnt_total;
                        }
                    );
                }
            );

        }
    );
}