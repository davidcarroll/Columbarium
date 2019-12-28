select	
	convert(int, Id1) PeopleId, 
	Id2 NicheId, 
	Id3 NicheId2, 
	LegalNicheId = formatmessage('%s-%03i-%s', 
		(select Value from dbo.Split(Id3, '-') where TokenId = 1),
		(select convert(int, Value) from dbo.Split(Id3, '-') where TokenId = 2),
		(select value from dbo.Split(Id3, '-') where TokenId = 3))
from custom.JsonDocumentRecords
where Section = 'ColumbariumNichePeople'