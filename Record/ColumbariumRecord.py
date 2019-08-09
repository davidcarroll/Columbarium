# Note:
# Two people cannot be editing any part of the columbarium data at the same time
# as one will clobber the other's changes.

def Initialize():
    model.Title = "Columbarium Record"
    #avoid using global data so debugging can examine all variables
    data = model.DynamicData()

    # names of all the records stored in Special Content records
    data.docName = 'ColumbariumData'
    data.editFormName = 'ColumbariumFormEdit'
    data.addNewRecordFormName = 'ColumbariumFormNewRecord'
    data.javascriptName = 'ColumbariumRecordJavascript'
    data.htmlName = 'ColumbariumRecordHtml'
    data.htmlRecordDeletedName = 'ColumbariumRecordDeleted'
    data.nextCertificateSqlName = 'ColumbariumRecordNextCertificate'
    data.redirect = '/PyScriptForm/ColumbariumRecord/person/%s'
    keyword = "Columbarium"
    data.keyword = keyword

    displayFormName = 'ColumbariumFormDisplay'
    metaName = 'ColumbariumDataMeta'
    lookupDataSqlName = 'ColumbariumRecordLookupData'

    if model.IsDebug:
        base = "c:/dev/columbarium/"
        data.addNewRecordFormName = base + "Record/%s.text.html" % data.addNewRecordFormName
        data.editFormName = base + "Record/%s.text.html" % data.editFormName
        data.javascriptName = base + "Record/%s.js" % data.javascriptName
        data.htmlName = base + 'Record/%s.text.html' % data.htmlName
        data.htmlRecordDeletedName = base + 'Record/%s.text.html' % data.htmlRecordDeletedName
        data.nextCertificateSqlName = base + 'Record/%s.sql' % data.nextCertificateSqlName
        data.redirect = '/PyScriptForm/c!dev-Columbarium-Record-ColumbariumRecord.py/person/%s'
        lookupDataSqlName = base + 'Record/%s.sql' % lookupDataSqlName
        displayFormName = base + "Record/%s.text.html" % displayFormName
        metaName = base + "Data/%s.json" % metaName
        data.docName = base + "Data/%s.json" % data.docName

    data.doc = model.DynamicDataFromJson(model.Content(data.docName))
    data.meta = model.DynamicDataFromJson(model.Content(metaName))
    data.displayForm = model.Content(displayFormName, keyword)

    lookupDataSql = model.Content(lookupDataSqlName, keyword)
    data.lookupDataSqlFromCertificate = lookupDataSql + " where Certificate = '%s'"
    data.lookupDataSqlFromPeopleId = lookupDataSql + " where cp.PeopleId = %s"
    data.lookupDataSqlFromNiche = lookupDataSql + """ 
        where exists(
            select null from custom.NichePeople 
            where PeopleId = cp.PeopleId and NicheId = '%s')
    """
    data.urnicon = '<i class="glyphicon glyphicon-modal-window" style="color:red"></i>'
    data.pyscript = Data.pyscript
    data.operationType = Data.p1
    data.id = Data.p2
    if model.HttpMethod == "post":
        data.postdata = Data
    return data

def FindElement(array, peopleid):
    # Finds object from an array of objects using peopleid
    # The array can be either ColumbariumPeople or Inurnments
    # Returns the first element matched or None if not found
    return next((i for i in array if i.PeopleId == peopleid), None)

def FindMatchingList(array, peopleid):
    # uses filter to reduce large list to small list using peopleid
    pid = int(peopleid)
    li = filter(lambda x: (x.PeopleId == pid), array)
    return list(li)

def DisplayForm(lookupdata, data):
    peopleid = int(lookupdata.PeopleId)
    person = FindElement(data.doc.ColumbariumPeople, peopleid)
    if person == None and peopleid:
        # display a form for creating a new record
        return AddRecordForm(data)
    # add supplemental data that will be specially parsed during update
    person.Niches = lookupdata.Niches
    person.InurnmentDate = lookupdata.InurnmentDate
    person.OfficiatedBy = lookupdata.OfficiatedBy
    icon = data.urnicon if person.InurnmentDate or person.OfficiatedBy else ''
    personLink = '<a href="/Person2/{}">{}</a> {}'.format(peopleid, lookupdata.Name, icon)
    rows = model.BuildDisplayRows(person, data.meta.ColumbariumPeople)
    if rows == None:
        return "not found"
    return data.displayForm.format(
        p = personLink,
        r = rows, 
        pid = peopleid, 
        scriptname = data.pyscript)

def CacheCertificate(certificate):
    if certificate:
        model.SetCacheVariable("LastViewedColumbariumCertificate", certificate)

def LookupData(data):
    if data.operationType == 'certificate': # people associated with certificate
        CacheCertificate(data.id)
        return q.QuerySql(data.lookupDataSqlFromCertificate % data.id)
    elif data.operationType == 'niche': # people associated with niche
        return q.QuerySql(data.lookupDataSqlFromNiche % data.id)
    elif data.operationType == 'person': # people associated with certificate via person
        # get certificate associated with person
        c = q.QuerySqlTop1(data.lookupDataSqlFromPeopleId % data.id) 
        if c != None:
            if c.Certificate:
                CacheCertificate(c.Certificate)
                return q.QuerySql(data.lookupDataSqlFromCertificate % c.Certificate)
            else:
                return q.QuerySql(data.lookupDataSqlFromPeopleId % data.id)
        return model.DynamicDataFromJsonArray('[{"PeopleId": %s}]' % data.id)
    elif data.operationType in ['add','edit','update','cancel']:
        # post operations always use single person
        return q.QuerySqlTop1(data.lookupDataSqlFromPeopleId % data.id)

def EditForm(data):
    lookupdata = LookupData(data)
    peopleid = int(data.id)
    person = FindElement(data.doc.ColumbariumPeople, peopleid)
    # add three properties found in separeate table 
    # (not part of the ColumbariumPeople schema) and they will be updated with special code
    person.Niches = lookupdata.Niches
    person.InurnmentDate = lookupdata.InurnmentDate
    person.OfficiatedBy = lookupdata.OfficiatedBy

    rows = model.BuildFormRows(person, data.meta.ColumbariumPeople)
    if rows == None:
        return ""
    editForm = model.Content(data.editFormName, data.keyword)
    return editForm.format(
        r = rows,
        p2 = peopleid,
        scriptname = data.pyscript)

def UpdateNiches(newvalue, data):
    nichepeople = data.doc.NichePeople
    peopleid = int(data.id)
    # before and after lists of Niches
    oldList = FindMatchingList(nichepeople, peopleid)
    oldList = model.ElementList(oldList, "Niche") # pulls single attributes from json objects
    newList = newvalue.replace(' ','').split(',')
    # use Python sets for comparing lists to get deletes and adds
    oldSet = set(oldList)
    newSet = set(newList) if newvalue else set()
    if newSet == oldSet: # easy comparision for equal sets
        return
    deletes = oldSet.difference(newSet) # items in oldSet not in newSet
    adds = newSet.difference(oldSet) # items in newSet not in oldSet

    for deleteniche in deletes:
        index = next((i for i, o in enumerate(nichepeople) if o.PeopleId == peopleid and o.Niche == deleteniche), -1)
        nichepeople.RemoveAt(index)
    for addniche in adds:
        if not addniche:
            continue
        obj = model.DynamicData()
        x = addniche.split('-')
        obj.NicheId = '{}-{}'.format(x[0],x[1])
        if len(x) > 2:
            obj.NichePart = x[2]
        obj.PeopleId = peopleid
        obj.Niche = addniche
        nichepeople.Insert(0, obj)

def UpdateInurnment(data):
    post = data.postdata
    peopleid = int(data.id)
    i = FindElement(data.doc.Inurnments, peopleid)
    if post.InurnmentDate or post.OfficiatedBy: 
        if not i: # create new Inurnment record
            i = model.DynamicData()
            i.PeopleId = peopleid
            data.doc.Inurnments.Insert(0, i)
        i.Niche = post.Niches
        i.OfficiatedBy = post.OfficiatedBy
        i.InurnmentDate = post.InurnmentDate
    else: # no date nor officatedby
        if i: # remove existing Inurnment
            data.doc.Inurnments.Remove(i)

def CheckDelete(data):
    post = data.postdata
    if (post.Notation == 'DELETE'  
            and not post.Certificate 
            and not post.Niches 
            and not post.InurnmentDate 
            and not post.OfficiatedBy):
        peopleid = int(data.id)
        people = data.doc.ColumbariumPeople
        i = next((i for i, item in enumerate(people) if item.PeopleId == peopleid), -1)
        people.RemoveAt(i)
        model.WriteContent(data.docName, str(data.doc))
        return True
    return False

def UpdateRecord(data):
    lookupdata = LookupData(data)
    peopleid = int(data.id)
    post = data.postdata
    record = FindElement(data.doc.ColumbariumPeople, peopleid)

    # update all the standard ColumbariumPeople properties
    for k in record.Keys(data.meta.ColumbariumPeople):
        # post[k] is the individual property passed in via HttpPost
        if k == 'Certificate' and post[k] == '': # remove empty Certificate
            record.Remove('Certificate')
        else:
            record.SetValue(k, post[k])

    # update the special properties not part of the standard ColumbariumPeople properties
    UpdateNiches(post.Niches, data)
    UpdateInurnment(data)
    if CheckDelete(data):
        return model.Content(data.htmlRecordDeletedName, data.keyword)

    model.WriteContent(data.docName, str(data.doc)) # save the modified document
    lookupdata = LookupData(data) # call again to get refreshed data
    return DisplayForm(lookupdata, data) # display the modified record

def AddRecordForm(data):
    addNewRecordForm = model.Content(data.addNewRecordFormName, data.keyword)
    nextCertificate = q.QuerySqlInt(model.Content(data.nextCertificateSqlName, data.keyword))
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
    obj.Certificate = data.postdata.Certificate
    data.doc.ColumbariumPeople.Insert(0, obj)
    model.WriteContent(data.docName, str(data.doc))
    return "REDIRECT=" + data.redirect % data.id

def ProcessHttpGet(data):
    model.Script = model.Content(data.javascriptName, data.keyword)
    html = model.Content(data.htmlName, data.keyword)
    lookuplist = LookupData(data)
    for info in lookuplist:
        form = DisplayForm(info, data)
        html += '\n<div class="columbarium">\n%s\n</div>\n' % form
    model.Form = html

def ProcessHttpPost(data):
    if data.operationType == "add":
        print AddRecord(data)
    elif data.operationType == "edit":
        print EditForm(data)
    elif data.operationType == "update":
        print UpdateRecord(data)
    elif data.operationType == "cancel":
        info = LookupData(data)
        print DisplayForm(info, data)

if model.HttpMethod == 'get':
    data = Initialize()
    ProcessHttpGet(data)

elif model.HttpMethod == 'post':
    data = Initialize()
    ProcessHttpPost(data)
