select top 1 Certificate + 1 NextAvailableCertificate 
from custom.ColumbariumPeople 
order by convert(int, Certificate) desc
