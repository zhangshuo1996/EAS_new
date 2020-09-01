let institution_patent_chart = getEChartsObject("institution-patent-pie");


get_institution_patent_num(school);
/*
获取各学院的专利数量
 */

function get_institution_patent_num(school){
    $.ajax({
        type: "get",
        url: "/profile/get_institution_patent_num",
        data: {"school": school},
        dataType: "json",
        success: function (json_data) {
            let institutions = json_data["institutions"];
            debugger
            data = json_data["series"];
            configure_angle_picture(institutions, data);
            getInstitutionRelation(school, institutions[institutions.length - 1]);
        }

    })
}

/*
配置极坐标下的柱状图
 */
function configure_angle_picture(institutions, data) {
    let option = {
        title: {
            text: '',
        },
        legend: {
            show: false,
            data: ['成果数量']
        },
        grid: {
            top: 100
        },
        angleAxis: {
            type: 'category',
            data: institutions
        },
        tooltip: {
            show: true,
            formatter: function (params) {
                let id = params.dataIndex;
                return "点击查看该学院专家的社区" + "<br>" + institutions[id] + '<br>成果数量：' + data[id][2];
            }
        },
        radar: {
            axisLine: {
                // show: false
            },
            splitLine: {
                show: false
            }
        },
        radiusAxis: { },
        polar: { },
        series: [{
            type: 'bar',
            itemStyle: {
                color: '#2c7be5'
            },
            data: data.map(function (d) {
                return d[0];
            }),
            coordinateSystem: 'polar',
            stack: '最大最小值',
            silent: true,

        }, {
            type: 'bar',
            itemStyle: {
                color: function(params) {
                    let colorList = [
                        "#c23531",
                        "#2f4554",
                        "#61a0a8",
                        "#d48265",
                        "#91c7ae",
                        "#749f83",
                        "#ca8622",
                        "#bda29a",
                        "#6e7074",
                        "#546570",
                        "#c4ccd3",
                        "#4BABDE",
                        "#FFDE76",
                        "#E43C59",
                        "#37A2DA"
                    ];
                    return colorList[params.dataIndex];
                }
            },
            data: data.map(function (d) {
                return d[1] - d[0];
            }),
            coordinateSystem: 'polar',
            name: '价格范围',
            stack: '最大最小值'
        }]
};


    institution_patent_chart.clear();
    institution_patent_chart.hideLoading();
    institution_patent_chart.setOption(option);
}


/*
极坐标系下的柱状图点击事件
 */
institution_patent_chart.on('click', function (params) {
    let institution = params.name;
    getInstitutionRelation(school, institution);
});

