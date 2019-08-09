base = 'C:/dev/Columbarium/Conversion/ColumbariumBuildViews'
model.CreateCustomView("Niches", model.Content(base + "Niches.sql"))
model.CreateCustomView("Inurnments", model.Content(base + "Inurnments.sql"))
model.CreateCustomView("NichePeople", model.Content(base + "NichePeople.sql"))
model.CreateCustomView("ColumbariumPeople", model.Content(base + "People.sql"))