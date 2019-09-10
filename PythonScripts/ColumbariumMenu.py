#Roles=Admin
def Menu():
    model.Title = "Columbarium Menu"
    rptSqlName = "ColumbariumRpt"
    rptUnclaimedNichesSqlName = "ColumbariumUnclaimedNiches"
    rptUnclaimedHalfNichesSqlName = "ColumbariumUnclaimedHalfNiches"
    rptCertificatesWithMultipleNichesSqlName = "ColumbariumCertificatesWithMultipleNiches"

    nicheWallsScriptName = "ColumbariumNicheWalls"
    mainScriptName = "ColumbariumRecord"
    javascriptName = "PeopleSearchJavascript"
    keyword = "Columbarium"

    if model.IsDebug:
        base = "c!dev-columbarium-{}-kw-" + keyword
        rptSqlName = base.format(
            "Reports-%s.sql" % rptSqlName)
        rptUnclaimedNichesSqlName = base.format(
            "Reports-%s.sql" % rptUnclaimedNichesSqlName)
        rptUnclaimedHalfNichesSqlName = base.format(
            "Reports-%s.sql" % rptUnclaimedHalfNichesSqlName)
        rptCertificatesWithMultipleNichesSqlName = base.format(
            "Reports-%s.sql" % rptCertificatesWithMultipleNichesSqlName)
        nicheWallsScriptName = base.format(
            "PythonScripts-%s.py" % nicheWallsScriptName)
        mainScriptName = base.format(
            "PythonScripts-%s.py" % mainScriptName)
        buildNicheScriptName = "ColumbariumBuildNicheData"
        javascriptName = "c:/dev/columbarium/Html/%s.js" % javascriptName

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
    print '</div></div></div>'

Menu()