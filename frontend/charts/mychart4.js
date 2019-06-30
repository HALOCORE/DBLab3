
var domLoan = document.getElementById("loancanvas");
var myChartLoan = echarts.init(domLoan);
var appLoan = {};

appLoan.title = '贷款业务统计';

function setLoanData(timenames, counts, amounts, pays){

    option = null;
    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data:['贷款总额','支付总额','开户数']
        },
        xAxis: [
            {
                type: 'category',
                data: timenames,
                axisPointer: {
                    type: 'shadow'
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '金额',
                min: 0,
                // max: 250,
                // interval: 50,
                axisLabel: {
                    formatter: '￥{value}'
                }
            },
            {
                type: 'value',
                name: '开户数',
                min: 0,
                // max: 25,
                // interval: 5,
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name:'贷款总额',
                type:'bar',
                data:amounts
            },
            {
                name:'支付总额',
                type:'bar',
                data:pays
            },
            {
                name:'开户数',
                type:'line',
                yAxisIndex: 1,
                data:counts
            }
        ]
    };
    ;
    if (option && typeof option === "object") {
        myChartLoan.setOption(option, true);
    }
}
