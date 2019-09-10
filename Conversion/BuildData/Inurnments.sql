select 
  PeopleId 
  ,dbo.RegexMatch(NicheNumber, '^.-') + dbo.RegexMatch(NicheNumber, '[1-9]\d*') as NicheId
  ,OfficiatedBy
  ,InurnmentDate 
from imported.ColumbariumData
where len(InurnmentDate) > 0