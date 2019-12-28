keyword = 'Columbarium'
installdata = 'c:\dev\columbarium\installdata.py'
model.DeleteFile(installdata)

def BuildCleanSlate():
    sql = "delete custom.JsonDocumentRecords where Section like 'Columbarium%'"
    model.WriteFile(installdata, "model.ExecuteSql('''\n%s\n''')\n" % sql)

def BuildDataRecords():
    base = "c:/dev/Columbarium/Conversion/BuildData/"

    # MetaData
    text = model.ReadFile("c:/dev/Columbarium/Html/ColumbariumMetaData.json")
    meta = model.DynamicDataFromJson(text)

    # People
    sql = model.ReadFile(base + "People.sql")
    name = 'ColumbariumPeople'
    ColumbariumPeople = model.SqlListDynamicData(sql, meta)
    for r in ColumbariumPeople:
        pid = r.PeopleId
        r.Remove('PeopleId')
        json = r.ToFlatString()
        json = json.replace('\\"', '\\\\"')
        model.WriteFile(installdata, 
            "model.AddUpdateJsonRecord('{}', '{}', {})\n".format(json, name, pid))

    # Inurnments
    sql = model.ReadFile(base + "Inurnments.sql")
    name = 'ColumbariumInurnments'
    Inurnments = model.SqlListDynamicData(sql)
    for r in Inurnments:
        pid = r.PeopleId
        nid = r.NicheId
        r.Remove('PeopleId')
        r.Remove('NicheId')
        json = r.ToFlatString()
        json = json.replace('\\"', '\\\\"')
        model.WriteFile(installdata, 
            "model.AddUpdateJsonRecord('{}', '{}', {}, '{}')\n".format(json, name, pid, nid))

    # NichePeople
    sql = model.ReadFile(base + "NichePeople.sql")
    name = 'ColumbariumNichePeople'
    NichePeople = model.SqlListDynamicData(sql)
    for r in NichePeople:
        model.WriteFile(installdata, 
            "model.AddUpdateJsonRecord('', '{}', {}, '{}', '{}')\n".format(name, r.PeopleId, r.NicheId, r.NicheId2))

BuildCleanSlate()
BuildDataRecords()
