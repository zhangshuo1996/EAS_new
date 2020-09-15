let data = transport.data;
let team_list = data["team_list"];
let teacher_basic_info = data["teacher_basic_info"];
let patent_info = data["patent_info"];
// let school_proportion = data["school_proportion"];
let old_input_key = transport.input_key;
let team_radar_chart = getEChartsObject('team-radar');
let index=0; // 搜索结果显示第几页



// let school_num_pie = getEChartsObject("school-pie");

$(document).ready(function() {
    // $(".show_content ul li").next("ul").hide();
    $(".show_content ul li").click(function() {
        $(this).next("ul").toggle();
    });
    fill_input();
});

/*
填充搜索框中的搜索内容
 */
function fill_input(){
    $("#input_key").val(old_input_key);
}

/**
 * 鼠标悬浮时左右箭头变大
 */
$(".move-page").mouseover(function () {
    $(this).attr("style", "font-size: 3rem");
});

$(".move-page").mouseleave(function () {
    $(this).attr("style", "font-size: 2rem");
});


/**
 * 鼠标点击下载界面
 */
$("#search_outcome").on("click", "#download_page", function () {
   download_page();
});
let result;
function download_page(){
    $("#fill_data").val(index);
    let sub = document.getElementById('submit_download');
    sub.click();
}


/**
 *鼠标点击箭头时更换页面
 */
$("#next_page").on("click", function () {
    let cur_index = index;
    index = cur_index + 1;
    if(index >= team_list.length-1){
        //"已经是最后一个团队"
    }
    let team_id = team_list[index]["team_id"];
    let institution = team_list[index]["institution"];
    insert_search_outcome();
     // 更新雷达图
    get_team_dimension_info(team_id);
    // 更新关系图
    getTeamRelation(team_id, institution);
});


$("#last_page").on("click", function () {
    let cur_index = index;
    index = cur_index - 1;
    if(index < 0){
        //"已经是最后一个团队"
    }
    let team_id = team_list[index]["team_id"];
    let institution = team_list[index]["institution"];
    insert_search_outcome();
     // 更新雷达图
    get_team_dimension_info(team_id);
    // 更新关系图
    getTeamRelation(team_id, institution);
});

/**
 * 团队人员点击事件，用于更新右侧的雷达图和关系图
 *
 */
$("#search_outcome").on("click", ".expert", function () {
    let team_id = $(this).data("id");
    let institution = $(this).data("institution");
    // 更新雷达图
    get_team_dimension_info(team_id);
    // 更新关系图
    getTeamRelation(team_id, institution);

});


insert_search_outcome();


/*
将搜索结果 页面
 */
function insert_search_outcome() {
    let html = [];
    // for(let i = 0; i < team_list.length; i++){
    let school = team_list[index]["school"];
    let institution = team_list[index]["institution"];
    let lab = team_list[index]["lab"];
    let member_id_list = team_list[index]["member_id_list"];
    let patent_id_list = team_list[index]["patent_id_list"];
    let project_list = team_list[index]["project_list"];
    let row_data = `
        <div class="card">
                <div class="card-header">
                    <div class="card-header-title">
                    `;

    row_data += `
    
                    <span class="expert"><span class="fe fe-users" style="font-size: 2rem"></span>
    `;
    for(let j = 0; j < member_id_list.length; j++){
        if(j > 5){
            break;
        }
        let teacher_info = teacher_basic_info[member_id_list[j]];
        let teacher_name = teacher_info["name"];
        row_data += `<span class="expert" style="margin: 1px; padding: 1px" data-id="${team_list[index]["team_id"]}" data-institution="${team_list[index]["institution"]}">${teacher_name}</span></span>`
    }
    row_data += `
        </div>
        <span class="school">
            <div class="avatar" style="height: 40px; width: 40px">
                <img style="height: 40px; width: 40px" src="/search/avatar/${school}">
            </div>
            <span style="margin-left: 1px">
                <a href="/profile/${school}">${school}</a>
            </span>
        </span>
    `;

    if(institution !== ""){
        row_data += `<span class="institution"><span class="fe fe-home"></span> ${institution}</span>`;
    }
    if(lab !== ""){
        row_data += `<span class="fe fe-box" style="margin-left: 1px; margin-right: 1px"></span><span> ${lab}</span>`;
    }

    row_data += `
        <span class="fe fe-arrow-down" id="download_page" title="保存结果为pdf" style="font-size: 1rem"></span>
        </div>
                <div class="card-body" style="">
                    <div class="row" style="">
                        <div class="col-md-9 show_content">
                            <ul style="list-style-type: none;">
                                <li><span class="fe fe-align-center"></span><a href="###">专利成果</a> <span class="badge badge-pill badge-primary">${patent_id_list.length}</span></li>
                                <ul>
    `;
    for(let j = 0; j < patent_id_list.length; j++){
        let index = j + 1;
        row_data += `<li> ${index}. ${patent_info[patent_id_list[j]][0]}[${patent_info[patent_id_list[j]][1]}]</li>`;
        // row_data += `${index}. ${patent_info[patent_id_list[j]]}`;
    }
    row_data += `
        </ul>
                            </ul>
                            <ul style="list-style-type: none;">
                                <li ><span class="fe fe-align-center"></span><a href="###">相关项目</a> <span class="badge badge-pill badge-success">${project_list.length}</span></li>
                                <ul>
    `;
    for(let j = 0; j < project_list.length; j++){
        row_data += `<li>${project_list[j]}</li>`;
    }
    row_data += `
                
                                
                                </ul>
                            </ul>
                        </div>
                        <div class="col-md-2 relation-pic"></div>
                        <div class="col-md-1"></div>
                    </div>
                    <div class="similar-patent"></div>
                </div>
            </div>
    
    `;

    html.push(row_data);
    // }

    let innerHtml = html.join("");
    $("#search_outcome").html(innerHtml);

    // 显示搜索结果中第一个团队的雷达图与关系图
    get_team_dimension_info(team_list[index]["team_id"]);
    getTeamRelation(team_list[index]["team_id"], team_list[index]["institution"])
}

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

            // 更新雷达图
            set_radar_option(
             [
                        {text: '研究人员水平', max: 100},
                        {text: '研究人员数量', max: 100},
                        {text: '学校水平（985,211）', max: 100},
                        {text: '实验平台', max: 100},
                        {text: '成果数量', max: 100},
                        {text: '项目数量', max: 100},
                    ],
            [
                json_data["researcher_level_score"],
                json_data["researcher_num_score"],
                json_data["school_level_score"],
                json_data["lab_score"],
                json_data["achieve_num"],
                json_data["project_score"]
            ],
                team_radar_chart,
        );
            let leader = json_data["leader"];
            $("#radar_graph_header").html(leader + "团队科研水平评估");
        }
    })
}