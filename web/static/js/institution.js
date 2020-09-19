let institution_relation_chart = getEChartsObject("institution-relation");
let institution_radar_chart = getEChartsObject("institution-radar");
let team_id_dict = {}; // 序号： team_id
let data = undefined;  // 后端传过来的关系原始数据
let expert_id = undefined;
let show_type = 2;  // show_type == 1：社区关系图， == 2 联系图

show_community_relation();
get_institution_dimension_info(school, institution);

/**
 * 复选框选择
 */
$(".visit_status").on("click", function () {
    if(expert_id === undefined){
        return ;
    }
    // 清除所有的复选框
    let check_box_arr = $(".visit_status");
    for(let i = 0; i < check_box_arr.length; i++){
        let check_box = $(check_box_arr[i]);
        check_box.prop("checked", false);
    }
    // 渲染点击的复选框
    let visit_status = $(this).val();
    $(this).prop("checked", true);
    // 更新后端的数据TODO:
    $.ajax({
        type: "get",
        url: "/profile/update_node_visit_status",
        data: {"teacher_id": expert_id, "visit_status": visit_status},
        dataType: "json",
        success: function () {
            // 重新渲染联系图
            data = undefined;
            show_link_relation();
        }
    })

});

/**
 * 点击关系图中的节点, 显示该专家的访问状态
 */
institution_relation_chart.on("click", function (params) {
    if(show_type === 1){
        return;
    }
    expert_id = params.data.name;  // 专家id
    let expert_name = params.data.label;  // 专家姓名
    let visit_status = params.data.visit_status;  // 访问状态
    // 请求该老师的拜访状态
    let check_box_arr = $(".visit_status");
    for(let i = 0; i < check_box_arr.length; i++){
        let check_box = $(check_box_arr[i]);
        check_box.prop("checked", false);
    }
    // 渲染该状态对应的复选框
    $(check_box_arr[visit_status]).prop("checked", true);
    //
    $("#expert_name").html(expert_name);
    $("#visit_status_modal").modal();
});

/**
 * 点击显示社区关系图
 */
$("#institution-graph").on("click", function () {
    show_type = 1;
    institution_relation_chart.clear();
    show_community_relation();
});

/**
 * 点击显示联系图
 */
$("#link-graph").on("click", function () {
    show_type = 2;
    institution_relation_chart.clear();
    show_link_relation();
});

/**
 * 显示社区关系图
 */
function show_community_relation() {
    if(data === undefined){ // 如果关系数据未定义，请求关系数据
        get_institution_relation(1);
    }else{  // 如果关系数据已定义，直接使用
        let graph_data = convert_graph_data(data, 1);
        reloadGraph(graph_data, "force", 1);
    }
}


/**
 * 显示联系图
 */
function show_link_relation() {
    if(data === undefined){
        get_institution_relation(2);
    }else{
        let graph_data = convert_graph_data(data, 2);
        reloadGraph(graph_data, "force", 2);
    }
}


/**
 * 获取学院内部的关系数据
 */
function get_institution_relation() {
    institution_relation_chart.showLoading();
    $.ajax({
        type: "get",
        url: "/profile/get_institution_relation",
        data: {"school": school, "institution": institution},
        dataType: "json",
        success: function (json_data) {
            data = json_data;
            let graph_data = convert_graph_data(json_data);
            reloadGraph(graph_data, "force");
            return true;
        }
    })
}


/**
 * 获取学院 内部的各维度打分
 */
function get_institution_dimension_info(school, institution) {
    $.ajax({
        type: "get",
        url: "/profile/get_institution_dimension_info",
        data: {"school": school, "institution": institution},
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
                institution_radar_chart,
            );
        }
    })
}


/**
 * 转换关系图数据
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
    let normal_style = {};

    for(let i = 0; i < temp_nodes.length; i++){
        if(name_set.has(temp_nodes[i]["name"])){
            continue;
        }
        name_set.add(temp_nodes[i]["name"]);
        let category = undefined;
        if(show_type === 1){
            nodes.push({
                name: String(temp_nodes[i]["id"]),
                school: school,
                institution: temp_nodes[i]["institution"],
                label: temp_nodes[i]["name"],
                category: temp_nodes[i]["team"],
                patent: temp_nodes[i]["patent"],
                visit_status: temp_nodes[i]["visit_status"],
                draggable: true,
                symbolSize: get_node_size(temp_nodes[i]["patent"]),
                itemStyle: {
                    normal: normal_style,
                }
            });
        }else{
            let visit_status = temp_nodes[i]["visit_status"];
            let visit_status_color = {0: '#2c7be5', 1: '#e6550d', 2: '#31a354', 3: '#756bb1', 4: '#636363'};
            category = visit_status;
            normal_style = {
                color: visit_status_color[visit_status],
            };
            nodes.push({
                name: String(temp_nodes[i]["id"]),
                school: school,
                institution: temp_nodes[i]["institution"],
                label: temp_nodes[i]["name"],
                category: category,
                patent: temp_nodes[i]["patent"],
                visit_status: temp_nodes[i]["visit_status"],
                draggable: true,
                symbolSize: get_node_size(temp_nodes[i]["patent"]),
                itemStyle: {
                    normal: normal_style,
                }
            });

        }

        team_set.add(String(temp_nodes[i]["team"]));
    }
    let team_map = {};
    let index = 0;
    for(let team_id of team_set){
        let team_leader = get_team_principle(team_id, temp_nodes);
        if(team_leader === undefined){
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
            layout: 'circular',
            data: [],
            links: [],
            categories: [],
            // // 边的长度范围
            // edgeLength: [10, 50],
            //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            roam: true,
            // 当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            focusNodeAdjacency:false,
            // 是否启用图例 hover(悬停) 时的联动高亮。
            legendHoverLink : true,
            circular: {
                rotateLabel: true
            },
            label: {
                normal: {
                    show : true,
                    position: 'insideBottomRight',
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
            itemStyle:{
                borderColor: '#fff',
                borderWidth: 1,
                shadowBlur: 10,
                shadowColor: 'rgba(10, 10, 10, 0.3)',
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
 * 重新加载关系图数据，把数据赋值给graphOption中的data
 * @param data 关系图数据
 */
function reloadGraph(data, layout="circular"){
    if(!"nodes" in data) return;
    let links = data.links;
    graphOption.series[0].data = data.nodes;
    graphOption.series[0].links = links;
    let categories = [];
    if(show_type === 1){
        categories[0] = {name: ''};
        for (let i = 0; i < data.community; i++) {
            categories[i] = {
                name: data.core_node[String(i)] + "团队"
            };
        }
    }else{
        categories = [{name: "未联系过"},{name: "联系过"},{name: "做过活动"},{name: "签过合同"},{name: "创业"}]
    }
    graphOption.series[0].layout = layout;
    graphOption.series[0].categories = categories;
    if(show_type === 1){  // 社区关系图才显示图例
        graphOption.legend = [{
            x: 'right',
            y: 'center',
            padding:[5, 30, 5, 10],
            orient: 'vertical',
            data: categories.map(function (a) {
                return a.name;
            })
        }];
    }else{
        graphOption.color = ['#2c7be5','#e6550d', '#31a354', '#756bb1', '#636363'];
        graphOption.legend = [{
            x: 'right',
            y: 'center',
            padding:[5, 30, 5, 10],
            orient: 'vertical',
            data: ["未联系过","联系过","做过活动","签过合同","创业"]
        }];
    }
    institution_relation_chart.clear();
    institution_relation_chart.setOption(graphOption);
    institution_relation_chart.hideLoading();
}


/**
 * 根据专利的数量 返回专家节点的大小
 *
 */
function get_node_size(patent_num) {
    if(patent_num < 5){
        return 10;
    }
    if(patent_num < 10){
        return 15;
    }
    if(patent_num < 20){
        return 20;
    }
    if(patent_num < 30){
        return 25;
    }else{
        return 30;
    }
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
