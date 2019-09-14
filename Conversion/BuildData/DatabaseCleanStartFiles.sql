drop table if exists #t
select name into #t
from dbo.Content c
join dbo.ContentKeyWords k on k.Id = c.Id
where k.Word = 'Columbarium'

delete dbo.ContentKeyWords where Word = 'Columbarium'
delete dbo.Content where name in (select name from #t)
drop table if exists #t

DROP view if exists [custom].[ColumbariumLookup]
DROP view if exists [custom].[ColumbariumLookupNiche]
DROP VIEW if exists [custom].[ColumbariumPeople]
DROP view if exists [custom].[ColumbariumInurnments]
DROP VIEW if exists [custom].[ColumbariumNextCertificate]
DROP view if exists [custom].[ColumbariumNichePeople]
DROP VIEW if exists [custom].[ColumbariumNiches]
