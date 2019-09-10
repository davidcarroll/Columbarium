#Roles=Admin
def Start():
    model.Title = "Columbarium Walls"
    data = model.DynamicData()
    docName = 'ColumbariumNicheData'
    styleName = "ColumbariumNicheStyle"
    mainScriptName = "ColumbariumRecord"
    keyword = "Columbarium"
    if model.IsDebug:
        mainScriptName = "c!dev-columbarium-PythonScripts-%s.py-kw-Columbarium" % mainScriptName
        styleName = "c:/dev/columbarium/html/%s.text.html" % styleName
    data.doc = model.DynamicDataFromJson(model.Content(docName, keyword))
    style = model.Content(styleName, keyword)
    data.lookup = q.QuerySql("select * from custom.ColumbariumLookupNiche")

    data.nicheLink = '<a href="/PyScriptForm/%s/niche/{0}" target="link">{0}</a>' % mainScriptName
    certificateUrl = '/PyScriptForm/%s/certificate/{0}' % mainScriptName
    data.certificateLink = '<br><span><small><a href="%s" target="link">COL&#8209;{0}</a></small></span>' % certificateUrl

    print style
    print '<div><a href="/PyScript/ColumbariumMenu" target="ColumbariumMenu">Columbarium Menu</a></div>'
    data.checkmarkIcon = '<i class="glyphicon glyphicon-ok"></i>'
    data.urnIcon = '<i class="glyphicon glyphicon-modal-window"></i>'

    for wall in data.doc.Walls:
        PrintWall(wall, data)

def LookupData(nicheid, data):
    return next((i for i in data.lookup if i.NicheId == nicheid), None)

def PrintWall(wall, data):
    print '<h2 style="text-align:center">{}</h2>'.format(wall.name)
    print '<table align="center" class="table notwide niche">'
    for row in data.doc.Rows:
        print '<tr>'
        for col in range(wall.start, wall.end + 1):
            nicheid = "{}-{}".format(row,col)
            lookupdata = LookupData(nicheid, data)
            print '<td>'
            cert = lookupdata.Certificate
            nichelink = data.nicheLink.format(nicheid)
            print nichelink if len(cert) > 0 else nicheid
            certlink = data.certificateLink.format(cert)
            print certlink if len(cert) > 0 else data.checkmarkIcon
            if lookupdata.InurnedCnt:
                print '<br>'
            for i in range(lookupdata.InurnedCnt):
                print data.urnIcon
            print '</td>'
            if col == wall.divider:
                print '<td>&nbsp;</td>'
        print '</tr>'
    print '</table>'

Start()