with data as (
	select 
		PeopleId
	    ,[Certificate] = 
            isnull(dbo.RegexMatch(CertificateNumber, '[1-9]\d*'), '0')
        ,CertificateNumber as OriginalCertificateNumber
	from imported.ColumbariumData
),
peopledata as (
	select 
		PeopleId
		,[Certificate]
	    ,OriginalCertificateNumber
		,[RefersTo] = case [Certificate]
	            when 27 then 144
	            when 76 then 77
	            else null
	        end
	from data
)
select 
    cd.PeopleId
    ,Spots = dbo.RegexMatch(Spots, '[1-9]\d*')
    ,convert(decimal, replace(AmtPaid, ',', '')) AmtPaid
    ,PurchasedBy
    ,Notes
    ,ContactName
    ,ContactPhoneNo
    ,ContactRelation
	,cp.Certificate
--	,cd.NicheNumber
	,Notation = case
		 when dbo.RegexMatch(Spots, '[1-9]\d*') is null and Spots <> '0' and len(Spots) > 0
		 	then Spots
		 when dbo.RegexMatch(NicheNumber, '^[A-I]-\d*.*$') is null and len(NicheNumber) > 0 
		 	then NicheNumber
	     else null
	 end	 
from imported.ColumbariumData cd
join peopledata cp on cp.PeopleId = cd.PeopleId
order by cp.Certificate