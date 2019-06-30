
var domCheque = document.getElementById("chequecanvas");
var myChartCheque = echarts.init(domCheque);
var appCheque = {};

appCheque.title = '支票业务统计';

function setChequeData(timenames, counts, remains){

    var colors = ['#d14a61', '#675bba'];
    option = null;
    option = {
        color: colors,

        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        grid: {
            right: '20%'
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data:['总资产','开户数']
        },
        xAxis: [
            {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                data: timenames
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '总信用账户金额',
                min: 0,
                //max: ,
                position: 'right',
                offset: 0,
                axisLine: {
                    lineStyle: {
                        color: colors[0]
                    }
                },
                axisLabel: {
                    formatter: '￥{value}'
                }
            },
            {
                type: 'value',
                name: '账户数',
                min: 0,
                //max: 100,
                position: 'left',
                axisLine: {
                    lineStyle: {
                        color: colors[1]
                    }
                },
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name:'总信用账户金额',
                type:'bar',
                yAxisIndex: 0,
                data: remains
            },
            {
                name:'账户数',
                type:'line',
                yAxisIndex: 1,
                data:counts
            }
        ]
    };
    ;
    if (option && typeof option === "object") {
        myChartCheque.setOption(option, true);
    }
}
