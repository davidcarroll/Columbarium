with nichecertificate as (
	select NicheId, cp.Certificate 
	from custom.ColumbariumPeople cp
	join custom.ColumbariumNichePeople np on np.PeopleId = cp.PeopleId
	group by np.NicheId, cp.Certificate
)
select 
	LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/certificate/%s', Certificate)
	,Certificate
	,count(*) Cnt
from nichecertificate
group by Certificate
having count(*) > 1