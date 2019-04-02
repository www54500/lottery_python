from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
class Finalscore:
    def __init__(self, teamA, teamB, scoreA, scoreB):
        self.teamA = teamA
        self.teamB = teamB
        self.scoreA = scoreA
        self.scoreB = scoreB

def interpret (name):
    if (name == "塞爾蒂克"):
        return "Celtics"
    if (name == "籃網"):
        return "Nets"
    if (name == "尼克"):
        return "Knicks"
    if (name == "76人"):
        return "76ers"
    if (name == "暴龍"):
        return "Raptors"
    if (name == "公牛"):
        return "Bulls"
    if (name == "騎士"):
        return "Cavaliers"
    if (name == "活塞"):
        return "Pistons"
    if (name == "溜馬"):
        return "Pacers"
    if (name == "公鹿"):
        return "Bucks"
    if (name == "老鷹"):
        return "Hawks"
    if (name == "黃蜂"):
        return "Hornets"
    if (name == "熱火"):
        return "Heat"
    if (name == "魔術"):
        return "Magic"
    if (name == "巫師"):
        return "Wizards"
    if (name == "金塊"):
        return "Nuggets"
    if (name == "灰狼"):
        return "Timberwolves"
    if (name == "雷霆"):
        return "Thunder"
    if (name == "拓荒者"):
        return "Blazers"
    if (name == "爵士"):
        return "Jazz"
    if (name == "勇士"):
        return "Warriors"
    if (name == "快艇"):
        return "Clippers"
    if (name == "湖人"):
        return "Lakers"
    if (name == "太陽"):
        return "Suns"
    if (name == "國王"):
        return "Kings"
    if (name == "獨行俠"):
        return "Mavericks"
    if (name == "火箭"):
        return "Rockets"
    if (name == "灰熊"):
        return "Grizzlies"
    if (name == "鵜鶘"):
        return "Pelicans"
    if (name == "馬刺"):
        return "Spurs"
    else:
        return name
    
#chrome_options = Options()
#chrome_options.add_argument("--headless") # define headless
#browser = webdriver.Chrome(options = chrome_options)
browser = webdriver.Chrome()
today = time.strftime("%Y-%m-%d", time.localtime())
if (len(sys.argv) == 2):
    # mmddyy
    y = "20" + sys.argv[1][4:6]
    m = sys.argv[1][0:2]
    d = sys.argv[1][2:4]
    today = y + "-" + m + "-" + d
browser.get("https://tw.global.nba.com/scores/#!/" + today)
time.sleep(10)
page = browser.page_source
print("get page source")
browser.close()
soup = BeautifulSoup(page, "html.parser")
teamtable = soup.findAll("td", class_="team-abbrv") # all teams
scoretable = soup.findAll("td", class_="final-score") # final score
print("beautiful:" + str(len(teamtable)))
scores = []
score = Finalscore("", "", 0.0, 0.0)
count = 0
for i in range(0, len(teamtable)):
    count += 1
    if ("awayTeam" in teamtable[i].a["team"]):
        team = interpret(teamtable[i].a.string)
        #print("away team: {0}, final score: {1}".format(team, scoretable[i].span.string))
        score.teamA = team
        score.scoreA = float(scoretable[i].span.string)
    elif ("homeTeam" in teamtable[i].a["team"]):
        team = interpret(teamtable[i].a.string)
        #print("home team: {0}, final score: {1}".format(team, scoretable[i].span.string))
        score.teamB = team
        score.scoreB = float(scoretable[i].span.string)
    else:
        print("error: there is no \"away\" or \"home\" team")
    
    if (count % 2 == 0):
        scores.append(score)
        score = Finalscore("", "", 0, 0)

# today = "1992-11-16"
m = today[5:7]
d = today[8:10]
y = today[2:4]
folder = m + d + y + "\\"

flist = os.listdir(folder)
for f in flist:
    if ("result" in f):
        os.remove(folder + f)

for f in flist:
    if ("predict" in f):
        filer = open(folder + f, 'r', encoding = "utf8")
        datetim = f.split("_")[0]
        filew = open(folder + datetim + "_result.csv", 'a', encoding = "utf8")
        count = 0
        teamA = ""
        teamB = ""
        spread = 0.0
        oddsA = 0.0
        oddsB = 0.0
        total = 0.0
        oddsU = 0.0
        oddsO = 0.0

        for line in filer:
            words = line.split(",")
            filew.write(line)
            #print(line)
            if (count % 7 == 0): # team
                teamA = words[0]
                teamB = words[1].strip("\n")
                #print("team A:{0}, team B:{1}".format(teamA, teamB))

            if (count % 7 == 1): # spread, odds, total score of tw lottery
                spread = float(words[0])
                oddsA = float(words[2])
                oddsB = float(words[3])
                total = float(words[5])
                oddsU = float(words[6])
                oddsO = float(words[7])
                #print("spread: {0}, odds: [{1}, {2}]; total: {3}, odds:[{4}, {5}]".format(spread, oddsA, oddsB, total, oddsU, oddsO))

            if (count % 7 == 5): # check result of bet
                for s in scores:
                    if (s.teamA == teamA and s.teamB == teamB):
                        if (s.scoreA + spread > s.scoreB):
                            #print("team A win!")
                            content = "v, , , , ,"
                        else:
                            #print("team B win!")
                            content = " ,v, , , ,"
                        if (s.scoreA + s.scoreB < total):
                            print("{0} v.s. {1}, under the total score".format(teamA, teamB))
                            content += " ,v, "
                        else:
                            print("{0} v.s. {1}, over the total score".format(teamA, teamB))
                            content += " , ,v"
                        filew.write(content)

            count += 1
            
        filer.close()
        filew.close()
        
'''i = 1
while (i > 0):
    if (os.path.isfile(folder + "result.csv")):
        os.remove(folder + "result.csv")
    elif (os.path.isfile(folder + "result" + str(i) + ".csv")):
        os.remove(folder + "result" + str(i) + ".csv")
    if (os.path.isfile(folder + "predict" + str(i) + ".csv")): # multiple predict files
        filer = open(folder + "predict" + str(i) + ".csv", 'r', encoding = "utf8")
        filew = open(folder + "result" + str(i) + ".csv", 'a', encoding = "utf8")
    elif (os.path.isfile(folder + "predict.csv")): # single predict file
        filer = open(folder + "predict.csv", 'r', encoding = "utf8")
        filew = open(folder + "result.csv", 'a', encoding = "utf8")
        i = -1 # break
    else: # no file
        break
    count = 0
    teamA = ""
    teamB = ""
    spread = 0.0
    oddsA = 0.0
    oddsB = 0.0
    total = 0.0
    oddsU = 0.0
    oddsO = 0.0

    for line in filer:
        words = line.split(",")
        filew.write(line)
        #print(line)
        if (count % 7 == 0): # team
            teamA = words[0]
            teamB = words[1].strip("\n")
            #print("team A:{0}, team B:{1}".format(teamA, teamB))

        if (count % 7 == 1): # spread, odds, total score of tw lottery
            spread = float(words[0])
            oddsA = float(words[2])
            oddsB = float(words[3])
            total = float(words[5])
            oddsU = float(words[6])
            oddsO = float(words[7])
            #print("spread: {0}, odds: [{1}, {2}]; total: {3}, odds:[{4}, {5}]".format(spread, oddsA, oddsB, total, oddsU, oddsO))

        if (count % 7 == 5): # check result of bet
            for s in scores:
                if (s.teamA == teamA and s.teamB == teamB):
                    if (s.scoreA + spread > s.scoreB):
                        #print("team A win!")
                        content = "v, , , , ,"
                    else:
                        #print("team B win!")
                        content = " ,v, , , ,"
                    if (s.scoreA + s.scoreB < total):
                        print("{0} v.s. {1}, under the total score".format(teamA, teamB))
                        content += " ,v, "
                    else:
                        print("{0} v.s. {1}, over the total score".format(teamA, teamB))
                        content += " , ,v"
                    filew.write(content)

        count += 1
        
    filer.close()
    filew.close()
    i += 1'''
print("finish.")