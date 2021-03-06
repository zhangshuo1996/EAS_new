let institution_relationship_chart = echarts.init(document.getElementById('institution_graph'));
let INSTITUTION_NAME = "";
let radar_chart = getEChartsObject("radar_graph");
let team_id_dict = {}; // 序号： team_id
let data2 = {
    community: 6,
    core_node: {
        1: "汪鹏", 2: "罗军舟", 3: "李必信", 4: "舒华忠", 5: "杨鹏", 6: "耿新"
    },
    links: [
       {source: "150837", target: "150855", paper: 0, patent: 2, project: 0},
       {source: "150876", target: "150837", paper: 0, patent: 0, project: 1},
       {source: "150894", target: "150837", paper: 0, patent: 0, project: 1},
       {source: "150865", target: "150837", paper: 0, patent: 0, project: 1},
       {source: "150885", target: "150837", paper: 0, patent: 0, project: 2},
       {source: "150922", target: "150837", paper: 0, patent: 2, project: 3},
       {source: "150838", target: "150901", paper: 0, patent: 0, project: 6},
       {source: "150840", target: "150838", paper: 0, patent: 0, project: 4},
       {source: "150908", target: "150838", paper: 0, patent: 0, project: 2},
       {source: "150921", target: "150838", paper: 0, patent: 0, project: 6},
    ],
    nodes: [
        {name: "150855", label: "罗军舟", category: 2, draggable: true, symbolSize: 26},
        {name: "150837", label: "沈典", category: 2, draggable: true, symbolSize: 14},
        {name: "150876", label: "单冯", category: 2, draggable: true, symbolSize: 16},
        {name: "150894", label: "金嘉晖", category: 2, draggable: true, symbolSize: 15},
        {name: "150865", label: "熊润群", category: 2, draggable: true, symbolSize: 17},
        {name: "150885", label: "吴巍炜", category: 2, draggable: true, symbolSize: 15},
        {name: "150922", label: "东方", category: 2, draggable: true, symbolSize: 18},
        {name: "150901", label: "漆桂林", category: 1, draggable: true, symbolSize: 13},
        {name: "150838", label: "张祥", category: 1, draggable: true, symbolSize: 13},
        {name: "150840", label: "高志强", category: 1, draggable: true, symbolSize: 11},
        {name: "150908", label: "姚莉", category: 6, draggable: true, symbolSize: 14},
        {name: "150921", label: "汪鹏", category: 1, draggable: true, symbolSize: 15,},
        {name: "150856", label: "李慧颖", category: 1, draggable: true, symbolSize: 10},
        {name: "150863", label: "吴含前", category: 6, draggable: true, symbolSize: 8},
        {name: "150910", label: "廖力", category: 3, draggable: true, symbolSize: 17},
        {name: "150839", label: "王璐璐", category: 3, draggable: true, symbolSize: 17},
        {name: "150897", label: "孔祥龙", category: 3, draggable: true, symbolSize: 17},
        {name: "150889", label: "蒋嶷川", category: 1, draggable: true, symbolSize: 11},
        {name: "150882", label: "倪巍伟", category: 6, draggable: true, symbolSize: 8},
        {name: "150867", label: "周晓宇", category: 1, draggable: true, symbolSize: 10},
        {name: "150900", label: "李必信", category: 3, draggable: true, symbolSize: 27,},
        {name: "150847", label: "张志政", category: 1, draggable: true, symbolSize: 15},
        {name: "150857", label: "王岩冰", category: 1, draggable: true, symbolSize: 10},
        {name: "150928", label: "舒华忠", category: 4, draggable: true, symbolSize: 26,},
        {name: "150841", label: "唐慧", category: 4, draggable: true, symbolSize: 12}
    ]

};



/*
获取学院的内部关系数据，并重新加载关系图
by zhang
 */
function getInstitutionRelation(school, institution){
    institution_relationship_chart.showLoading();
    $("#institution_name").html(institution + "专家团队");
    $.ajax({
        type: "get",
        url: "/profile/getInstitutionRelation",
        data: {"school": school, "institution": institution},
        dataType: "json",
        success: function (json_data) {
            let graph_data = convert_graph_data(json_data);
            reloadGraph(graph_data);
        }
    })
}

/*
转换关系图数据
 */
function convert_graph_data(data) {
    let temp_links = data.links;
    let temp_nodes = data.nodes;
    let links = [];
    let nodes = [];
    let team_set = new Set();
    let have_push_links_set = new Set();
    for(let i = 0; i < temp_links.length; i++){
        let source = String(temp_links[i]["source"]);
        let target = String(temp_links[i]["target"]);
        let s1 = source + "--" + target;
        let s2 = target + "--" + source;
        if(have_push_links_set.has(s1) || have_push_links_set.has(s2)){
            continue;
        }else{
            have_push_links_set.add(s1);
            have_push_links_set.add(s2);
        }
        links.push({
            source: source,
            target: target,
            paper:0,
            patent:0,
            project:0,
        });
    }
    let name_set = new Set();
    for(let i = 0; i < temp_nodes.length; i++){
        if(name_set.has(temp_nodes[i]["name"])){
            continue;
        }
        name_set.add(temp_nodes[i]["name"]);
        nodes.push({
            name: String(temp_nodes[i]["id"]),
            label: temp_nodes[i]["name"],
            category: temp_nodes[i]["team"],
            draggable: true,
            symbolSize: 26
        });
        team_set.add(String(temp_nodes[i]["team"]));
    }

    let team_map = {};
    let index = 0;
    for(let team_id of team_set){
        let team_leader = get_team_principle(team_id, temp_nodes);
        if(team_leader == undefined){
            continue;
        }
        team_map[index] = team_leader;
        team_id_dict[team_id] = index++;
    }
    for(let i = 0; i < nodes.length; i++){
        let team_id = nodes[i]["category"];
        nodes[i]["team_id"] = team_id;
        nodes[i]["category"] = team_id_dict[team_id];
    }
    return {
        community: index,
        core_node: team_map,
        links: links,
        nodes: nodes,
        team_set: team_set
    };
}

/**
 * 根据 team_id 获取这个团队的首脑人物
 * @param team_id
 * @param nodes
 * @returns {string|*}
 */
function get_team_principle(team_id, nodes) {
    for(let i = 0; i < nodes.length; i++){
        if(team_id == nodes[i]["id"]){
            return nodes[i]["name"];
        }
    }
    return undefined;
}


//关系图属性
let graphOption = {
    tooltip: {
        formatter: function (params) {
            if (params.dataType === "node") {
                let shcool = params.data.school === undefined? school: params.data.school,
                    institution = params.data.institution === undefined? INSTITUTION_NAME: params.data.institution;

                //设置提示框的内容和格式 节点和边都显示name属性
                return `<strong>节点属性</strong><hr>姓名：${params.data.label}<br>所属学校：${shcool}<br>所属学院：${institution}`;
            }
            else{
                if(params.data.visited){
                    return  `<strong>关系属性</strong><hr>拜访次数：${params.data.visited}次<br>参与活动：${params.data.activity}`;
                }
                return `<strong>关系属性</strong><hr>
                论文合作：${params.data.paper}次<br>专利合作：${params.data.patent}次<br>项目合作：${params.data.project}次<br>`;
            }
        }
    },
    // 图例
    legend: [],
    animation: true,
    series : [
        {
            type: 'graph',
            layout: 'force',
            data: [],
            links: [],
            categories: [],
            // // 边的长度范围
            // edgeLength: [10, 50],
            //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            roam: true,
            // 当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            // focusNodeAdjacency:true,
            // 是否启用图例 hover(悬停) 时的联动高亮。
            legendHoverLink : true,
            label: {
                normal: {
                    position: 'inside',
                    show : true,

                    //回调函数，显示用户名
                    formatter: function(params){
                        return params.data.label;
                    }
                }
            },
            force: {
                repulsion : [20,100],//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                gravity : 0.05,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                edgeLength :[20,100],//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
                layoutAnimation : true
            },

            lineStyle: {
                show : true,
                color: 'target',//决定边的颜色是与起点相同还是与终点相同
                curveness: 0.1//边的曲度，支持从 0 到 1 的值，值越大曲度越大。
            }
        }
    ]
};

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
    [10, 10, 10, 10, 10]
);

/**
 * 设置并加载雷达图
 * @param dimension
 * @param data
 */
function set_radar_option(dimension, data, teacher_name="点击右图节点查看科研水平评估") {
    $("#radar_graph_header").html(teacher_name + "团队科研水平评估");
    let option = {
        title: {
            // text: '多雷达图'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            left: 'center',
            data: ['分布']
        },
        radar: [
            {},
            {
                indicator: dimension,
                radius: 100,
                center: ['50%', '60%'],
            }
        ],
        series: [
            {
                type: 'radar',
                radarIndex: 1,
                areaStyle: {},
                data: [
                    {
                        value: data,
                        name: '某主食手机'
                    }
                ]
            }
        ]
    };
    radar_chart.clear();
    radar_chart.hideLoading();
    radar_chart.setOption(option);
}

/**
 * 重新加载关系图数据，把数据赋值给graphOption中的data
 * @param data 关系图数据
 */
function reloadGraph(data){
    if(!"nodes" in data) return;
    let links = data.links;
    graphOption.series[0].data = data.nodes;
    graphOption.series[0].links = links;
    let categories = [];
    categories[0] = {name: ''};
    for (let i = 0; i < data.community; i++) {
        debugger
        categories[i] = {
            name: data.core_node[String(i)]+"团队"
        };
    }
    graphOption.series[0].categories = categories;
    graphOption.legend = [{
        data: categories.map(function (a) {
            return a.name;
        })
    }];
    institution_relationship_chart.setOption(graphOption);
    institution_relationship_chart.hideLoading();
}

/**
 * 关系图上的点 点击事件
 */
institution_relationship_chart.on('click', function (params) {
    //仅限节点类型
    if (params.dataType === 'node' && params.data.name !== "0"){
        //页面
        debugger;
        let team_id = params.data.team_id;
        // 获取这个team_id的各维度数据，构建雷达图
        get_team_dimension_info(team_id);
    }
});

/**
 * 获取团队的各维度信息，用于更新雷达图
 */
function get_team_dimension_info(team_id) {

    $.ajax({
        type: "get",
        url: "/profile/get_team_dimension_info",
        data: {"team_id": team_id, "school": school},
        dataType: "json",
        success: function (json_data) {
            debugger
            // 更新雷达图
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
                json_data["teacher_name"]
        );
        }
    })
}
