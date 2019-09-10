$("#pythonSearch").autocomplete({
    appendTo: "#SearchResults2",
    autoFocus: true,
    minLength: 1,
    source: function (request, response) {
        // The search is handled by /PythonSearch/Names in c#
        $.post("/PythonSearch/Names", request, function (ret) {
            response(ret.slice(0, 10));
        }, "json");
    },
    select: function (event, ui) {
    }
}).data("uiAutocomplete")._renderItem = function (ul, item) {
    /* The {link} below (on line line 21) will be replaced 
       with the anchor tag using something like the following code in your Python script

       javascript = model.Content(javascriptName)
       link = "<a href='/PyScriptForm/%s/person/{0}'><b>{1}</b>{2}{3}{4}</a>" % mainScriptName
       model.Script = javascript.replace("{link}", link)
    */
    link = "{link}".format(item.Pid, item.Name, item.Spouse, item.Email, item.Addr);
    return $("<li>")
        .append(link)
        .appendTo(ul);
};
