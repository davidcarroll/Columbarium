$(function () {
    ColumbariumPostOperation = function(event) {
        event.preventDefault();
        var target = event.target || event.srcElement;
        var container = $(target).closest("div.columbarium")
        var q = $(container).find("form").serialize();
        $.post("/PyScriptForm", q, function (ret) {
            $(container).html(ret);
        });
    }
    ColumbariumCancelUpdate = function(event) {
        event.preventDefault();
        var target = event.target || event.srcElement;
        var container = $(target).closest("div.columbarium")
        $(container).find("input[name=p1]").val('cancel')
        var q = $(container).find("form").serialize();
        $.post("/PyScriptForm", q, function (ret) {
            $(container).html(ret);
        });
    }
});
