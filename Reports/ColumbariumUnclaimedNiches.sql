select Wall, n.NicheId from custom.ColumbariumNiches n
left join custom.ColumbariumNichePeople np on n.NicheId = np.NicheId
where np.NicheId is null