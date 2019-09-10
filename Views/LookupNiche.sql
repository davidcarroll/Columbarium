select 
    n.NicheId 
    ,[Certificate] = isnull(cp.Certificate, '')
    ,InurnedCnt = (select count(*) from custom.ColumbariumInurnments i where i.NicheId = n.NicheId)
	,n.Wall
	,n.[Row]
	,n.Col
from custom.ColumbariumNiches n
left join custom.ColumbariumNichePeople np on np.NicheId = n.NicheId
left join custom.ColumbariumPeople cp on cp.PeopleId = np.PeopleId
group by n.NicheId, cp.Certificate, Wall, Col, Row