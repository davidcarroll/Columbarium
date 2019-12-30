select convert(int, Id1) PeopleId, Id2 NicheId, j.*
from custom.JsonDocumentRecords
     cross apply openjson(Json) with (
		InurnmentDate varchar(50)
		,OfficiatedBy varchar(50)
	) j
where Section = 'ColumbariumInurnments'