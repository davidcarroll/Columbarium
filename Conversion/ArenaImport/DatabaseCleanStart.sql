delete dbo.ContentKeyWords where Word like 'Columbarium'
delete dbo.Content where Name like '%Columbarium%'
delete dbo.Content where Name = 'PeopleSearchJavascript'
drop table if exists imported.ColumbariumData
drop view if exists custom.Niches
drop view if exists custom.Inurnments
drop view if exists custom.NichePeople
drop view if exists custom.ColumbariumPeople
