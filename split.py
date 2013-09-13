from PIL import Image
import re

fin = file("crests.css")
positions = re.findall("\.flair-(.*?)[,{].*?background-position:0 -(\d+)", fin.read())
prev = 0
current_image = 1
crests = Image.open('%s.png' % current_image)
width = 20
for team, offset in positions:
    #if the team name ends in -s2 -s3 -s4, chop it
    if re.search('-s\d', team):
        team = team[:-3]

    offset = int(offset)
    print team, offset, prev

    if offset != prev + 21:
        current_image += 1
        crests = Image.open('%s.png' % current_image)
        if current_image == 3:
            width = 40
        else:
            width = 20

    prev = offset

    crest = crests.crop((0, offset, width, offset + 20))
    crest.save('crests/%s.png' % team)
