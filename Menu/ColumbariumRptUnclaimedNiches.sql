select Wall, n.NicheId from custom.Niches n
left join custom.NichePeople np on n.NicheId = np.NicheId
where np.NicheId is null