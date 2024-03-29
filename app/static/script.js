$(function(){
    $('#add_search_row').on("click",function(){
        var $tableBody = $('#search_rows_tbl').find("tbody"),
        $trLast = $tableBody.find("tr:last"),
        $trNew = $trLast.clone(true);

        var new_index = parseInt($trLast.attr("data-index"))+1;
        $trNew.attr("data-index",new_index);
        $trNew.find("select").attr("name","criterion-" + new_index + "-column");
        $trNew.find("input[type=text]").attr("name","criterion-" + new_index + "-regex_search");

        $trLast.after($trNew);
        $('.remove_search_row').removeAttr("disabled")
    });

    $('.remove_search_row').on("click",function(){
        if ($('#search_rows_tbl > tbody tr').length > 1){
            $(this).parent().parent().remove();
        }
    });
    $('#graph_it_btn').on("click",function(){
        // I don't really know or like javascript, please help :(
        var result = "";
        $.ajax({
            url:'/api/get_active_data',
            async:false,
            success: function(data){
                result = data;
            }
        });
        data = result["data"]
        headers = result["headers"]
        x_axis = $('#x_axis').find(":selected").text();
        y_axis = $('#y_axis').find(":selected").text();
        console.log(x_axis)
        console.log(y_axis)
        // Get data for x axis
        var x_data = [];
        for (var i=0; i<data.length; i++){
            x_data.push(data[i][x_axis]);
        }

        // Get data for y axis
        var y_data = [];
        for (var i=0; i<data.length; i++){
            y_data.push(data[i][y_axis]);
        }
        console.log("x_data " + x_data);
        console.log("y_data " + y_data);
        var trace1 = {
            x:x_data,
            y:y_data,
            mode:"lines",
            type:"scatter"
        };
        Plotly.newPlot("graph_output",[trace1]);
    });

    $('.col_setup_data_type').on("click",function(){
        d_type = $(this).find(":selected").attr("value");
        console.log(d_type)
        // If d_type is datetime then allow format column to be filled in
        if (d_type == "datetime"){
            $(this).parent().parent().find("input[type=text][name$=_format]").removeAttr("disabled");
        }
        else{
            $(this).parent().parent().find("input[type=text][name$=_format]").attr("disabled","disabled");
        }
    });

    function update_conditions_avail(h_select){
        d_type = $(h_select).find(":selected").attr("data-d-type")
        conditions = $(h_select).parent().parent().find("#collate_condition");
        options = conditions.children()
        for (var i=0; i<options.length; i++){
            d_types = $(options[i]).attr("data-d-types").split(" ")
            if ($.inArray(d_type,d_types) > -1){
                $(options[i]).removeAttr("disabled")
            }
            else{
                $(options[i]).attr("disabled","disabled")
            }
        }
    }

    $('#condition_col').on("change",function(){
        update_conditions_avail(this);
    });

    $('#condition_col').on("load",function(){
        update_conditions_avail(this);
    });
});