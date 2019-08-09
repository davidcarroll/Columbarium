def Menu():
    model.Title = "Columbarium Menu"
    rptSqlName = "ColumbariumRpt"
    rptUnclaimedNichesSqlName = "ColumbariumRptUnclaimedNiches"
    rptUnclaimedHalfNichesSqlName = "ColumbariumRptUnclaimedHalfNiches"
    rptCertificatesWithMultipleNichesSqlName = "ColumbariumRptCertificatesWithMultipleNiches"

    nicheWallsScriptName = "ColumbariumNicheWalls"
    mainScriptName = "ColumbariumRecord"
    buildDataScriptName = "ColumbariumBuildData"
    buildMetaScriptName = "ColumbariumBuildMetaData"
    buildNicheScriptName = "ColumbariumBuildNicheData"
    createViewsScriptName = "ColumbariumBuildViews"
    javascriptName = "PeopleSearchJavascript"
    keyword = "Columbarium"

    if model.IsDebug:
        base = "c!dev-columbarium-{}-kw-" + keyword
        rptSqlName = base.format(
            "Menu-%s.sql" % rptSqlName)
        rptUnclaimedNichesSqlName = base.format(
            "Menu-%s.sql" % rptUnclaimedNichesSqlName)
        rptUnclaimedHalfNichesSqlName = base.format(
            "Menu-%s.sql" % rptUnclaimedHalfNichesSqlName)
        rptCertificatesWithMultipleNichesSqlName = base.format(
            "Menu-%s.sql" % rptCertificatesWithMultipleNichesSqlName)
        nicheWallsScriptName = base.format(
            "Walls-%s.py" % nicheWallsScriptName)
        mainScriptName = base.format(
            "Record-%s.py" % mainScriptName)
        buildDataScriptName = base.format(
            "Conversion-%s.py" % buildDataScriptName)
        buildMetaScriptName = base.format(
            "Conversion-%s.py" % buildMetaScriptName)
        buildNicheScriptName = base.format(
            "Conversion-%s.py" % buildNicheScriptName)
        createViewsScriptName = base.format(
            "Conversion-%s.py" % createViewsScriptName)
        javascriptName = "c:/dev/columbarium/Menu/%s.js" % javascriptName

    javascript = model.Content(javascriptName, keyword)
    link = "<a href='/PyScriptForm/%s/person/{0}' target='link'><b>{1}</b>{2}{3}{4}</a>" % mainScriptName
    model.Script = javascript.replace("{link}", link)

    print '''Search by Name or PeopleId: <input id="pythonSearch" type="text" autocomplete="off" 
        style="width: 14em; font-size: 14px; padding: 5px;" class="form-control input-sm" />'''

    print '<a href="/PyScript/%s" target="walls">Niche Walls</a><br>' % nicheWallsScriptName
    print '<a href="/RunScript/%s" target="rpt">Columbarium Report</a><br>' % rptSqlName
    print '<a href="/RunScript/%s" target="rpt">Unclaimed Empty Niches</a><br>' % rptUnclaimedNichesSqlName
    print '<a href="/RunScript/%s" target="rpt">Unclaimed Half Niches</a><br>' % rptUnclaimedHalfNichesSqlName
    print '<a href="/RunScript/%s" target="rpt">Certificates With Multiple Niches</a><br>' % rptCertificatesWithMultipleNichesSqlName

    if model.IsDebug:
        print '<br>'
        print '<a href="/PyScript/%s">Build Columbarium Data</a><br>' % buildDataScriptName
        print '<a href="/PyScript/%s">Build Columbarium Meta Data</a><br>' % buildMetaScriptName
        print '<a href="/PyScript/%s">Build Columbarium Niche Data</a><br>' % buildNicheScriptName
        print '<a href="/PyScript/%s">Create Views</a><br>' % createViewsScriptName
Menu()