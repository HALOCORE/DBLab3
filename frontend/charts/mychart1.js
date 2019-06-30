
var dom = document.getElementById("assetcanvas");

var myChart = echarts.init(dom);
var app = {};
option = null;
option = {
    backgroundColor: 'white',

    title: {
        text: '储蓄资产比例（分币种）',
        left: 'center',
        top: 20,
        textStyle: {
            color: '#333'
        }
    },

    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },

    visualMap: {
        show: false,
        min: 80,
        max: 600,
        inRange: {
            colorLightness: [0, 1]
        }
    },
    series : [
        {
            name:'访问来源',
            type:'pie',
            radius : '55%',
            center: ['50%', '50%'],
            data:[
                {value:335, name:'RMB'},
                {value:310, name:'SGD'},
                {value:274, name:'USD'},
                {value:235, name:'HKD'},
                {value:400, name:'BTC'}
            ].sort(function (a, b) { return a.value - b.value; }),
            roseType: 'radius',
            label: {
                normal: {
                    textStyle: {
                        color: 'rgba(50, 50, 50, 0.8)'
                    }
                }
            },
            labelLine: {
                normal: {
                    lineStyle: {
                        color: 'rgba(50, 50, 50, 0.8)'
                    },
                    smooth: 0.2,
                    length: 10,
                    length2: 20
                }
            },
            itemStyle: {
                normal: {
                    color: '#c23531',
                    shadowBlur: 60,
                    shadowColor: 'rgba(0, 0, 0, 0.3)'
                }
            },

            animationType: 'scale',
            animationEasing: 'elasticOut',
            animationDelay: function (idx) {
                return Math.random() * 200;
            }
        }
    ]
};

if (option && typeof option === "object") {
    myChart.setOption(option, true);
    
}
