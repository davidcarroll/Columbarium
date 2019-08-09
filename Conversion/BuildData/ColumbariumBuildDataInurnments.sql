select 
  PeopleId 
  ,dbo.RegexMatch(NicheNumber, '^.-') + dbo.RegexMatch(NicheNumber, '[1-9]\d*') Niche
  ,OfficiatedBy
  ,InurnmentDate 
from imported.ColumbariumData
where len(InurnmentDate) > 0