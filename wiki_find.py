import wikipedia
import requests
import re
import os, os.path

def logo_guess(team, guessword="football"):
    p = wikipedia.page(wikipedia.search("%s %s" % (team, guessword))[0])
    print "found page %s" % p.title
    files = re.findall('<table[^\n]*?vcard.*?a href="(/wiki/File.*?)" class="image".*?</table>', p.html(), re.S)
    imagepage = "http://en.wikipedia.org" + files[0]
    r = requests.get(imagepage)
    fullimage = re.findall(r'fullImageLink.*?href="(.*?)".*?/div', r.content, re.S)
    assert fullimage[0].startswith("//")
    return 'http:' + fullimage[0]

def download(image_url, image_name):
    cmd = "wget %s -O '%s' > /dev/null 2>&1 &" % (image_url, image_name)
    print cmd
    os.system(cmd)

def exceptions(team):
    if 'Bor Dort' in team: return 'Borussia Dortmund'
    if 'monchenglad' in team.lower(): return 'Borussia Monchengladbach'
    if 'Hamburg' in team: return 'Hamburger SV'
    if 'nurnberg' in team.lower(): return 'FC Nurnberg'
    if 'valencia' in team.lower(): return 'Valencia CF'
    return team

def get(team):
    team = exceptions(team)

    #if we already have it, bail
    for extension in ["svg", "png"]:
        filename = "wikicrests/%s.%s" % (team, extension)
        if os.path.isfile(filename):
            print "found %s already" % team
            return

    try:
        logo_file = logo_guess(team)
    except IndexError:
        try:
            logo_file = logo_guess(team, "club")
        except IndexError:
            print "unable to get logo for team %s" % team
            return

    extension = re.split('\.', logo_file)[-1]
    filename = "wikicrests/%s.%s" % (team, extension)
    download(logo_file, filename)

if __name__=="__main__":
    import csv
    with open("teamnames.txt") as f:
        for team in f:
            team = team.strip()
            print team
            get(team)
    #print logo_guess('betis')
    #print logo_guess('juventus')
    #print logo_guess('botafogo')
