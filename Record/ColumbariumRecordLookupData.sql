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
