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
});