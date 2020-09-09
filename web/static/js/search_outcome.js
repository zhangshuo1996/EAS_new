let data = transport.data;
let team_list = data["team_list"];
let teacher_basic_info = data["teacher_basic_info"];
let patent_info = data["patent_info"];
// let school_proportion = data["school_proportion"];
let old_input_key = transport.input_key;
let team_radar_chart = getEChartsObject('team-radar');


// let school_num_pie = getEChartsObject("school-pie");

$(document).ready(function() {
    $(".show_content ul li").next("ul").hide();
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
 * 团队人员点击事件，用于更新右侧的雷达图和关系图
 *
 */
$("#search_outcome").on("click", ".expert", function () {
    let team_id = $(this).data("id");
    let institution = $(this).data("institution");
    // 更新雷达图
    get_team_dimension_info(team_id);
    // TODO：更新关系图
    getTeamRelation(team_id, institution);

});

// set_pie_option(school_num_pie, pieOption, school_proportion);

insert_search_outcome();
/*
将搜索结果 页面
 */
function insert_search_outcome() {
    let html = [];
    for(let i = 0; i < team_list.length; i++){
        let school = team_list[i]["school"];
        let institution = team_list[i]["institution"];
        let lab = team_list[i]["lab"];
        let member_id_list = team_list[i]["member_id_list"];
        let patent_id_list = team_list[i]["patent_id_list"];
        let project_list = team_list[i]["project_list"];
        let row_data = `
            <div class="card">
                    <div class="card-header">
                        <div class="card-header-title">
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
        </div>
                        <span class="lab"><span class="fe fe-users"></span>
        `;
        for(let j = 0; j < member_id_list.length; j++){
            if(j > 5){
                break;
            }
            let teacher_info = teacher_basic_info[member_id_list[j]];
            let teacher_name = teacher_info["name"];
            row_data += `<span class="expert" style="margin: 1px; padding: 1px" data-id="${team_list[i]["team_id"]}" data-institution="${team_list[i]["institution"]}">${teacher_name}</span></span>`
        }
        row_data += `
            </div>
                    <div class="card-body" style="">
                        <div class="row" style="">
                            <div class="col-md-9 show_content">
                                <ul style="list-style-type: none;">
                                    <li><span class="fe fe-align-center"></span><a href="###">相似成果</a> <span class="badge badge-pill badge-primary">${patent_id_list.length}</span></li>
                                    <ul>
        `;
        for(let j = 0; j < patent_id_list.length; j++){
            let index = j + 1;
            row_data += `<li> ${index}. ${patent_info[patent_id_list[j]]}</li>`;
            row_data += `<!--<li> ${index}. ${patent_info[patent_id_list[j]]}<span class="badge-light">相似度：95%</span></li>-->`;
        }
        row_data += `
            </ul>
                                </ul>
                                <ul style="list-style-type: none;">
                                    <li ><span class="fe fe-align-center"></span><a href="###">相关项目</a> <span class="badge badge-pill badge-success">${project_list.length}</span></li>
                                    <ul>
        `;
        for(let j = 0; j < project_list.length; j++){
            row_data += `<li><a href="#">${project_list[j]}</a></li>`;
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
    }

    let innerHtml = html.join("");
    $("#search_outcome").html(innerHtml);

    // 显示搜索结果中第一个团队的雷达图与关系图
    get_team_dimension_info(team_list[0]["team_id"]);
    getTeamRelation(team_list[0]["team_id"], team_list[0]["institution"])
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
                    ],
            [
                json_data["researcher_level_score"],
                json_data["researcher_num_score"],
                json_data["school_level_score"],
                json_data["lab_score"],
                json_data["achieve_num"],
            ],
                team_radar_chart,
        );
        }
    })
}