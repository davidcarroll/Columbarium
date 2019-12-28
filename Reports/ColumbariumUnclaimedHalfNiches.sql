select n.Wall, n.LegalNicheId as NicheId
from custom.ColumbariumNichePeople np
join custom.ColumbariumNiches n on n.NicheId = np.NicheId
group by n.NicheId, n.LegalNicheId, n.Wall
having count(*) = 1