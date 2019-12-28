#Roles=Columbarium

def Initialize():
    model.Title = "Columbarium Record"
    #avoid using global data so debugging can examine all variables
    data = model.DynamicData()

    # names of all the records stored in Special Content records
    data.editFormName = 'ColumbariumFormEdit'
    data.addNewRecordFormName = 'ColumbariumFormNewRecord'
    data.javascriptName = 'ColumbariumRecordJavascript'
    data.htmlName = 'ColumbariumRecordHtml'
    data.htmlRecordDeletedName = 'ColumbariumRecordDeleted'
    data.nextCertificateSqlName = 'ColumbariumRecordNextCertificate'
    data.redirect = '/PyScriptForm/ColumbariumRecord/person/%s'
    data.NicheSection = "ColumbariumNichePeople"
    data.PeopleSection = "ColumbariumPeople"
    data.InurnmentSection = "ColumbariumInurnments"

    displayFormName = 'ColumbariumFormDisplay'
    metaName = 'ColumbariumMetaData'

    data.meta = model.DynamicDataFromJson(model.Content(metaName))
    data.displayForm = model.Content(displayFormName)
    data.htmlRecordDeleted = model.Content(data.htmlRecordDeletedName)

    lookupDataSql = "select * from custom.ColumbariumLookup"
    data.lookupDataSqlFromCertificate = lookupDataSql + " where Certificate = %s"
    data.lookupDataSqlFromPeopleId = lookupDataSql + " where PeopleId = %s"
    data.lookupDataSqlFromNiche = ''' 
        select lu.* from custom.ColumbariumLookup lu
        join custom.ColumbariumNichePeople np on np.PeopleId = lu.PeopleId
        where np.NicheId = '%s'
    '''
    data.lookupNichesByPeopleId = "select NicheId from custom.ColumbariumLookupNiche where PeopleId = %s"
    data.lookupInurnmentByPeopleId = "select * from custom.ColumbariumInurnments where PeopleId = %s"
    data.urnicon = '<i class="glyphicon glyphicon-modal-window" style="color:red"></i>'
    data.pyscript = Data.pyscript
    data.operationType = Data.p1
    data.id = Data.p2
    if model.HttpMethod == "post":
        data.post = Data
    return data

def DisplayForm(lookupdata, data):
    peopleid = int(lookupdata.PeopleId)
    person = lookupdata.Json
    if not person and peopleid:
        # display a form for creating a new record
        return AddRecordForm(data)
    # add supplemental data that will be specially parsed during update
    person.Certificate = lookupdata.LegalCertificate
    person.Niches = lookupdata.LegalNicheIds
    person.InurnmentDate = lookupdata.InurnmentDate
    person.OfficiatedBy = lookupdata.OfficiatedBy
    personLink = PersonLink(data, lookupdata)
    rows = model.BuildDisplayRows(person, data.meta)
    if rows == None:
        return "not found"
    return data.displayForm.format(
        p = personLink,
        r = rows, 
        pid = peopleid, 
        scriptname = data.pyscript)

def PersonLink(data, lookupdata):
    record = lookupdata.Json
    icon = data.urnicon if record.InurnmentDate or record.OfficiatedBy else ''
    return '<a href="/Person2/{}" target="person">{}</a> {}'.format(data.id, lookupdata.Name, icon)

def LookupByPeopleId(peopleid):
    sql = data.lookupDataSqlFromPeopleId % peopleid
    return model.SqlListDynamicData(sql, data.meta)
def FetchPerson(peopleid):
    sql = data.lookupDataSqlFromPeopleId % peopleid
    return model.SqlTop1DynamicData(sql, data.meta)
def LookupByCertificate(certificate):
    sql = data.lookupDataSqlFromCertificate % certificate
    return model.SqlListDynamicData(sql, data.meta)
def LookupByNiche(nicheid):
    sql = data.lookupDataSqlFromNiche % nicheid
    return model.SqlListDynamicData(sql, data.meta)
def LookupNichesByPeopleId(peopleid):
    sql = data.lookupNichesByPeopleId % peopleid
    return model.SqlListDynamicData(sql)
def FetchInurnment(peopleid):
    sql = data.lookupInurnmentByPeopleId % peopleid
    return model.SqlTop1DynamicData(sql)

def CacheCertificate(certificate):
    if certificate:
        model.SetCacheVariable("LastViewedColumbariumCertificate", certificate)

def LookupData(data):
    if data.operationType == 'certificate': # people associated with certificate
        CacheCertificate(data.id)
        return LookupByCertificate(data.id)
    elif data.operationType == 'niche': # people associated with niche
        return LookupByNiche(data.id)
    elif data.operationType == 'person': # people associated with certificate via person
        # get certificate associated with person
        c = FetchPerson(data.id)
        if c != None:
            if c.Certificate:
                CacheCertificate(c.Certificate)
                return LookupByCertificate(c.Certificate)
            else:
                return LookupByPeopleId(data.id)
        return model.DynamicDataFromJsonArray('[{"PeopleId": %s}]' % data.id)
    elif data.operationType in ['add','edit','update','cancel']:
        # post operations always use single person
        return FetchPerson(data.id)

def EditForm(data):
    lookupdata = LookupData(data)
    record = lookupdata.Json
    # add three special properties to person
    # (not part of the ColumbariumPeople schema) and they will be updated with special code
    record.PeopleId = lookupdata.PeopleId
    record.Certificate = lookupdata.Certificate
    record.Niches = lookupdata.Niches
    record.InurnmentDate = lookupdata.InurnmentDate
    record.OfficiatedBy = lookupdata.OfficiatedBy

    rows = model.BuildFormRows(record, data.meta)
    if rows == None:
        return ""
    editForm = model.Content(data.editFormName)
    personLink = PersonLink(data, lookupdata)
    return editForm.format(
        p = personLink,
        r = rows,
        p2 = data.id,
        scriptname = data.pyscript)

def UpdateNiches(data, lookupdata):
    oldvalue = lookupdata.Niches
    newvalue = data.post.Niches
    # before and after lists of Niches
    oldList = filter(None, oldvalue.replace(' ','').split(','))
    newList = filter(None, newvalue.replace(' ','').split(','))
    # use Python sets for comparing lists to get deletes and adds
    oldSet = set(oldList)
    newSet = set(newList) if newvalue else set()
    if newSet == oldSet: # easy comparision for equal sets
        return
    deletes = oldSet.difference(newSet) # items in oldSet not in newSet
    adds = newSet.difference(oldSet) # items in newSet not in oldSet

    for nicheid2 in deletes:
        nicheid = GetNicheId(nicheid2)
        model.DeleteJsonRecord(data.NicheSection, data.id, nicheid, nicheid2)
    for nicheid2 in adds:
        nicheid = GetNicheId(nicheid2)
        model.AddUpdateJsonRecord('', data.NicheSection, data.id, nicheid, nicheid2)

def GetNicheId(nicheid2):
    x = nicheid2.split('-')
    if len(x) == 1:
        return nicheid2
    return '{}-{}'.format(x[0],x[1])

def UpdateInurnment(data, lookupdata):
    i = FetchInurnment(data.id)
    nlist = data.post.Niches.replace(' ','').split(',')
    if data.post.InurnmentDate or data.post.OfficiatedBy: 
        if not i: # create new Inurnment record
            i = model.DynamicData()
        i.OfficiatedBy = data.post.OfficiatedBy
        i.InurnmentDate = data.post.InurnmentDate
        model.AddUpdateJsonRecord(i, data.InurnmentSection, data.id, nlist[0])
    else: # no date nor officatedby
        if i: # remove existing Inurnment
            model.DeleteJsonRecord(data.InurnmentSection, data.id, nlist[0])

def CheckDelete(data):
    if (data.post.Notation == 'DELETE'  
            and not data.post.Certificate 
            and not data.post.Niches 
            and not data.post.InurnmentDate 
            and not data.post.OfficiatedBy):
        model.DeleteJsonRecord(data.PeopleSection, data.id)
        return True
    return False

def UpdateRecord(data):
    lookupdata = LookupData(data)
    if lookupdata == None:
        return data.htmlRecordDeleted
    record = lookupdata.Json

    # update all the standard ColumbariumPeople properties
    for k in record.Keys(data.meta):
        # post[k] is the individual property passed in via HttpPost
        if k == 'Certificate' and data.post[k] == '': # remove empty Certificate
            record.Remove('Certificate')
        else:
            record.SetValue(k, data.post[k])

    # update the special properties not part of the standard ColumbariumPeople properties
    UpdateNiches(data, lookupdata)
    UpdateInurnment(data, lookupdata)
    if CheckDelete(data):
        return data.htmlRecordDeleted

    model.AddUpdateJsonRecord(record, "ColumbariumPeople", data.id)
    lookupdata = LookupData(data) # call again to get refreshed data
    return DisplayForm(lookupdata, data) # display the modified record

def AddRecordForm(data):
    addNewRecordForm = model.Content(data.addNewRecordFormName)
    nextCertificate = q.QuerySqlInt("select NextAvailableCertificate from custom.ColumbariumNextCertificate")
    lastViewedCertificate = model.GetCacheVariable("LastViewedColumbariumCertificate")
    lastViewedCertificateHtml = ""
    if lastViewedCertificate:
        lastViewedCertificateHtml = "<br>Last Viewed Certificate = <b>%s</b>" % lastViewedCertificate 
    name = q.QuerySqlStr("select Name from dbo.People where PeopleId = %s" % data.id)
    return addNewRecordForm.format(
        person = name,
        next = nextCertificate,
        last = lastViewedCertificateHtml,
        peopleid = int(data.id), 
        scriptname = data.pyscript)

def AddRecord(data):
    obj = model.DynamicData()
    obj.PeopleId = int(data.id)
    obj.Certificate = data.post.Certificate
    model.AddUpdateJsonRecord(obj, data.PeopleSection, data.id)
    return "REDIRECT=" + data.redirect % data.id

def ProcessHttpGet(data):
    model.Script = model.Content(data.javascriptName)
    container = model.Content(data.htmlName)
    html = ""
    lookuplist = LookupData(data)
    if lookuplist == None:
        AddRecordForm(data)
    for info in lookuplist:
        form = DisplayForm(info, data)
        html += '\n<div class="columbarium">\n%s\n</div>\n' % form
    model.Form = container.replace("<!--INDIVIDUAL FORMS-->", html)

def ProcessHttpPost(data):
    if data.operationType == "add":
        print(AddRecord(data))
    elif data.operationType == "edit":
       print(EditForm(data)) 
    elif data.operationType == "update":
        print(UpdateRecord(data))
    elif data.operationType == "cancel":
        info = LookupData(data)
        print(DisplayForm(info, data))

if model.HttpMethod == 'get':
    data = Initialize()
    ProcessHttpGet(data)

elif model.HttpMethod == 'post':
    data = Initialize()
    ProcessHttpPost(data)
