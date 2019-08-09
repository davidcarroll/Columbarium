select 
    People = (select count(*) from custom.ColumbariumPeople)
    ,Inurnments = (select count(*) from custom.Inurnments)
    ,Niches = (select count(*) from custom.Niches)
