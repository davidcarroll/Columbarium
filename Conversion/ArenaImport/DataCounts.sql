select 
    People = (select count(*) from custom.ColumbariumPeople)
    ,Inurnments = (select count(*) from custom.ColumbariumInurnments)
    ,Niches = (select count(*) from custom.ColumbariumNiches)
