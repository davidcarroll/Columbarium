select *
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumData'),
			'$.NichePeople')))
with (   
	NicheId varchar(50) '$.NicheId'
	,NichePart varchar(50) '$.NichePart'  
	,PeopleId int '$.PeopleId'
	,Niche varchar(50) '$.Niche'
	) 