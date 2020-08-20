let data = transport.data;
let team_list = data["team_list"];
let teacher_basic_info = data["teacher_basic_info"];
let patent_info = data["patent_info"];
let school_proportion = data["school_proportion"];
let old_input_key = transport.input_key;
//搜索结果的返回类型
let search_type = transport.type;

// 当前选中的学校 包含在结果中的
let cur_outcome_list;
let patent_school_dict = {};
//默认学校列表选择是patent结果中的
let school_dict;
let currentPage; // 当前是第几页
let pageSize; // 每页显示的数量
let total; // 总共的数量
let pageNumber; //总共的页数



let school_num_pie = getEChartsObject("school-pie");

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

set_pie_option(school_num_pie, pieOption, school_proportion);

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
                                <div class="avatar" style="height: 25px; width: 25px">
                                    <img style="height: 25px; width: 25px" src="/search/avatar/${school}">
                                </div>${school}
                            </span>
                        `;
        if(institution !== ""){
            row_data += `<span class="institution"><span class="fe fe-home"></span> ${institution}</span>`;
        }
        if(lab !== ""){
            row_data += `<span class="fe fe-box"></span><span> ${lab}</span>`;
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
            debugger;
            let teacher_name = teacher_info["name"];
            row_data += `<span class="expert" style="margin: 1px; padding: 1px">${teacher_name}</span></span>`
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

}