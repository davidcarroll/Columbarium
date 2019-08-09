select * 
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumDataNiche'),
		 '$.Niches'))) 
with (   
	NicheId varchar(20) '$.NicheId'
	,[Row] varchar(50) '$.Row'
	,Col int '$.Col'
	,Wall varchar(200)'$.Wall'
 ) 