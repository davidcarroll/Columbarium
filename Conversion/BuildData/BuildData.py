'''
http://localhost:8888/PyScript/c!dev-columbarium-Conversion-BuildData-BuildData.py-kw-Columbarium
'''

keyword = 'Columbarium'

def CleanSlate():
    sql = model.ReadFile("c:/dev/Columbarium/Conversion/BuildData/DatabaseCleanStart.sql")
    model.ExecuteSql(sql)

def WritePython():
    base = "c:/dev/Columbarium/PythonScripts/"

    py = model.ReadFile(base + "ColumbariumBuildNicheData.py")
    model.WriteContentPython('ColumbariumBuildNicheData',  py, keyword)
    model.CallScript('ColumbariumBuildNicheData')

    py = model.ReadFile(base + "ColumbariumMenu.py")
    model.WriteContentPython('ColumbariumMenu',  py, keyword)

    py = model.ReadFile(base + "ColumbariumNicheWalls.py")
    model.WriteContentPython('ColumbariumNicheWalls',  py, keyword)

    py = model.ReadFile(base + "ColumbariumRecord.py")
    model.WriteContentPython('ColumbariumRecord',  py, keyword)

def WriteDataRecords():
    base = "c:/dev/Columbarium/Conversion/BuildData/"

    # MetaData
    MetaData = model.ReadFile(base + "ColumbariumMetaData.json")
    model.WriteContentText('ColumbariumMetaData', MetaData, keyword)
    meta = model.DynamicDataFromJson(MetaData)

    # People
    sql = model.ReadFile(base + "People.sql")
    model.DeleteJsonRecordSection('ColumbariumPeople')
    ColumbariumPeople = model.SqlListDynamicData(sql, meta)
    for r in ColumbariumPeople:
        pid = r.PeopleId
        r.Remove('PeopleId')
        model.AddUpdateJsonRecord(r, 'ColumbariumPeople', pid)

    # Inurnments
    sql = model.ReadFile(base + "Inurnments.sql")
    model.DeleteJsonRecordSection('ColumbariumInurnments')
    Inurnments = model.SqlListDynamicData(sql)
    for r in Inurnments:
        pid = r.PeopleId
        nid = r.NicheId
        r.Remove('PeopleId')
        r.Remove('NicheId')
        model.AddUpdateJsonRecord(r, 'ColumbariumInurnments', pid, nid)

    # NichePeople
    sql = model.ReadFile(base + "NichePeople.sql")
    model.DeleteJsonRecordSection('ColumbariumNichePeople')
    NichePeople = model.SqlListDynamicData(sql)
    for r in NichePeople:
        model.AddUpdateJsonRecord("", 'ColumbariumNichePeople', r.PeopleId, r.NicheId, r.NicheId2)

def WriteViews():
    base = 'C:/dev/Columbarium/Views/'

    vw = model.ReadFile(base + "Niches.sql")
    model.CreateCustomView("ColumbariumNiches", vw)

    vw = model.ReadFile(base + "Inurnments.sql")
    model.CreateCustomView("ColumbariumInurnments", vw) 

    vw = model.ReadFile(base + "People.sql")
    model.CreateCustomView("ColumbariumPeople", vw)

    vw = model.ReadFile(base + "NichePeople.sql")
    model.CreateCustomView("ColumbariumNichePeople", vw)

    vw = model.ReadFile(base + "LookupNiche.sql")
    model.CreateCustomView("ColumbariumLookupNiche", vw)

    vw = model.ReadFile(base + "Lookup.sql")
    model.CreateCustomView("ColumbariumLookup", vw)

    vw = model.ReadFile(base + "NextCertificate.sql")
    model.CreateCustomView("ColumbariumNextCertificate", vw)

def WriteReports():
    base = 'C:/dev/Columbarium/Reports/'

    sql = model.ReadFile(base + "ColumbariumRpt.sql")
    model.WriteContentSql('ColumbariumRpt',  sql, keyword)

    sql = model.ReadFile(base + "ColumbariumCertificatesWithMultipleNiches.sql")
    model.WriteContentSql('ColumbariumCertificatesWithMultipleNiches',  sql, keyword)

    sql = model.ReadFile(base + "ColumbariumUnclaimedNiches.sql")
    model.WriteContentSql('ColumbariumUnclaimedNiches',  sql, keyword)

    sql = model.ReadFile(base + "ColumbariumUnclaimedHalfNiches.sql")
    model.WriteContentSql('ColumbariumUnclaimedHalfNiches',  sql, keyword)

def WriteHtml():
    base = "c:/dev/Columbarium/Html/"

    html = model.ReadFile(base + "ColumbariumFormDisplay.text.html")
    model.WriteContentText("ColumbariumFormDisplay", html)

    html = model.ReadFile(base + "ColumbariumFormNewRecord.text.html")
    model.WriteContentText("ColumbariumFormNewRecord", html)

    html = model.ReadFile(base + "ColumbariumNicheStyle.text.html")
    model.WriteContentText("ColumbariumNicheStyle", html)

    html = model.ReadFile(base + "ColumbariumRecordDeleted.text.html")
    model.WriteContentText("ColumbariumRecordDeleted", html)

    html = model.ReadFile(base + "ColumbariumRecordHtml.text.html")
    model.WriteContentText("ColumbariumRecordHtml", html)

    html = model.ReadFile(base + "ColumbariumRecordJavascript.js")
    model.WriteContentText("ColumbariumRecordJavascript", html)

    html = model.ReadFile(base + "PeopleSearchJavascript.js")
    model.WriteContentText("PeopleSearchJavascript", html)

WritePython()
WriteDataRecords()
WriteViews()
WriteReports()
WriteHtml()
