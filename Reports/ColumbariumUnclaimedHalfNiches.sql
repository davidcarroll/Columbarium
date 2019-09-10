select n.Wall, n.NicheId
from custom.ColumbariumNichePeople np
join custom.ColumbariumNiches n on n.NicheId = np.NicheId
group by n.NicheId, n.Wall
having count(*) = 1