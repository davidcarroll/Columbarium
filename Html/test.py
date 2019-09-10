meta = model.DynamicDataFromJson(model.Content("ColumbariumDataMeta"))
view = 'ColumbariumRecordLookup'
peopleid = 15974
certificate = 339
sql = "select * from custom.{} where Certificate = '{}'".format(view, certificate)
#rows = model.SqlList(sql)
r = model.SqlListDynamicData(sql, meta.ColumbariumPeople)
print '<pre>'
#print model.FormatJson(rows)
print model.FormatJson(r)
print '</pre>'

'''
doc = model.DynamicDataFromJson(model.Content("ColumbariumData"))
print '<pre>'
for r in doc.ColumbariumPeople:
    pid = r.PeopleId
    r.Remove('PeopleId')
    model.AddUpdateJsonRecord(str(r), 'ColumbariumPeople', pid)
    print pid
    print r
for r in doc.Inurnments:
    pid = r.PeopleId
    niche = r.Niche
    r.Remove('Niche')
    r.Remove('PeopleId')
    model.AddUpdateJsonRecord(str(r), 'Inurnments', niche, pid)
    print niche, pid
    print r
for r in doc.NichePeople:
    pid = r.PeopleId
    niche = r.Niche
    if r.NicheId == None:
        continue
    r.Remove('Niche')
    r.Remove('PeopleId')
    model.AddUpdateJsonRecord(str(r), 'NichePeople', niche, pid)
    print niche, pid
    print r
print '</pre>'
'''

