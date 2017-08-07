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
    });
});