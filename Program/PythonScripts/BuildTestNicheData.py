# Modify the following JSON data to specify your wall structures
WallData = '''
{
    "Walls": [
        {"name":'First Wall',"start":1,"end":12,"divider":6},
        {"name":'Second Wall',"start":13,"end":34,"divider":23},
    ],
    "Rows": [
        'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A'
    ]
}
'''
data = model.DynamicDataFromJson(WallData)
data.Niches = []
for wall in data.Walls:
    for row in data.Rows:
        n = 0
        for col in range(wall.start, wall.end+1):
            niche = model.DynamicData()
            niche.NicheId = '{}-{}'.format(row, col)
            niche.Wall = wall.name
            niche.Row = row
            niche.Col = col
            n += 1
            if n == wall.divider:
                niche.Divider = True
            data.Niches.append(niche)

json = model.FormatJson(data)
model.WriteContent('ColumbariumNicheData', json, 'Columbarium')
