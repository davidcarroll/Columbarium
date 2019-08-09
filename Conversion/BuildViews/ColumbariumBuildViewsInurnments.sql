select * 
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumData'),
			'$.Inurnments')))
with (   
	Niche varchar(200) '$.Niche'  
	,PeopleId int '$.PeopleId'
	,InurnmentDate varchar(50) '$.InurnmentDate'
	,OfficiatedBy varchar(50) '$.OfficiatedBy'
	) 