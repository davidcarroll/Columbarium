
def WriteContent(w, base, name, typ):
    f = open('{}/{}.{}'.format(base, name, typ), 'r')
    text = f.read()
    fulltype = Type(typ)
    w.write('model.WriteContent{}("{}", """\n{}\n""")\n'.format(fulltype, name, text))

def WriteView(w, base, name):
    f = open('{}{}.sql'.format(base, name), 'r')
    text = f.read()
    w.write('model.CreateCustomView("Columbarium{}", """\n{}\n""")\n'.format(name, text))

def Type(typ):
    if typ == 'sql':
        return 'Sql'
    if typ == 'py':
        return 'Python'
    if typ == 'json':
        return 'Text'
    if typ == 'js':
        return 'Text'
    if typ == 'text.html':
        return 'Text'

def WritePythonScripts(w):
    base = 'C:/dev/columbarium/PythonScripts/'
    WriteContent(w, base, 'ColumbariumBuildNicheData', 'py')
    WriteContent(w, base, 'ColumbariumMenu', 'py')
    WriteContent(w, base, 'ColumbariumjNicheWalls', 'py')
    WriteContent(w, base, 'ColumbariumRecord', 'py')

def WriteReports(w)
    base = 'C:/dev/columbarium/Reports/'
    WriteContent(w, base, 'ColumbariumCertificatesWithMultipleNiches, 'sql')
    WriteContent(w, base, 'ColumbariumRpt', 'sql')
    WriteContent(w, base, 'ColumbariumUnclaimedHalfNiches', 'sql')
    WriteContent(w, base, 'ColumbariumUnclaimedNiches', 'sql')

def WriteHtml(w)
    base = 'C:/dev/columbarium/Html/'
    WriteContent(w, base, 'ColumbariumFormDisplay', 'text.html')
    WriteContent(w, base, 'ColumbariumFormEdit', 'text.html')
    WriteContent(w, base, 'ColumbariumFormNewRecord', 'text.html')
    WriteContent(w, base, 'ColumbariumNicheStyle', 'text.html')
    WriteContent(w, base, 'ColumbariumRecordDeleted', 'text.html')
    WriteContent(w, base, 'ColumbariumRecordHtml', 'text.html')
    WriteContent(w, base, 'ColumbariumRecordJavascript', 'js')
    WriteContent(w, base, 'PeopleSearchJavascript', 'js')

def WriteViews(w):
    base = 'C:/dev/columbarium/Views/'
    WriteView(w, base, 'Inurnments')
    WriteView(w, base, 'Lookup')
    WriteView(w, base, 'LookupNiche')
    WriteView(w, base, 'NextCertificate')
    WriteView(w, base, 'NichePeople')
    WriteView(w, base, 'Niches')
    WriteView(w, base, 'People')

def WriteData():
    w = open('c:\dev\columbarium\installdata.py', 'w')
    base = 'C:/dev/columbarium/Conversion/BuildData/'
    WriteContent(w, base, 'ColumbariumMetaData', 'json')

def WriteDataContent():
    base = 'C:/dev/columbarium/data/'
    WriteContent(w, base, 'ColumbariumData', 'json')
    WriteContent(w, base, 'ColumbariumNicheData', 'json')

w = open('c:\dev\columbarium\installscripts.py', 'w')

WriteMenuContent(w)
WriteNicheWallsContent(w)
WriteRecordContent(w)
WriteViews(w)

WriteTestDataContent()
WriteDataContent()