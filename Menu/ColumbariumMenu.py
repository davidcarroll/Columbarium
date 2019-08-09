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
            "NicheWalls-%s.py" % nicheWallsScriptName)
        mainScriptName = base.format(
            "Record-%s.py" % mainScriptName)
        buildDataScriptName = base.format(
            "Conversion-BuildData-%s.py" % buildDataScriptName)
        buildMetaScriptName = base.format(
            "Conversion-BuildData-%s.py" % buildMetaScriptName)
        buildNicheScriptName = base.format(
            "Conversion-BuildData-%s.py" % buildNicheScriptName)
        createViewsScriptName = base.format(
            "Conversion-BuildViews-%s.py" % createViewsScriptName)
        javascriptName = "c:/dev/columbarium/Menu/%s.js" % javascriptName

    javascript = model.Content(javascriptName, keyword)
    link = "<a href='/PyScriptForm/%s/person/{0}' target='link'><b>{1}</b>{2}{3}{4}</a>" % mainScriptName
    model.Script = javascript.replace("{link}", link)

    print '''
    <div id="page-header" class="text-center"><h2>Columbarium Menu</h2></div>
    <div class="container-fluid" id="main">
        <div class="box-content">
            <div class="well" style="max-width: 350px; margin: auto;">
                Search by Name or PeopleId: <input id="pythonSearch" type="text" autocomplete="off" 
                    style="width: 14em; font-size: 14px; padding: 5px;" class="form-control input-sm" /><br>
                <a href="/PyScript/{}" target="walls">Niche Walls</a><br>
                <a href="/RunScript/{}" target="rpt">Columbarium Report</a><br>
                <a href="/RunScript/{}" target="rpt">Unclaimed Empty Niches</a><br>
                <a href="/RunScript/{}" target="rpt">Unclaimed Half Niches</a><br>
                <a href="/RunScript/{}" target="rpt">Certificates With Multiple Niches</a><br>
    '''.format( nicheWallsScriptName, 
                rptSqlName, 
                rptUnclaimedNichesSqlName, 
                rptUnclaimedHalfNichesSqlName, 
                rptCertificatesWithMultipleNichesSqlName)
    if model.IsDebug:
        print '''
        <br>
        <a href="/PyScript/{}">Build Columbarium Data</a><br>
        <a href="/PyScript/{}">Build Columbarium Meta Data</a><br>
        <a href="/PyScript/{}">Build Columbarium Niche Data</a><br>
        <a href="/PyScript/{}">Create Views</a><br>
        '''.format( buildDataScriptName,
                    buildMetaScriptName,
                    buildNicheScriptName,
                    createViewsScriptName)
    print '</div></div></div>'

Menu()