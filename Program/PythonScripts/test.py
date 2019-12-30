r = model.DynamicData()
r.PeopleId = 2
r.Contact = 'test'
s = r.ToFlatString()
print(s)