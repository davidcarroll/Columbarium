model.WriteContentPython("ColumbariumMenu", """
#Roles=Admin
def Menu():
    model.Title = "Columbarium Menu"
    rptSqlName = "ColumbariumRpt"
    rptUnclaimedNichesSqlName = "ColumbariumRptUnclaimedNiches"
    rptUnclaimedHalfNichesSqlName = "ColumbariumRptUnclaimedHalfNiches"
    rptCertificatesWithMultipleNichesSqlName = "ColumbariumRptCertificatesWithMultipleNiches"

    nicheWallsScriptName = "ColumbariumNicheWalls"
    mainScriptName = "ColumbariumRecord"
    buildDataScriptName = "ColumbariumBuildData"
    buildMetaScriptName = "ColumbariumBuildMetaData"
    buildNicheScriptName = "ColumbariumBuildNicheData"
    createViewsScriptName = "ColumbariumBuildViews"
    javascriptName = "PeopleSearchJavascript"
    keyword = "Columbarium"

    javascript = model.Content(javascriptName, keyword)
    link = "<a href='/PyScriptForm/%s/person/{0}' target='link'><b>{1}</b>{2}{3}{4}</a>" % mainScriptName
    model.Script = javascript.replace("{link}", link)

    print '''
    <div id="page-header" class="text-center"><h2>Columbarium Menu</h2></div>
    <div class="container-fluid" id="main">
        <div class="box-content">
            <div class="well" style="max-width: 350px; margin: auto;">
                Search by Name or PeopleId: <input id="pythonSearch" type="text" autocomplete="off" 
                    style="width: 14em; font-size: 14px; padding: 5px;" class="form-control input-sm" /><br>
                <a href="/PyScript/{}" target="walls">Niche Walls</a><br>
                <a href="/RunScript/{}" target="rpt">Columbarium Report</a><br>
                <a href="/RunScript/{}" target="rpt">Unclaimed Empty Niches</a><br>
                <a href="/RunScript/{}" target="rpt">Unclaimed Half Niches</a><br>
                <a href="/RunScript/{}" target="rpt">Certificates With Multiple Niches</a><br>
                <a href="/PyScript/{}">Re-Build Columbarium Niche Data</a><br>
    '''.format( nicheWallsScriptName, 
                rptSqlName, 
                rptUnclaimedNichesSqlName, 
                rptUnclaimedHalfNichesSqlName, 
                rptCertificatesWithMultipleNichesSqlName,
                buildNicheScriptName)
    print '</div></div></div>'

Menu()
""")
model.WriteContentSql("ColumbariumRpt", """
select 
     p.PeopleId
	,LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/person/%i', p.PeopleId)
	,pp.Name
	,LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/certificate/%s', p.[Certificate])
     ,p.[Certificate]
     ,p.Notation
     ,Contact = p.ContactName
          + '<br>' + p.ContactPhoneNo
          + '<br>' + p.ContactRelation
     ,n.NicheId
     ,n.NichePart
     ,i.InurnmentDate
     ,p.Notes
from custom.ColumbariumPeople p
left join dbo.People pp on pp.PeopleId = p.PeopleId
left join custom.NichePeople n on n.PeopleId = p.PeopleId
left join custom.Inurnments i on i.PeopleId = p.PeopleId 
order by p.Certificate desc, NicheId, n.NichePart
""")
model.WriteContentSql("ColumbariumRptCertificatesWithMultipleNiches", """
with nichecertificate as (
	select NicheId, cp.Certificate 
	from custom.ColumbariumPeople cp
	join custom.NichePeople np on np.PeopleId = cp.PeopleId
	group by np.NicheId, cp.Certificate
)
select 
	LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/certificate/%s', Certificate)
	,Certificate
	,count(*) Cnt
from nichecertificate
group by Certificate
having count(*) > 1
""")
model.WriteContentSql("ColumbariumRptUnclaimedNiches", """
select Wall, n.NicheId from custom.Niches n
left join custom.NichePeople np on n.NicheId = np.NicheId
where np.NicheId is null
""")
model.WriteContentSql("ColumbariumRptUnclaimedHalfNiches", """
select n.Wall, n.NicheId
from custom.NichePeople np
join custom.Niches n on n.NicheId = np.NicheId
group by n.NicheId, n.Wall
having count(*) = 1
""")
model.WriteContentText("PeopleSearchJavascript", """
$("#pythonSearch").autocomplete({
    appendTo: "#SearchResults2",
    autoFocus: true,
    minLength: 1,
    source: function (request, response) {
        // The search is handled by /PythonSearch/Names in c#
        $.post("/PythonSearch/Names", request, function (ret) {
            response(ret.slice(0, 10));
        }, "json");
    },
    select: function (event, ui) {
    }
}).data("uiAutocomplete")._renderItem = function (ul, item) {
    /* The {link} below (on line line 21) will be replaced 
       with the anchor tag using something like the following code in your Python script

       javascript = model.Content(javascriptName)
       link = "<a href='/PyScriptForm/%s/person/{0}'><b>{1}</b>{2}{3}{4}</a>" % mainScriptName
       model.Script = javascript.replace("{link}", link)
    */
    link = "{link}".format(item.Pid, item.Name, item.Spouse, item.Email, item.Addr);
    return $("<li>")
        .append(link)
        .appendTo(ul);
};

""")
model.WriteContentPython("ColumbariumBuildNicheData", """
#Roles=Admin

# Modify the following JSON data to specify your wall structures
WallData = '''
{
    "Walls": [
        {"name":'Fountain',"start":1,"end":12,"divider":6},
        {"name":'West Wall',"start":13,"end":34,"divider":23},
        {"name":'Phase 1B Large Wall',"start":35,"end":56},
        {"name":'Phase 1B Small Wall',"start":57,"end":65}
    ],
    "Rows": [
        'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A'
    ]
}
'''
data = model.DynamicDataFromJson(WallData)
data.Niches = []
for wall in data.Walls:
    for row in data.Rows:
        n = 0
        for col in range(wall.start, wall.end+1):
            niche = model.DynamicData()
            niche.NicheId = '{}-{}'.format(row, col)
            niche.Wall = wall.name
            niche.Row = row
            niche.Col = col
            n += 1
            if n == wall.divider:
                niche.Divider = True
            data.Niches.append(niche)

json = model.FormatJson(data)
model.WriteContent('ColumbariumNicheData', json, 'Columbarium')

""")
model.WriteContentSql("ColumbariumNicheLookupData", """
drop table if exists #inurned
select Niche, PeopleId into #inurned from custom.Inurnments
select 
    n.NicheId 
    ,[Certificate] = isnull(cp.Certificate, '')
    ,InurnedCnt = (select count(*) from #inurned where Niche = n.NicheId)
from custom.Niches n
left join custom.NichePeople np on np.NicheId = n.NicheId
left join custom.ColumbariumPeople cp on cp.PeopleId = np.PeopleId
group by n.NicheId, cp.Certificate, Wall, Col, Row
order by n.Wall, n.Row, n.Col
""")
model.WriteContentText("ColumbariumNicheStyle", """
<style> table.niche td>div { font-weight:bold;
        font-size: 10pt;
    }
    table.niche td {
        border: 1px solid #ddd;
        text-align: center;
        width:4em;
    }
    table.niche td i.glyphicon-modal-window {
        color: red;
    }
    table.niche td i.glyphicon-ok {
        color: green;
        font-size: 20px;
    }
    table.niche td>span{font-size:smaller}
</style>

""")
model.WriteContentPython("ColumbariumNicheWalls", """
#Roles=Admin
def Start():
    model.Title = "Columbarium Walls"
    data = model.DynamicData()
    docName = 'ColumbariumNicheData'
    styleName = "ColumbariumNicheStyle"
    lookupNicheDataSqlName = "ColumbariumNicheLookupData"
    nicheScriptName = 'ColumbariumNiche'
    mainScriptName = "ColumbariumRecord"
    keyword = "Columbarium"
    data.doc = model.DynamicDataFromJson(model.Content(docName, keyword))
    style = model.Content(styleName, keyword)
    lookupNicheDataSql = model.Content(lookupNicheDataSqlName, keyword)
    data.lookup = q.QuerySql(lookupNicheDataSql)

    data.nicheLink = '<a href="/PyScriptForm/%s/niche/{0}" target="link">{0}</a>' % mainScriptName
    certificateUrl = '/PyScriptForm/%s/certificate/{0}' % mainScriptName
    data.certificateLink = '<br><span><small><a href="%s" target="link">COL&#8209;{0}</a></small></span>' % certificateUrl

    print style
    print '<div><a href="/PyScript/ColumbariumMenu">Columbarium Menu</a></div>'
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
""")
model.WriteContentText("ColumbariumFormDisplay", """
<form class='form-horizontal display'>
    <fieldset>
        <div class="form-group">
            <label class="col-md-4 control-label">Record</label>
            <div class="col-md-4">
                <div class="form-control">{p}</div>
            </div>
        </div>
{r}
        <div class="form-group">
            <label class="col-md-4 control-label"></label>
            <div class="col-md-4">
                <button class="postOperation btn btn-primary">
                    Edit
                </button>
            </div>
        </div>
        <input type='hidden' name='pyscript' value='{scriptname}' />
        <input type='hidden' name='p1' value='edit' />
        <input type='hidden' name='p2' value='{pid}' />
    </fieldset>
</form>
""")
model.WriteContentText("ColumbariumFormEdit", """
<form class='form-horizontal'>
    <legend>Columbarium</legend>
    <fieldset>
{r}
        <div class="form-group">
            <label class="col-md-4 control-label"></label>
            <div class="col-md-4">
                <button class="postOperation btn btn-success">
                    Update
                </button>
                <button class="cancelupdate btn btn-default">
                    Cancel
                </button>
            </div>
        </div>
        <input type='hidden' name='p1' value='update' />
        <input type='hidden' name='p2' value='{p2}' />
        <input type='hidden' name='pyscript' value='{scriptname}' />
    </fieldset>
</form>
""")
model.WriteContentText("ColumbariumFormNewRecord", """
<form class="form-horizontal">
  <fieldset>
  <legend>New Columbarium Record</legend>
  
  <!-- Display Person to be Added -->
  <div class="form-group">
      <label class="col-md-4 control-label">Record</label>
      <div class="col-md-4">
          <div class="form-control">{person}</div>
      </div>
  </div>

  <!-- Enter Certificate Number -->
  <div class="form-group">
    <label class="col-md-4 control-label" for="textinput">Certificate</label>  
    <div class="col-md-4">
    <input id="textinput" name="Certificate" type="text" 
      placeholder="Enter Certificate number" class="form-control input-md">
    <span class="help-block">Next Available Certificate = <b>{next}</b>{last}</span>  
    </div>
  </div>
  
  <!-- Press Create -->
  <div class="form-group">
    <label class="col-md-4 control-label"></label>
    <div class="col-md-4">
      <button class="btn btn-primary postOperation">
          Create
      </button>
    </div>
  </div>

        <input type='hidden' name='p1' value='add' />
        <input type='hidden' name='p2' value='{peopleid}' />
        <input type='hidden' name='pyscript' value='{scriptname}' />
  </fieldset>
</form>
    
""")
model.WriteContentPython("ColumbariumRecord", """
#Roles=Admin

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

    data.doc = model.DynamicDataFromJson(model.Content(data.docName))
    data.meta = model.DynamicDataFromJson(model.Content(metaName))
    data.displayForm = model.Content(displayFormName, keyword)

    lookupDataSql = model.Content(lookupDataSqlName, keyword)
    data.lookupDataSqlFromCertificate = lookupDataSql + " where Certificate = '%s'"
    data.lookupDataSqlFromPeopleId = lookupDataSql + " where cp.PeopleId = %s"
    data.lookupDataSqlFromNiche = lookupDataSql + ''' 
        where exists(
            select null from custom.NichePeople 
            where PeopleId = cp.PeopleId and NicheId = '%s')
    '''
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

""")
model.WriteContentText("ColumbariumRecordDeleted", """
<div class="columbarium">
    <form class="form-horizontal display">
        <fieldset>
            <div class="form-group">
                <label class="col-md-4 control-label"></label>
                <div class="col-md-4">
                    <div class="form-control alert alert-danger">Columbarium Record Deleted</div>
                </div>
            </div>
        </fieldset>
    </form>
</div>
""")
model.WriteContentText("ColumbariumRecordHtml", """
<style>
    div.columbarium form.display div.form-group { margin-bottom:initial }
    div.columbarium form.display div.form-control { border:none }
    div.columbarium form.display div.form-control { height:initial }
    div.columbarium form.display div.form-control { min-height:15px }
    div.columbarium textarea.form-control { height:90px }
    div.columbarium input.form-control { height:initial }
    div.columbarium input.form-control { padding: 3px 12px }
</style>
<!--forms go here-->
""")
model.WriteContentText("ColumbariumRecordJavascript", """
$(function () {
    $('body').on('click', 'button.postOperation', function(ev){
        ev.preventDefault();
        var container = $(this).closest("div.columbarium")
        var q = $(container).find("form").serialize();
        $.post("/PyScriptForm", q, function (ret) {
            $(container).html(ret);
        });
        return false;
    });
    $('body').on('click', 'button.cancelupdate', function(ev){
        ev.preventDefault();
        var container = $(this).closest("div.columbarium")
        $(container).find("input[name=p1]").val('cancel')
        var q = $(container).find("form").serialize();
        $.post("/PyScriptForm", q, function (ret) {
            $(container).html(ret);
        });
        return false;
    });
});

""")
model.WriteContentSql("ColumbariumRecordLookupData", """
select 
     cp.PeopleId
     ,p.Name
     ,cp.Certificate
     ,Niches = stuff((
          select ',' + Niche
               from custom.NichePeople
               where PeopleId = cp.PeopleId
               group by Niche
               for xml path('')), 1, 1, '')
     ,i.InurnmentDate
     ,i.OfficiatedBy
from custom.ColumbariumPeople cp
join dbo.People p on p.PeopleId = cp.PeopleId
left join custom.Inurnments i on i.PeopleId = cp.PeopleId

""")
model.WriteContentSql("ColumbariumRecordNextCertificate", """
select top 1 Certificate + 1 NextAvailableCertificate 
from custom.ColumbariumPeople 
order by convert(int, Certificate) desc

""")
model.CreateCustomView("Inurnments", """
select * 
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumData'),
			'$.Inurnments')))
with (   
	Niche varchar(200) '$.Niche'  
	,PeopleId int '$.PeopleId'
	,InurnmentDate varchar(50) '$.InurnmentDate'
	,OfficiatedBy varchar(50) '$.OfficiatedBy'
	) 
""")
model.CreateCustomView("NichePeople", """
select *
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumData'),
			'$.NichePeople')))
with (   
	NicheId varchar(50) '$.NicheId'
	,NichePart varchar(50) '$.NichePart'  
	,PeopleId int '$.PeopleId'
	,Niche varchar(50) '$.Niche'
	) 
""")
model.CreateCustomView("Niches", """
select * 
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumNicheData'),
		 '$.Niches'))) 
with (   
	NicheId varchar(20) '$.NicheId'
	,[Row] varchar(50) '$.Row'
	,Col int '$.Col'
	,Wall varchar(200)'$.Wall'
 ) 
""")
model.CreateCustomView("ColumbariumPeople", """
select * 
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumData'),
			'$.ColumbariumPeople')))
with (   
	PeopleId int '$.PeopleId'
	,Notation varchar(50) '$.Notation'
	,Spots int '$.Spots'
	,AmtPaid money '$.AmtPaid'
	,PurchasedBy varchar(50) '$.PurchasedBy'
	,Notes varchar(400) '$.Notes'
	,ContactName varchar(50) '$.ContactName'
	,ContactPhoneNo varchar(50) '$.ContactPhoneNo'
	,ContactRelation varchar(50) '$.ContactRelation'
	,[Certificate] varchar(25) '$.Certificate'
	) 
""")
