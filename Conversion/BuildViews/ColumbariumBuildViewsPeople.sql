select * 
from openjson((select json_query(
		(select Body from dbo.Content where Name = 'ColumbariumData'),
			'$.ColumbariumPeople')))
with (   
	PeopleId int '$.PeopleId'
	,Notation varchar(50) '$.Notation'
	,Spots int '$.Spots'
	,AmtPaid money '$.AmtPaid'
	,PurchasedBy varchar(50) '$.PurchasedBy'
	,Notes varchar(400) '$.Notes'
	,ContactName varchar(50) '$.ContactName'
	,ContactPhoneNo varchar(50) '$.ContactPhoneNo'
	,ContactRelation varchar(50) '$.ContactRelation'
	,[Certificate] varchar(25) '$.Certificate'
	) 