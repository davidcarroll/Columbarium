with nichecertificate as (
	select NicheId, cp.Certificate, cp.LegalCertificate 
	from custom.ColumbariumPeople cp
	join custom.ColumbariumNichePeople np on np.PeopleId = cp.PeopleId
	group by np.NicheId, cp.Certificate, cp.LegalCertificate
)
select 
	LinkForNext = formatmessage('/PyScriptForm/ColumbariumRecord/certificate/%s', nc.Certificate)
	,nc.LegalCertificate as [Certificate]
	,count(*) Cnt
from nichecertificate nc
group by nc.Certificate, nc.LegalCertificate
having count(*) > 1