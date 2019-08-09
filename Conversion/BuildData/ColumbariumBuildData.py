data = model.DynamicData()
base = "c:/dev/Columbarium/Conversion/BuildData/ColumbariumBuildData"

data.ColumbariumPeople = q.QuerySql(model.Content(base + "People.sql"))
data.Inurnments = q.QuerySql(model.Content(base + "Inurnments.sql"))
data.NichePeople = q.QuerySql(model.Content(base + "NichePeople.sql"))

json = model.FormatJson(data)
keyword = "Columbarium"
model.WriteContent('c:/dev/Columbarium/Data/ColumbariumData.json', json, keyword)