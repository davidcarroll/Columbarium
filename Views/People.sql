select convert(int, Id1) as PeopleId, j.*
from custom.JsonDocumentRecords
     cross apply openjson(Json) with (
		 Spots nvarchar(100) 
		,AmtPaid decimal
		,PurchasedBy varchar(50)
		,Notes varchar(400)
		,ContactName varchar(50)
		,ContactPhoneNo varchar(50)
		,ContactRelation varchar(50)
		,[Certificate] varchar(25)
		) j
	where Section = 'ColumbariumPeople'