select 'View' [Type], s.name [Schema], v.name [Name]
from sys.views v
join sys.schemas s on s.schema_id = v.schema_id
where s.name = 'custom'

union 

select 'Table',  s.name, t.name
from sys.tables t
join sys.schemas s on s.schema_id = t.schema_id
where s.name = 'imported'