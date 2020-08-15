
let school_num_pie = getEChartsObject("school-pie");

let data = {
    "legend": ["东南大学", "南京航空航天大学", "武汉大学", "浙江大学", "上海大学", "同济大学", "北京理工大学"],
    "series": [
        {"name": "东南大学", "value": 3},
        {"name": "南京航空航天大学", "value": 5},
        {"name": "武汉大学", "value": 2},
        {"name": "浙江大学", "value": 6},
        {"name": "上海大学", "value": 1},
        {"name": "同济大学", "value": 5},
        {"name": "北京理工大学", "value": 2},
    ],
    "seriesName": "学校数量占比"
};

set_pie_option(school_num_pie, pieOption, data);