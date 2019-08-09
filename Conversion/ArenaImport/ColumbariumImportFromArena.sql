drop table if exists #datatbl
drop table if exists #resultset
drop table if exists imported.ColumbariumData

if exists (select name from sys.schemas where name = 'imported')
	drop schema imported
go

create schema imported
go

declare @ProfileId int = 5955, @OrganizationId int = 1

	SELECT	RF.person_id
		, cpm.notes
		, F.title
		, rf.selected_value

	into #datatbl
	FROM ArenaRestoreDB.dbo.core_profile_member_field_value RF
	INNER JOIN ArenaRestoreDB.dbo.core_custom_field F ON F.custom_field_id = RF.custom_field_id
	inner join ArenaRestoreDB.dbo.core_profile_member cpm on rf.person_id=cpm.person_id and rf.profile_id=cpm.profile_id
	WHERE RF.[profile_id] = @ProfileId
	AND f.organization_id = @OrganizationId

select person_id, notes, 
	[Contact Name],[Officiated By],[Contact Phone No],[Niche #],[Urns Received], [# Spots],
	[Amt Paid],[Certificate Number],[Inurnment Date],[Purchased By],[Contact - Relation]
	into #resultset
	  FROM #datatbl
	  PIVOT (MIN(selected_value)
			FOR title IN ([Contact Name],[Officiated By],[Contact Phone No],[Niche #],[Urns Received],[# Spots],
			[Amt Paid],[Certificate Number],[Inurnment Date],[Purchased By],[Contact - Relation])) as PVTTable

select rs.person_id as ArenaId
	, p.PeopleId
     , rs.notes
     , rs.[Contact Name] ContactName
     , rs.[Officiated By] OfficiatedBy
     , rs.[Contact Phone No] ContactPhoneNo
     , rs.[Niche #] NicheNumber
     , rs.[Urns Received] UrnsReceived
     , rs.[# Spots] Spots
     , rs.[Amt Paid] AmtPaid
     , rs.[Certificate Number] CertificateNumber
     , rs.[Inurnment Date] InurnmentDate
     , rs.[Purchased By] PurchasedBy
     , rs.[Contact - Relation] ContactRelation
	 into imported.ColumbariumData
from #resultset rs
left outer join dbo.PeopleExtra pe on pe.Field = 'Arena Id' and pe.IntValue = rs.person_id
left join dbo.People p on p.PeopleId = pe.PeopleId
