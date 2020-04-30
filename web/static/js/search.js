
//$(function (){
//    $.ajax({
//        type: "get",
//        url: "/search",
//        contentType: "application/json; charset=utf-8",
//        dataType: "json",
//        success: function(){
//            console.log("---")
//        }
//    })
//})
console.log("-----")
function search(){
    var input_key = document.getElementById("input_key2").value;
    console.log(input_key)
    console.log("0----")
    $.ajax({
        url: '/get_input',
        data: {"input_key": input_key},
        type: "POST",
        dataType: "json",
        success: function(data){
            console.log(data["data"]);
            fill(data);
        }

    })
}

/*

*/
function fill(data){
    fill_str = "";
    for(i = 0; i < data.length; i++){
        tmp_str = "<p>" + data[i]["basic_info"]["school"] + "</p>" +
                "<p>" + data[i]["basic_info"]["institution"] + "</p>" +
                "<p>" + data[i]["basic_info"]["name"] + "</p>" +
                "<p>" + data[i]["achieve_nums"] + "</p>" +"<br>";
        fill_str += tmp_str;
    }
    document.getElementById("fill").innerHTML = fill_str;
    console.log("success");
}
