$(function () {
    $('body').on('click', 'button.postOperation', function(ev){
        ev.preventDefault();
        var container = $(this).closest("div.columbarium")
        var q = $(container).find("form").serialize();
        $.post("/PyScriptForm", q, function (ret) {
            $(container).html(ret);
        });
        return false;
    });
    $('body').on('click', 'button.cancelupdate', function(ev){
        ev.preventDefault();
        var container = $(this).closest("div.columbarium")
        $(container).find("input[name=p1]").val('cancel')
        var q = $(container).find("form").serialize();
        $.post("/PyScriptForm", q, function (ret) {
            $(container).html(ret);
        });
        return false;
    });
});
