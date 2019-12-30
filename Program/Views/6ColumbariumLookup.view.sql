select 
     j.Id1 PeopleId
     ,p.Name
	,cp.Certificate
	,cp.LegalCertificate
     ,j.Json
     ,Niches = isnull(stuff((
          select ', ' + np.NicheId2
               from custom.ColumbariumNichePeople np
               join custom.ColumbariumNiches n on n.NicheId = np.NicheId
               where PeopleId = j.Id1
               order by n.Wall, n.Row, n.Col, np.NicheId2
               for xml path('')), 1, 2, ''), '')
     ,LegalNicheIds = isnull(stuff((
          select ', ' + np.LegalNicheId 
               from custom.ColumbariumNichePeople np
               join custom.ColumbariumNiches n on n.NicheId = np.NicheId
               where PeopleId = j.Id1
               order by n.Wall, n.Row, n.Col, np.NicheId2
               for xml path('')), 1, 2, ''), '')
     ,i.InurnmentDate
     ,i.OfficiatedBy
from custom.JsonDocumentRecords j
join custom.ColumbariumPeople cp on cp.PeopleId = j.Id1
join dbo.People p on p.PeopleId = j.Id1
left join custom.ColumbariumInurnments i on i.PeopleId = j.Id1
where j.Section = 'ColumbariumPeople'