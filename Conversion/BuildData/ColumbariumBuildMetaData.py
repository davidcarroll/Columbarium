MetaData = model.DynamicDataFromJson('''{
  "Inurnments": {
    "Niche": "str",
    "PeopleId": "readonly int",
    "OfficiatedBy": "str",
    "InurnmentDate": "date"
  },
  "ColumbariumPeople": {
    "PeopleId": "readonly int",
    "Notation": "str",
    "Spots": "int",
    "AmtPaid": "money",
    "PurchasedBy": "str",
    "Notes": "textarea",
    "ContactName": "str",
    "ContactPhoneNo": "str",
    "ContactRelation": "str",
    "Certificate": "str",
    "RefersTo": "int",
    "Niches": "special str",
    "InurnmentDate": "special str",
    "OfficiatedBy": "special str"
  }
}''')
json = model.FormatJson(MetaData)
model.WriteContent('C:/dev/Columbarium/data/ColumbariumDataMeta.json', json, 'Columbarium')
