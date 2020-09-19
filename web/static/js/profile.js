let institution_patent_chart = getEChartsObject("institution-patent-bar");
let school_radar_chart = getEChartsObject("school-radar");


/**
 * 加载雷达图
 */
set_radar_option(
     [
                {text: '研究人员水平', max: 100},
                {text: '研究人员数量', max: 100},
                {text: '学校水平（985,211）', max: 100},
                {text: '实验平台', max: 100},
                {text: '成果数量', max: 100},
            ],
    [10, 10, 10, 10, 10],
    school_radar_chart,
);


get_institution_patent_num(school);

get_school_normalize_dimension_score();


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
            data = {
                "series": {
                    "data": json_data["series"],
                    "type": 'bar',
                    "barWidth": 10
                },
            };
            barOption.yAxis.data = institutions;
            barOption.grid = {
                 left: '20px',
                 right: '20px',
                bottom: '1%',
                containLabel: true
            }
            set_option(institution_patent_chart, barOption, data);
        }
    })
}

/**
 * 获取学校归一化之后的各维度分数
 * @param school
 */
function get_school_normalize_dimension_score(school="东南大学") {
    $.ajax({
        type: "get",
        url: "/profile/get_school_normalize_dimension_score",
        data: {"school": school},
        dataType: "json",
        success: function (json_data) {
            set_radar_option(
                 [
                            {text: '研究人员水平', max: 100},
                            {text: '研究人员数量', max: 100},
                            {text: '学校水平（985,211）', max: 100},
                            {text: '实验平台', max: 100},
                            {text: '成果数量', max: 100},
                        ],
                [
                    json_data["researcher_level_score"],
                    json_data["researcher_num_score"],
                    json_data["school_level_score"],
                    json_data["lab_score"],
                    json_data["achieve_num"],
                ],
                school_radar_chart,
            );
        }
    })
}


/**
 * 柱状图点击事件, 跳转至学院画像
 */
institution_patent_chart.on("click", function (params) {
    let institution = params.name;
    window.location.href = "/profile/institution_profile/" + school + "/" + institution;
});


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
            top: 80
        },
        angleAxis: {
            type: 'category',
            data: institutions,
            axisTick: { //坐标轴刻度设置
        　　　　show: false
        　　},
        　　splitLine: { //分割线设置
        　　　　show: false,
        　　},
        },
        radius: 20,
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
    // getInstitutionRelation(school, institution);
});

