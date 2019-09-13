'''
http://localhost:8888/PyScript/c!dev-columbarium-Conversion-BuildData-BuildData.py-kw-Columbarium
'''
keyword = 'Columbarium'
installscripts = 'c:\dev\columbarium\installscripts.py'
installdata = 'c:\dev\columbarium\installdata.py'
model.DeleteFile(installscripts)
model.DeleteFile(installdata)

def InstallText(base, name, ext):
    text = model.ReadFile(base + name + '.' + ext)
    model.WriteContentText(name, text, keyword)
    model.WriteFile(installscripts, 
        'model.WriteContentText("{}", """\n{}\n""", "{}")\n'.format(name, text, keyword))
    return text

def InstallPython(name):
    base = "c:/dev/Columbarium/PythonScripts/"
    text = model.ReadFile(base + name + ".py")
    model.WriteContentPython(name,  text, keyword)
    model.WriteFile(installscripts, 
        'model.WriteContentPython("{}", """\n{}\n""", "{}")\n'.format(name, text, keyword))

def InstallView(name):
    base = "c:/dev/Columbarium/Views/"
    text = model.ReadFile(base + name + ".sql")
    model.CreateCustomView("Columbarium" + name, text)
    model.WriteFile(installscripts, 
        'model.CreateCustomView("Columbarium{}", """\n{}\n""")\n'.format(name, text))

def InstallReport(name):
    base = "c:/dev/Columbarium/Reports/"
    text = model.ReadFile(base + keyword + name + ".sql")
    model.WriteContentSql(keyword + name,  text, keyword)
    model.WriteFile(installscripts, 
        'model.WriteContentSql("{}", """\n{}\n""", "{}")\n'.format(keyword + name, text, keyword))

def InstallHtml(name, ext):
    base = "c:/dev/Columbarium/Html/"
    text = model.ReadFile(base + name + ext)
    model.WriteContentText(name,  text, keyword)
    model.WriteFile(installscripts, 
        'model.WriteContentText("{}", """\n{}\n""", "{}")\n'.format(name, text, keyword))

def CleanSlate():
    sql = model.ReadFile("c:/dev/Columbarium/Conversion/BuildData/DatabaseCleanStart.sql")
    model.ExecuteSql(sql)

def InstallPythonScripts():
    InstallPython('ColumbariumBuildNicheData')
    model.CallScript('ColumbariumBuildNicheData')

    InstallPython('ColumbariumMenu')
    InstallPython('ColumbariumNicheWalls')
    InstallPython('ColumbariumRecord')

def InstallDataRecords():
    base = "c:/dev/Columbarium/Conversion/BuildData/"

    # MetaData
    text = InstallText(base, 'ColumbariumMetaData', "json")
    meta = model.DynamicDataFromJson(text)

    # People
    sql = model.ReadFile(base + "People.sql")
    name = 'ColumbariumPeople'
    model.DeleteJsonRecordSection(name)
    ColumbariumPeople = model.SqlListDynamicData(sql, meta)
    for r in ColumbariumPeople:
        pid = r.PeopleId
        r.Remove('PeopleId')
        model.AddUpdateJsonRecord(r, name, pid)
        model.WriteFile(installdata, 
            "model.AddUpdateJsonRecord('{}', '{}', {})')\n".format(r.ToFlatString(), name, pid))

    # Inurnments
    sql = model.ReadFile(base + "Inurnments.sql")
    name = 'ColumbariumInurnments'
    model.DeleteJsonRecordSection(name)
    Inurnments = model.SqlListDynamicData(sql)
    for r in Inurnments:
        pid = r.PeopleId
        nid = r.NicheId
        r.Remove('PeopleId')
        r.Remove('NicheId')
        model.AddUpdateJsonRecord(r, name, pid, nid)
        model.WriteFile(installdata, 
            "model.AddUpdateJsonRecord('{}', '{}', {}, '{}')\n".format(r.ToFlatString(), name, pid, nid))

    # NichePeople
    sql = model.ReadFile(base + "NichePeople.sql")
    name = 'ColumbariumNichePeople'
    model.DeleteJsonRecordSection(name)
    NichePeople = model.SqlListDynamicData(sql)
    for r in NichePeople:
        model.AddUpdateJsonRecord("", name, r.PeopleId, r.NicheId, r.NicheId2)
        model.WriteFile(installdata, 
            "model.AddUpdateJsonRecord('', '{}', {}, '{}', '{}')\n".format(name, r.PeopleId, r.NicheId, r.NicheId2))

def InstallViews():
    InstallView('Niches')
    InstallView('Inurnments')
    InstallView('People')
    InstallView('NichePeople')
    InstallView('LookupNiche')
    InstallView('Lookup')
    InstallView('NextCertificate')

def InstallReports():
    InstallReport("Rpt")
    InstallReport("CertificatesWithMultipleNiches")
    InstallReport("UnclaimedNiches")
    InstallReport("UnclaimedHalfNiches")

def InstallHtmlFiles():
    InstallHtml(keyword + "FormDisplay", ".text.html")
    InstallHtml(keyword + "FormNewRecord", ".text.html")
    InstallHtml(keyword + "NicheStyle", ".text.html")
    InstallHtml(keyword + "RecordDeleted", ".text.html")
    InstallHtml(keyword + "RecordHtml", ".text.html")
    InstallHtml(keyword + "RecordJavascript", ".js")
    InstallHtml("PeopleSearchJavascript", ".js")

CleanSlate()
InstallPythonScripts()
InstallDataRecords()
InstallViews()
InstallReports()
InstallHtmlFiles()
