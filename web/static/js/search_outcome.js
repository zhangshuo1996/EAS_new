// 选择的类型是论文还是专利， 默认是论文
// var outcome_paper_list = transport.outcome_paper_list;
var outcome_patent_list = transport.outcome_patent_list;
var input_key = transport.input_key;
//默认选择是paper
var outcome_list = outcome_patent_list;
//搜索结果的返回类型
var search_type = transport.type;
// 当前选中的学校 包含在结果中的
var cur_outcome_list = outcome_list;

var patent_school_dict = {};
extract_patent_school_list();
//默认学校列表选择是paper结果中的
var school_dict = patent_school_dict;
var currentPage = 1; // 当前是第几页
var pageSize = 6; // 每页显示的数量
var total = outcome_list.length; // 总共的数量
var pageNumber = parseInt(total / pageSize) + 1; //总共的页数
// 显示右侧边栏的学校
show_school(school_dict);
// 更新搜索结果内容
update_show_result();
document.getElementById("layui-laypage-count").innerHTML = "共" + total + "条";

fill_input();

/*
填充搜索框中的搜索内容
 */
function fill_input(){
    $("#input_key").val(input_key);
}

/*
提取出论文搜索结果中的学校列表
 */
// function extract_paper_school_list() {
//     for(let i = 0; i < outcome_paper_list.length; i++){
//         let school = outcome_paper_list[i]["basic_info"]["school"];
//         let school_id = outcome_paper_list[i]["basic_info"]["school_id"];
//         if(!paper_school_dict.hasOwnProperty(school_id)){
//             paper_school_dict[school_id] = school;
//         }
//     }
// }


/*
提取出专利搜索结果中的学校列表
 */
function extract_patent_school_list() {
    for(let i = 0; i < outcome_patent_list.length; i++){
        let school = outcome_patent_list[i]["basic_info"]["school"];
        let school_id = outcome_patent_list[i]["basic_info"]["school_id"];
        if(!patent_school_dict.hasOwnProperty(school_id)){
            patent_school_dict[school_id] = school;
        }
    }
}


/*
侧边显示高校
 */
function show_school(school_dict) {
    let html = [];
    html.push(`
            <label><input id="select_all" type="checkbox" value="全选" checked="true" />全选</label> 
        `);
    for(let school_id in school_dict){
        let row_data = `
            <label><input class="select_school" name="Fruit" type="checkbox" value="${school_id}" checked="true" />${school_dict[school_id]}</label> 
        `;
        html.push(row_data);
    }
    let innerString = html.join(`<br>`);
    document.getElementById("show_school").innerHTML = innerString;
}

/*
高校全选/全不选 点击事件
 */
$("#show_school").on("click", "#select_all", function () {
    let is_selected = $(this).is(":checked");
    if(is_selected){
        update_check_box(true);
    }else{
        update_check_box(false);
    }
    update_show_result();
});


/*
更新右边选择框全选或者全不选
 */
function update_check_box(val){
    let row_list = $("#show_school label .select_school");
    for(let i = 0; i < row_list.length; i++){
        let row = $(row_list[i]);
        row.prop("checked", val);
    }
}


/*
学校列表复选框点击事件
 */
$("#show_school label .select_school").on("change", function () {
    update_show_result();
});


/*
右侧边的学校更新时，调用该函数，用于更新显示搜索的结果
 */
function update_show_result() {
    let row_list = $("#show_school label .select_school");
    let select_school_id_list = [];
    // 首先选择 被选中的学校 id
    for(let i = 0; i < row_list.length; i++){
        let row = row_list[i];
        let selected = row.checked; // 该复选框是否被选中
        let school_id = row.value; // 复选框对应的学校id
        if(selected){
            select_school_id_list.push(school_id);
        }
    }
    // 显示的结果中 只有 用户目前选定的学校
    cur_outcome_list = [];
    for(let i = 0; i < outcome_list.length; i++){
        let school_id_str = outcome_list[i]["basic_info"]["school_id"].toString();
        let is_existed = select_school_id_list.indexOf(school_id_str) > -1;
        if(is_existed){
            cur_outcome_list.push(outcome_list[i]);
        }
    }
    total = cur_outcome_list.length; // 总共的数量
    pageNumber = parseInt(total / pageSize) + 1; //总共的页数
    document.getElementById("layui-laypage-count").innerHTML = "共" + total + "条";
    // 而后利用这些id更新 显示的学校列表， 只显示选择的学校
    inner_html(select_school_id_list);

}


/*
将换页后 页面最下方显示页码的部分更新
*/
function update_page_number(){
    var innerString = "";
    for(var i = 1; i <= pageNumber; i++){
        if(i == currentPage){
            innerString +=  "<div class=\"btn-group mr-2\" role=\"group\" aria-label=\"First group\">" +
                                "<button type=\"button\" class=\"btn btn-secondary\">" + i + "</button>" +
                             "</div>";
        }else{
            innerString += "<button type=\"button\" class=\"btn btn-secondary\">" + i + "</button>"
        }
    }
    document.getElementById("page_ctrl").innerHTML = innerString;
}

/*
将换页后的内容更新
*/
function inner_html(select_school_id_list){
    let html = [];

    console.log(outcome_list);
    for(let i = pageSize * (currentPage - 1); i < pageSize * (currentPage-1) + pageSize && i < total; i++){
        let outcome = cur_outcome_list[i];
        let index = i+1;
        if(search_type == "teacher"){
            let school_id_str = outcome["basic_info"]["school_id"].toString();
            let is_existed = select_school_id_list.indexOf(school_id_str) > -1;
            if(!is_existed){
                continue;
            }
            let row_data = `
                        <tr>
                            <th scope="row">${index}</th>
                            <td><a href="/school/${outcome["basic_info"]["school"]}">${outcome["basic_info"]["school"]}</a></td>
                            <td><a href="/institution/${outcome["basic_info"]["school"]}/${outcome["basic_info"]["institution"]}">${outcome["basic_info"]["institution"]}</a></td>
                            <td><a href="/teacher/${outcome["id"]}">${outcome["basic_info"]["name"]}</div></td>
                            <td>
                                <div class="accordion" id="accordionExample">
                                  
                                    <div class="card-header" id="headingOne">
                                      <h2 class="mb-0">
                                        <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapse${i}" aria-expanded="false" aria-controls="collapse${i}">
                                          相似成果数量：${outcome["achieve_nums"]}
                                        </button>
                                      </h2>
                                    </div>
                                    <div id="collapse${i}" class="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
                                      <div class="card-body">       
            `;
            html.push(row_data);

            let patent_list = outcome["patent_list"];
            for(let i = 0; i < patent_list.length; i++){
                let inner_data = `
                                <div class="ends" style="font-size:1vw;-webkit-transform-origin-x: 0;-webkit-transform: scale(0.90);">
                                    ${patent_list[i]["patent_name"]}
                                </div>
                `;
                html.push(inner_data);
            }
            let last_data = `
                                  
                                </div>
                              </div>
                            </div>
                        </td>          
                    </tr>
            `;
            html.push(last_data);

        }
        else if(search_type == "institution"){
            if(!(outcome["basic_info"]["school_id"] in select_school_id_list)){
                continue;
            }
            //TODO： 更新前端的显示样式
            let row_data = `<button type="button" class="list-group-item list-group-item-action">
                            <div><a href="/school/${outcome["school_name"]}">${outcome["school_name"]}</a>
                            <a href="/institution/"${outcome["school_name"]}/${outcome["institution_name"]}>
                            ${outcome["institution_name"]}</a></div>
                            <div>相似成果数量 ：${outcome["achieve_nums"]}</div>
                            <button>                            
                        `;
            html.push(row_data);
        }
    }
    innerString = html.join("");
    document.getElementById("outcome_put").innerHTML = innerString;
}

// $("#nav1").on('click', function(){
//     document.getElementById('nav1').setAttribute("class", "nav-link active");
//     document.getElementById('nav2').setAttribute("class", "nav-link");
//     outcome_list = outcome_paper_list;
//     select_type = 0;
//     school_dict = paper_school_dict;
//     currentPage = 1;
//     inner_html();
//     show_school(school_dict);
//
// });

$("#nav2").on('click', function(){
    document.getElementById('nav2').setAttribute("class", "nav-link active");
    // document.getElementById('nav1').setAttribute("class", "nav-link");
    outcome_list = outcome_patent_list;
    school_dict = patent_school_dict;
    currentPage = 1;
    // inner_html();
    show_school(school_dict);
    update_show_result();
})



$(".layui-laypage-first").on('click',function(){
    if(currentPage != 1) {
        currentPage = 1;
        console.log("test1   " + currentPage);
        update_show_result();
    }
})

$(".layui-laypage-pre").on('click',function(){
    if(currentPage != 1) {
        currentPage = currentPage-1;
        console.log("test1   " + currentPage);
        update_show_result();
    }
});

$(".layui-laypage-next").on('click',function(){
    if(currentPage != pageNumber) {
        currentPage = currentPage+1;
        console.log("test1   " + currentPage);
        update_show_result();
    }
});

$(".layui-laypage-last").on('click',function(){
    if(currentPage != pageNumber) {
        currentPage = pageNumber;
        console.log("test1     " + currentPage);
        update_show_result();
    }
});
