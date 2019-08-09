select n.Wall, n.NicheId
from custom.NichePeople np
join custom.Niches n on n.NicheId = np.NicheId
group by n.NicheId, n.Wall
having count(*) = 1