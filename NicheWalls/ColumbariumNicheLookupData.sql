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