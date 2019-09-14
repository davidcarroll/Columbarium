keyword = 'Columbarium'
installscripts = 'c:\dev\columbarium\installscripts.py'
model.DeleteFile(installscripts)

def BuildText(base, name, ext):
    text = model.ReadFile(base + name + '.' + ext)
    model.WriteFile(installscripts, 
        'model.WriteContentText("{}", """\n{}\n""", "{}")\n'.format(name, text, keyword))
    return text

def BuildPython(name):
    base = "c:/dev/Columbarium/PythonScripts/"
    text = model.ReadFile(base + name + ".py")
    model.WriteFile(installscripts, 
        'model.WriteContentPython("{}", """\n{}\n""", "{}")\n'.format(name, text, keyword))

def BuildView(name):
    base = "c:/dev/Columbarium/Views/"
    text = model.ReadFile(base + name + ".sql")
    model.WriteFile(installscripts, 
        'model.CreateCustomView("Columbarium{}", """\n{}\n""")\n'.format(name, text))

def BuildReport(name):
    base = "c:/dev/Columbarium/Reports/"
    text = model.ReadFile(base + keyword + name + ".sql")
    model.WriteFile(installscripts, 
        'model.WriteContentSql("{}", """\n{}\n""", "{}")\n'.format(keyword + name, text, keyword))

def BuildHtml(name, ext):
    base = "c:/dev/Columbarium/Html/"
    text = model.ReadFile(base + name + ext)
    model.WriteFile(installscripts, 
        'model.WriteContentText("{}", """\n{}\n""", "{}")\n'.format(name, text, keyword))

def BuildCleanSlate():
    sql = model.ReadFile("c:/dev/Columbarium/Conversion/BuildData/DatabaseCleanStartFiles.sql")
    model.WriteFile(installscripts, "model.ExecuteSql('''\n%s\n''')\n" % sql)

def BuildPythonScripts():
    BuildPython('ColumbariumBuildNicheData')
    model.WriteFile(installscripts, "model.CallScript('ColumbariumBuildNicheData')\n")

    BuildPython('ColumbariumMenu')
    BuildPython('ColumbariumNicheWalls')
    BuildPython('ColumbariumRecord')

def BuildViews():
    BuildView('Niches')
    BuildView('Inurnments')
    BuildView('People')
    BuildView('NichePeople')
    BuildView('LookupNiche')
    BuildView('Lookup')
    BuildView('NextCertificate')

def BuildReports():
    BuildReport("Rpt")
    BuildReport("CertificatesWithMultipleNiches")
    BuildReport("UnclaimedNiches")
    BuildReport("UnclaimedHalfNiches")

def BuildHtmlFiles():
    BuildHtml(keyword + "FormDisplay", ".text.html")
    BuildHtml(keyword + "FormEdit", ".text.html")
    BuildHtml(keyword + "FormNewRecord", ".text.html")
    BuildHtml(keyword + "NicheStyle", ".text.html")
    BuildHtml(keyword + "RecordDeleted", ".text.html")
    BuildHtml(keyword + "RecordHtml", ".text.html")
    BuildHtml(keyword + "MetaData", ".json")
    BuildHtml(keyword + "RecordJavascript", ".js")
    BuildHtml("PeopleSearchJavascript", ".js")

BuildCleanSlate()
BuildPythonScripts()
BuildViews()
BuildReports()
BuildHtmlFiles()
