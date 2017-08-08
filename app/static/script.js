$(function(){
    $('#add_search_row').on("click",function(){
        var $tableBody = $('#search_rows_tbl').find("tbody"),
        $trLast = $tableBody.find("tr:last"),
        $trNew = $trLast.clone(true);

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
            $(this).parent().parent().find("input[type=text]").removeAttr("disabled");
        }
        else{
            $(this).parent().parent().find("input[type=text]").attr("disabled","disabled");
        }
    });
});