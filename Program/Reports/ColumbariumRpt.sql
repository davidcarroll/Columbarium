select 
     p.PeopleId
	,LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/person/%i', p.PeopleId)
	,pp.Name
	,LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/certificate/%s', p.[Certificate])
     ,p.LegalCertificate as Certificate
     ,Contact = p.ContactName
          + '<br>' + p.ContactPhoneNo
          + '<br>' + p.ContactRelation
     ,n.LegalNicheId as Niche
     ,i.InurnmentDate
     ,p.Notes
     --,n.LegalNicheId
     --,p.LegalCertificate
from custom.ColumbariumPeople p
left join dbo.People pp on pp.PeopleId = p.PeopleId
left join custom.ColumbariumNichePeople n on n.PeopleId = p.PeopleId
left join custom.ColumbariumInurnments i on i.PeopleId = p.PeopleId 
order by p.Certificate desc, NicheId2