import Chart from "./chart.js";
console.log("institution.js");
var dataset = transport.outcome_list;
var discipline = transport.discipline;
var nums_list = [] // 成果数量列表
console.log(dataset)


var school_list = [];
var data_processed = []; //已处理过的数据
get_school_patent();
console.log(school_list);
console.log(data_processed);

var title = discipline + "排名靠前的高校成果数量对比"
//-------------------------------
var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            color: ['#c23531','#2f4554', '#61a0a8'],
            title: {
                text: title
            },
            tooltip: {},
            legend: {
                data:['成果数量']
            },
            xAxis: {
                data: school_list
            },
            yAxis: {},
            series: [{
                name: '成果数量',
                type: 'bar',
                data: nums_list,
                itemStyle: {
                        normal: {
                            color: function(params) {
                                var colorList = ["#3398db", "#434348", "#90ed7d", "#f7a35c", "#61a0a8", "#61a0a8", "#91c7ae", "#2f4554",'#c23531','#2f4554', '#61a0a8'];
                                return colorList[params.dataIndex]
                            }
                        }
                    },
                    label: {
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);

//-------------------------------


/*
从给定的数据中获取学校列表和成果列表
*/
function get_school_patent(){
    for(var i = 0; i < dataset.length; i++){
            var school = dataset[i].x;
            var patent_nums = dataset[i].y;
            if(school_list.indexOf(school) == -1){
                school_list.push(school);
                data_processed.push({
                    "x": school,
                    "y": patent_nums,
                })
            }else{
                var cur = school_list.indexOf(school);
                console.log(data_processed);
                console.log(cur);
                patent_nums += data_processed[cur].y;
                data_processed[cur].y = patent_nums;
            }
        }
        data_processed = data_processed.sort(compare("y"));
        school_list = []
        for(var i = 0; i < data_processed.length; i++){
            school_list.push(data_processed[i].x);
            nums_list.push(data_processed[i].y);
        }

}
/*
对数组[
        {x:**, y: 1},
        {x:**, y: 2},
        {x:**, y: 3},
        ...
     ]
按y降序排序
*/
function compare(property){
    return function(a, b){
        var v1 = a[property];
        var v2 = b[property];
        return v2 - v1;
    }
}