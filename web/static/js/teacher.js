console.log("test teacher_js");
var teacher_net = transport.teacher_net;
var teacher_info = transport.teacher_info;
console.log(teacher_info)
var myChart = echarts.init(document.getElementById('main'), 'macarons');

transform_link(teacher_net.nodes, teacher_net.links);
var nodes_ = teacher_net.nodes;
var links_ = teacher_net.links;
console.log("00000000");
console.log(nodes_);
console.log(links_);
console.log("000000")
createGraph(myChart, teacher_net)



function getOption(teacher_net){
    var categories = ["0"];

    //设置option样式
    option = {
        title : {
            text:"",
            x:'middle',
            y:'bottom'
        },
        tooltip : { // 鼠标悬浮于节点之上时的提示框，
            trigger: 'item', // 数据触发类型
//            formatter: '{b}',
            formatter: function(params){
                return params.data.school + " : " + params.data.institution;
            },
    //        formatter: function(params){//触发之后返回的参数，这个函数是关键
    //        if (params.data.category !=undefined) //如果触发节点
    //           window.open("http://www.baidu.com")
    //        }
        },
        color:['#EE6A50','#4F94CD','#B3EE3A','#DAA520'],
        toolbox: { // 工具箱 ：每个图表最多一个
            show : false,
            feature : { // 启用功能
                //dataView数据视图，打开数据视图，可设置更多属性,readOnly 默认数据视图为只读(即值为true)，可指定readOnly为false打开编辑功能
                restore : {show: true}, // 还原， 复位原始图表
                magicType: {show: true, type: ['force', 'chord']}, // 动态类型转换 ？？
                saveAsImage : {show: true} // 保存图片
            }
        },
        // 图例， 每个图表最多有一个图例
//        legend: {
//            x: 'left', // 图例位置
//            //图例的名称，这里返回短名称，即不包含第一个，当然你也可以包含第一个，这样就可以在图例中选择主干人物
//            data: categories.map(function (a) {//显示策略
//                return a.name;
//            })
//        },
        // series 数据，用于设置图表数据
        series: [{
            type: 'graph',
            layout: 'force',

            label: {
                normal: {
                  show: true,
                  position: 'top',//设置label显示的位置
                  // formatter: '{c}',//设置label读取的值为value

                  textStyle: {
                    fontSize: '12rem'
                  },
                }
            },

             symbolSize: (value, params) => {
                console.log("+++++")
                console.log(value);
                console.log(params);
                return value;
              },
            draggable: true,
            data: teacher_net.nodes,
            force: {
                edgeLength: 50,
                repulsion: 200,
                gravity: 0.1
            },
            links: teacher_net.links,
            itemStyle: {
                    borderColor: '#fff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.3)'
                },
            lineStyle: {
//                    color: 'source',
//                    curveness: 0.3,
                    normal: {
                        show: true,
                        color: 'target',
                        curveness: 0.3
                    }
                },
            emphasis: {
                    lineStyle: {
                        width: 10
                    }
                }
        }]
    };


    return option;
}
function createGraph(myChart, teacher_net){
    console.log("create graph")
    //设置option样式
    option=getOption(teacher_net)
    //使用Option填充图形
    myChart.setOption(option);
    //点可以跳转页面
    myChart.on('click', function (params) {
                var data=params.value
                //点没有source属性
                if(data.source==undefined){
                    nodeName=params.name
                    teacher_id = params.data.id2
//                    window.open(teacher_info["homepage"])
                    window.open("/teacher/" + teacher_id)
                    console.log("teacher_id" + teacher_id)
                }

    });
//    myChart.hideLoading();
}

function transform_link(nodes, links){
    id_name = {};
    for(var i = 0; i < nodes.length; i++){
        if(i == 0){
            nodes[i].category = 0;
        }else{
            nodes[i].category = 1;
        }
        id = nodes[i].id;
        name = nodes[i].name;
        nodes[i].id2 = nodes[i].id;
        nodes[i].label = nodes[i].school + " : " + nodes[i].institution;
        delete nodes[i].id;
//        delete nodes[i].code;
//        delete nodes[i].school;
//        delete nodes[i].institution;
        id_name[id] = name;
        delete nodes[i].name;
        nodes[i].name = id_name[id];
        if(35 - i*5 > 10){
            nodes[i].value = 35 - i*5;
        }else{
            nodes[i].value = 10;
        }

    }
    teacher_net.nodes = nodes;


    for(var i = 0; i < links.length; i++){
        var source_id = links[i].source;
        var target_id = links[i].target;
        links[i].source = id_name[source_id]
        links[i].target = id_name[target_id]
        links[i].label = links[i].value.paper + links[i].value.patent + links[i].value.project;
        delete links[i].value;

    }
    teacher_net.links = links;



}