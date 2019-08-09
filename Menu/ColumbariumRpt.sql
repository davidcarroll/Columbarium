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