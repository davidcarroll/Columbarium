
def WriteContent(w, base, name, typ):
    f = open('{}/{}.{}'.format(base, name, typ), 'r')
    text = f.read()
    fulltype = Type(typ)
    w.write('model.WriteContent{}("{}", """\n{}\n""")\n'.format(fulltype, name, text))

def WriteView(w, base, name):
    f = open('{}{}.sql'.format(base, name), 'r')
    text = f.read()
    w.write('model.CreateCustomView("{}", """\n{}\n""")\n'.format(name, text))

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

def WriteMenuContent(w):
    base = 'C:/dev/columbarium/menu/'
    WriteContent(w, base, 'ColumbariumMenu', 'py')
    WriteContent(w, base, 'ColumbariumRpt', 'sql')
    WriteContent(w, base, 'ColumbariumRptCertificatesWithMultipleNiches', 'sql')
    WriteContent(w, base, 'ColumbariumRptUnclaimedNiches', 'sql')
    WriteContent(w, base, 'ColumbariumRptUnclaimedHalfNiches', 'sql')
    WriteContent(w, base, 'PeopleSearchJavascript', 'js')
    WriteContent(w, base, 'ColumbariumBuildNicheData', 'py')

def WriteNicheWallsContent(w):
    base = 'C:/dev/columbarium/nichewalls/'
    WriteContent(w, base, 'ColumbariumNicheLookupData', 'sql')
    WriteContent(w, base, 'ColumbariumNicheStyle', 'text.html')
    WriteContent(w, base, 'ColumbariumNicheWalls', 'py')

def WriteRecordContent(w):
    base = 'C:/dev/columbarium/record/'
    WriteContent(w, base, 'ColumbariumFormDisplay', 'text.html')
    WriteContent(w, base, 'ColumbariumFormEdit', 'text.html')
    WriteContent(w, base, 'ColumbariumFormNewRecord', 'text.html')
    WriteContent(w, base, 'ColumbariumRecord', 'py')
    WriteContent(w, base, 'ColumbariumRecordDeleted', 'text.html')
    WriteContent(w, base, 'ColumbariumRecordHtml', 'text.html')
    WriteContent(w, base, 'ColumbariumRecordJavascript', 'js')
    WriteContent(w, base, 'ColumbariumRecordLookupData', 'sql')
    WriteContent(w, base, 'ColumbariumRecordNextCertificate', 'sql')

def WriteViews(w):
    base = 'C:/dev/columbarium/conversion/buildviews/ColumbariumBuildViews'
    WriteView(w, base, 'Inurnments')
    WriteView(w, base, 'NichePeople')
    WriteView(w, base, 'Niches')
    WriteView(w, base, 'ColumbariumPeople')

def WriteDataContent():
    w = open('c:\dev\columbarium\installdata.py', 'w')
    base = 'C:/dev/columbarium/data/'
    WriteContent(w, base, 'ColumbariumData', 'json')
    WriteContent(w, base, 'ColumbariumDataMeta', 'json')
    WriteContent(w, base, 'ColumbariumNicheData', 'json')

def WriteTestDataContent():
    w = open('c:\dev\columbarium\installtestdata.py', 'w')
    base = 'C:/dev/columbarium/Data/test'
    WriteContent(w, base, 'ColumbariumData', 'json')
    WriteContent(w, base, 'ColumbariumDataMeta', 'json')
    WriteContent(w, base, 'ColumbariumBuildNicheData', 'py')

w = open('c:\dev\columbarium\installscripts.py', 'w')

WriteMenuContent(w)
WriteNicheWallsContent(w)
WriteRecordContent(w)
WriteViews(w)

WriteTestDataContent()
WriteDataContent()