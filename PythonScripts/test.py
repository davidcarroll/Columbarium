def GetIdAndPart(niche):
    x = niche.split('-')
    id = '{}-{}'.format(x[0],x[1])
    part = None
    if len(x) > 2:
        part = x[2]
    return (id, part)

(nicheid, nichepart) = GetIdAndPart("I-18-a")
print nicheid
print nichepart