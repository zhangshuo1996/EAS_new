let outcome_patent_list = transport.outcome_patent_list;
let old_input_key = transport.input_key;
//默认选择是patent
let outcome_list = outcome_patent_list;
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
update_global_and_page();

/*
填充搜索框中的搜索内容
 */
function fill_input(){
    $("#input_key").val(old_input_key);
}

/*
点击搜索按钮时， 判断是否有输入， 若有，显示搜索圆圈， 隐藏上次的搜索结果
 */
$("#submit_button").on("click", function () {
    let new_input_key = $("#input_key").val();
    if(new_input_key != "" && new_input_key != old_input_key){
        // 显示加载圆圈
        show_load_cycle();
        get_search_outcome(new_input_key);
    }
});

/*
异步获取新的搜索结果数据
 */
function get_search_outcome(new_input_key) {
    $.ajax({
        dataType: 'json',
        type: 'get',
        data: {"input_key": new_input_key},
        url: 'search/get_search_outcome',
        success: function (json_data) {
            outcome_patent_list = json_data.data;
            hide_load_cycle();
            update_global_and_page();
        }
    })
}

/*
获取搜索结果后，更新全局变量以及页面显示
 */
function update_global_and_page() {
    outcome_list = outcome_patent_list;
    cur_outcome_list = outcome_list;
    extract_patent_school_list();
    // 当前选中的学校 包含在结果中的
    cur_outcome_list = outcome_list;

    patent_school_dict = {};
    extract_patent_school_list();
    //默认学校列表选择是patent结果中的
    school_dict = patent_school_dict;
    currentPage = 1; // 当前是第几页
    pageSize = 6; // 每页显示的数量
    total = outcome_list.length; // 总共的数量
    pageNumber = parseInt(total / pageSize) + 1; //总共的页数
    // 显示右侧边栏的学校
    show_school(school_dict);
    // 更新搜索结果内容
    update_show_result();
    document.getElementById("layui-laypage-count").innerHTML = "共" + total + "条";
    fill_input();
}


/*
提取出专利搜索结果中的学校列表
 */
function extract_patent_school_list() {
    for(let i = 0; i < outcome_patent_list.length; i++){
        let school = outcome_patent_list[i]["basic_info"]["school"];
        let school_id = outcome_patent_list[i]["basic_info"]["school_id"];
        if(patent_school_dict.hasOwnProperty(school_id) == false){
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
学校列表复选框点击事件
 */
$("#show_school label .select_school").on("change", function () {
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
    let innerString = "";
    for(let i = 1; i <= pageNumber; i++){
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
// function inner_html(select_school_id_list){
//     let html = [];
//     console.log(outcome_list);
//     for(let i = pageSize * (currentPage - 1); i < pageSize * (currentPage-1) + pageSize && i < total; i++){
//         let outcome = cur_outcome_list[i];
//         let index = i+1;
//         let school_id_str = outcome["basic_info"]["school_id"].toString();
//         let is_existed = select_school_id_list.indexOf(school_id_str) > -1;
//         if(!is_existed){
//             continue;
//         }
//         let row_data = `
//                     <tr>
//                         <th scope="row">${index}</th>
//                         <td><a href="/school/${outcome["basic_info"]["school"]}">${outcome["basic_info"]["school"]}</a></td>
//                         <td><a href="/institution/${outcome["basic_info"]["school"]}/${outcome["basic_info"]["institution"]}">${outcome["basic_info"]["institution"]}</a></td>
//                         <td><a href="/teacher/${outcome["id"]}">${outcome["basic_info"]["name"]}</div></td>
//                         <td>
//                             <div class="accordion" id="accordionExample">
//
//                                 <div class="card-header" id="headingOne">
//                                   <h2 class="mb-0">
//                                     <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapse${i}" aria-expanded="false" aria-controls="collapse${i}">
//                                       相似成果数量：${outcome["achieve_nums"]}
//                                     </button>
//                                   </h2>
//                                 </div>
//                                 <div id="collapse${i}" class="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
//                                   <div class="card-body">
//         `;
//         html.push(row_data);
//
//         let patent_list = outcome["patent_list"];
//         for(let i = 0; i < patent_list.length; i++){
//             let inner_data = `
//                             <div class="ends" style="font-size:1vw;-webkit-transform-origin-x: 0;-webkit-transform: scale(0.90);">
//                                 ${patent_list[i]["patent_name"]}
//                             </div>
//             `;
//             html.push(inner_data);
//         }
//         let last_data = `
//
//                             </div>
//                           </div>
//                         </div>
//                     </td>
//                 </tr>
//         `;
//         html.push(last_data);
//     }
//     innerString = html.join("");
//     document.getElementById("outcome_put").innerHTML = innerString;
// }


function inner_html(select_school_id_list){
    let html = [];
    console.log(outcome_list);
    for(let i = pageSize * (currentPage - 1); i < pageSize * (currentPage-1) + pageSize && i < total; i++){
        let outcome = cur_outcome_list[i];
        let index = i+1;
        let school_id_str = outcome["basic_info"]["school_id"].toString();
        let is_existed = select_school_id_list.indexOf(school_id_str) > -1;
        if(!is_existed){
            continue;
        }
        let row_data = `
                    <div class="card">
                    <div class="card-header" id="headingOne">
                        <h2 class="mb-0">
                            <div class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                                <span>
                                    <a href="#">${outcome["basic_info"]["school"]}</a> 
                                    <a href="#">${outcome["basic_info"]["institution"]}</a> 
                                    <a href="#">${outcome["basic_info"]["name"]}</a>
                                </span>
                                
                                <span class="badge badge-primary" style="text-align: right"> 相似成果数量${outcome["achieve_nums"]}</span>
<!--                                <div class="text-right">-->
<!--                                </div>-->
                            </div>
                          </h2>
                        </div>
                        <div id="collapseOne" class="collapse " aria-labelledby="headingOne" data-parent="#accordionExample">
                          <div class="card-body">
        `;
        html.push(row_data);

        let patent_list = outcome["patent_list"];
        for(let i = 0; i < patent_list.length; i++){
            let inner_data = `
                            <p>
                                ${patent_list[i]["patent_name"]}
                            </p>
            `;
            html.push(inner_data);
        }
        let last_data = `
                            </div>
                        </div>
                      </div>
        `;
        html.push(last_data);
    }
    innerString = html.join("");
    document.getElementById("outcome_put").innerHTML = innerString;
}

/*
隐藏搜索结果，翻页和学校列表， 显示加载圆圈
 */
function show_load_cycle(){
    $("#outcome_list").attr("class", "d-none");
    $("#change_page").attr("class", "d-none");
    // 显示加载圆圈
    $("#load_cycle").attr("class", "");
}

/*
显示搜索结果，翻页和学校列表， 隐藏加载圆圈
 */
function hide_load_cycle(){
    $("#outcome_list").attr("class", "row");
    $("#change_page").attr("class", "row");
    // 显示加载圆圈
    $("#load_cycle").attr("class", "d-none");
}


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
