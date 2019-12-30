#Roles=Columbarium
model.UsesCustomView("ColumbariumNiches")
model.UsesCustomView("ColumbariumInurnments")
model.UsesCustomView("ColumbariumPeople")
model.UsesCustomView("ColumbariumNichePeople")
model.UsesCustomView("ColumbariumLookupNiche")
model.UsesCustomView("ColumbariumLookup")
model.UsesCustomView("ColumbariumNextCertificate")

def Menu():
    model.Title = "Columbarium Menu"
    rptSqlName = "ColumbariumRpt"
    rptUnclaimedNichesSqlName = "ColumbariumUnclaimedNiches"
    rptUnclaimedHalfNichesSqlName = "ColumbariumUnclaimedHalfNiches"
    rptCertificatesWithMultipleNichesSqlName = "ColumbariumCertificatesWithMultipleNiches"

    nicheWallsScriptName = "ColumbariumNicheWalls"
    mainScriptName = "ColumbariumRecord"
    javascriptName = "PeopleSearchJavascript"

    javascript = model.Content(javascriptName)
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