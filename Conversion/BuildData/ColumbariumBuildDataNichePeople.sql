with data as (
    select 
        [PeopleId],
		Niche = ltrim(Split.a.value('.', 'varchar(100)'))
    from  (
    select 
        PeopleId, 
        NicheList = 
            cast ('<m>' + replace([NicheNumber], ',', '</m><m>') + '</m>' as xml)
    from  imported.ColumbariumData
	where iif(len(dbo.RegexMatch(NicheNumber, '^[A-I]-\d*.*$'))>0, NicheNumber, null) is not null
	) aa cross apply NicheList.nodes ('/m') as split(a) 
), 
data2 as (
	select 
		NicheId = dbo.RegexMatch(Niche, '^.-') + dbo.RegexMatch(Niche, '[1-9]\d*'), 
		NichePart = (select value from dbo.Split(Niche, '-') where TokenID = 3), 
		PeopleId
	from data
)
select 
	NicheId, 
	NichePart, 
	PeopleId, 
	Niche = iif(NichePart is null, NicheId, formatmessage('%s-%s', NicheId, NichePart))
from data2
where data2.PeopleId is not null