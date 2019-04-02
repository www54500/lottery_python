import time
import sys
from datetime import date
from datetime import timedelta
class BetData:
    def __init__(self, teamA, teamB, spread, sOddsA, sOddsB, total, oddsU, oddsO):
        self.teamA = teamA
        self.teamB = teamB
        self.spread = spread
        self.sOddsA = sOddsA
        self.sOddsB = sOddsB
        self.total = total
        self.oddsU = oddsU
        self.oddsO = oddsO

class BetRatio:
    def __init__(self, teamA, teamB, spread, sRatio, total, tRatio):
        self.teamA = teamA
        self.teamB = teamB
        self.spread = spread
        self.sRatio = sRatio
        self.total = total
        self.tRatio = tRatio

def twLotteryAnalysis (file):
    countspread = 0
    counttotal = 0
    betdatas = []
    gtimes = []
    betdata = BetData("", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    for line in file:
        line = line.strip('\n')
        
        if ("@" in line):
            tmp = line.split(" ")
            gtime = tmp[len(tmp)-1]
            gtimes.append(gtime)
        
        if (countspread == 0 and counttotal == 0): # clear old data
            betdata = BetData("", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
        if (countspread == 2): # teamA and spread
            tmp = line.split('(')
            betdata.teamA = interpret(tmp[0].strip())
            betdata.spread = float(tmp[1][0:len(tmp[1])-1])

        if (countspread == 3): # spread odds of teamA 
            betdata.sOddsA = float(line)

        if (countspread == 4): # teamB
            tmp = line.split('(')
            betdata.teamB = interpret(tmp[0].strip())

        if (countspread == 5): # spread odds of teamB 
            betdata.sOddsB = float(line)

        if (counttotal == 2): # total
            tmp = line.split(' ')
            betdata.total = float(tmp[1])

        if (counttotal == 3): # over odds of total
            betdata.oddsO = float(line)

        if (counttotal == 5): # under odds of total
            betdata.oddsU = float(line)
            countspread = 0
            counttotal = 0
            betdatas.append(betdata)

        if (line == "讓分" or countspread != 0):
            countspread += 1

        if (line == "大小[總分]" or counttotal != 0):
            counttotal += 1
    file.close()
    return [betdatas, gtimes]

def bet365Analysis (file, dt):
    m = int(dt[0:2])
    d = int(dt[2:4])
    y = int("20" + dt[4:6])
    #today = time.strftime("%a %d %b", time.localtime())
    today = date(y, m, d).strftime("%a %d %b")
    tomorrow = (date(y, m, d) + timedelta(days = 1)).strftime("%a %d %b")
    count = 0
    first = 0
    phase = "none"
    betdatas = []
    betdata = BetData("", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) # teamA, teamB, spread, sOddsA, sOddsB, total, oddsU, oddsO
    t = 0
    for line in file:
        line = line.strip('\n')
        #print("{0}: {1}".format(t, line))
        
        if (line == "OTB"):
            count += 2
            continue
        
        if (line == "Money Line"):
            break

        if (line == today): 
            phase = "teams"
            count = 0
            continue

        if (line == tomorrow):
            phase = "none"
            continue

        if (line == "Spread"):
            if (not first): #is first
                count = 0
                first = 1
                phase = "spread"
                continue
            else:
                first = 0
                phase = "none"

        if (line == "Total"):
            if (first and phase == "total"): #is not first
                first = 0
                phase = "none"
            else:
                first = 1
                count = 0
                phase = "total"
                continue

        if (count % 2 == 0 and phase == "teams"): #teamA
            tmp = line.split(' ')
            if (len(tmp) < 2):
                continue
            betdata.teamA = tmp[len(tmp)-1]

        if (count % 2 == 1 and phase == "teams"): #teamB
            tmp = line.split(' ')
            if (len(tmp) < 2):
                continue
            betdata.teamB = tmp[len(tmp)-1]
            betdatas.append(betdata)
            betdata = BetData("", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        if (count % 4 == 0): #spread
            if (phase == "spread"):
                betdata = betdatas[count // 4] # a set has 4 elements
                betdata.spread = float(line)
            elif (phase == "total"):
                betdata = betdatas[count // 4]
                tmp = line.split(" ")
                try:
                    betdata.total = float(tmp[1])
                except IndexError as ie:
                    continue

        if (count % 4 == 1):
            if (phase == "spread"): #sOddsA
                betdata = betdatas[count // 4]
                betdata.sOddsA = float(line)
            elif (phase == "total"): #oddsO
                betdata = betdatas[count // 4]
                betdata.oddsO = float(line)

        if (count % 4 == 3):
            if (phase == "spread"): #sOddsB
                betdata = betdatas[count // 4]
                betdata.sOddsB = float(line)
            elif (phase == "total"): #oddsU
                betdata = betdatas[count // 4]
                betdata.oddsU = float(line)

        count += 1
        t += 1
        
    file.close()
    for b in reversed(betdatas):
        if (b.oddsU == 0.0 or b.oddsO == 0.0 or b.sOddsB == 0.0 or b.sOddsA == 0.0):
            print("[Warning] data of a bet may be empty.")
            sys.exit(0)
    return betdatas

def betRatio (file): #teamA, teamB, spread, sRatio, total, tRatio
    ratios = []
    ratio = BetRatio("", "", 0.0, 0.0, 0.0, 0.0)
    count = 0
    skip = 0
    for line in file:
        line = line.strip('\n')

        if (line == "FINAL"):
            skip = 1

        if (count == 2 and skip-1): # teamA
            tmp = line.split(' ')
            ratio.teamA = tmp[len(tmp)-1]

        if (count == 6 and skip-1): # teamB
            tmp = line.split(' ')
            ratio.teamB = tmp[len(tmp)-1]

        if (count == 14 and skip-1): # sRatio
            tmp = line.split('%')
            ratio.sRatio = float(int(tmp[0])/100)

        if (count == 15 and skip-1): # spread
            ratio.spread = float(line)

        if (count == 21 and skip-1): # tRatio
            tmp = line.split('%')
            ratio.tRatio = float(int(tmp[0])/100)
            
        if (count == 22 and skip-1): # total
            ratio.total = float(line)

        if (count == 25): # re-count
            count = 0
            if (skip-1):
                ratios.append(ratio)
            else:
                skip = 0
            del ratio
            ratio = BetRatio("", "", 0.0, 0.0, 0.0, 0.0)
            continue
        
        count += 1
    file.close()
    return ratios

def interpret (name):
    if (name == "波士頓塞爾提克"):
        return "Celtics"
    if (name == "布魯克林籃網"):
        return "Nets"
    if (name == "紐約尼克"):
        return "Knicks"
    if (name == "費城76人"):
        return "76ers"
    if (name == "多倫多暴龍"):
        return "Raptors"
    if (name == "芝加哥公牛"):
        return "Bulls"
    if (name == "克里夫蘭騎士"):
        return "Cavaliers"
    if (name == "底特律活塞"):
        return "Pistons"
    if (name == "印第安那溜馬"):
        return "Pacers"
    if (name == "密爾瓦基公鹿"):
        return "Bucks"
    if (name == "亞特蘭大老鷹"):
        return "Hawks"
    if (name == "夏洛特黃蜂"):
        return "Hornets"
    if (name == "邁阿密熱火"):
        return "Heat"
    if (name == "奧蘭多魔術"):
        return "Magic"
    if (name == "華盛頓巫師"):
        return "Wizards"
    if (name == "丹佛金塊"):
        return "Nuggets"
    if (name == "明尼蘇達灰狼"):
        return "Timberwolves"
    if (name == "奧克拉荷馬雷霆"):
        return "Thunder"
    if (name == "波特蘭拓荒者"):
        return "Blazers"
    if (name == "猶他爵士"):
        return "Jazz"
    if (name == "金州勇士"):
        return "Warriors"
    if (name == "洛杉磯快艇"):
        return "Clippers"
    if (name == "洛杉磯湖人"):
        return "Lakers"
    if (name == "鳳凰城太陽"):
        return "Suns"
    if (name == "沙加緬度國王"):
        return "Kings"
    if (name == "達拉斯獨行俠"):
        return "Mavericks"
    if (name == "休士頓火箭"):
        return "Rockets"
    if (name == "曼斐斯灰熊"):
        return "Grizzlies"
    if (name == "紐奧良鵜鶘"):
        return "Pelicans"
    if (name == "聖安東尼奧馬刺"):
        return "Spurs"
    else:
        return name

#todaydate = time.strftime("%Y_%m_%d", time.localtime())

folder = time.strftime("%m%d%y", time.localtime())

if (len(sys.argv) == 3):
    folder = sys.argv[1] # argv[0] is the name of program
    name = sys.argv[2]
else:
    name = sys.argv[1]
print("folder: {0}, name: {1}".format(folder, name))

path = folder + "/" + name + "_oddsshark.txt"
file = open(path, 'r', encoding='utf8')
ratios = betRatio(file)

path = folder + "/" + name  + "_twlottery.txt"
file = open(path, 'r', encoding='utf8')
tmpdata = twLotteryAnalysis(file)
twdatas = tmpdata[0]
gametimes = tmpdata[1]
if (len(twdatas) != len(gametimes)):
    print("[Error] length of twdatas isn't same as gametimes's")
    sys.exit(0)

path = folder + "/" + name  + "_bet365.txt"
file = open(path, 'r', encoding='utf8')
datas365 = bet365Analysis(file, folder)

path = folder + "/" + name + "_predict.csv"
file = open(path, 'w', encoding='utf8')
context = ""
i = 0
for tw in twdatas: # corrected odds
    correctedA = 1.75
    correctedB = 1.75
    correctedU = 1.75
    correctedO = 1.75
    for b365 in datas365:
        if (tw.teamA == b365.teamA and tw.teamB == b365.teamB):
            correctedA = b365.sOddsA-(tw.spread-b365.spread)*0.06
            correctedB = b365.sOddsB-(tw.spread-b365.spread)*-0.06
            correctedU = b365.oddsU-(tw.total-b365.total)*0.06
            correctedO = b365.oddsO-(tw.total-b365.total)*-0.06
            print("{0}\t{1}\t{2}".format(tw.teamA, tw.teamB, gametimes[i]))
            print("{0:.1f}\t{1:.1f}\t{2:.2f}\t{3:.2f} || {4:.1f}\t{5:.2f}\t{6:.2f}".format(tw.spread, tw.spread*-1, tw.sOddsA, tw.sOddsB, tw.total, tw.oddsU, tw.oddsO))
            print("{0:.1f}\t{1:.1f}\t{2:.2f}\t{3:.2f} || {4:.1f}\t{5:.2f}\t{6:.2f}".format(b365.spread, b365.spread*-1, b365.sOddsA, b365.sOddsB, b365.total, b365.oddsU, b365.oddsO))
            print(" \t \t{0:.2f}\t{1:.2f} ||  \t{2:.2f}\t{3:.2f}".format(correctedA, correctedB, correctedU, correctedO))
            context += "{0},{1},{2}\n".format(tw.teamA, tw.teamB, gametimes[i])
            context += "{0:.1f},{1:.1f},{2:.2f},{3:.2f}, ,{4:.1f},{5:.2f},{6:.2f}\n".format(tw.spread, tw.spread*-1, tw.sOddsA, tw.sOddsB, tw.total, tw.oddsU, tw.oddsO)
            context += "{0:.1f},{1:.1f},{2:.2f},{3:.2f}, ,{4:.1f},{5:.2f},{6:.2f}\n".format(b365.spread, b365.spread*-1, b365.sOddsA, b365.sOddsB, b365.total, b365.oddsU, b365.oddsO)
            context += " , ,{0:.2f},{1:.2f}, , ,{2:.2f},{3:.2f}\n".format(correctedA, correctedB, correctedU, correctedO)

    for r in ratios:
        if (tw.teamA == r.teamA and tw.teamB == r.teamB):
            predictA = "    "
            predictB = "    "
            predictC = "    "
            predictD = "    "
            if (r.sRatio <= 0.4 and correctedA-tw.sOddsA <= 0.1):
                predictA = "v   "
            if (1-r.sRatio <= 0.4 and correctedB-tw.sOddsB <= 0.1):
                predictB = "v   "
            if (r.tRatio <= 0.4 and correctedU-tw.oddsU <= 0.1):
                predictC = "v   "
            if (1-r.tRatio <= 0.4 and correctedO-tw.oddsO <= 0.1):
                predictD = "v   " 
            print("{0:.0%}\t{1:.0%}\t \t     ||  \t{2:.0%}\t{3:.0%}".format(r.sRatio, 1-r.sRatio, r.tRatio, 1-r.tRatio))
            print("{0}\t{1}\t \t     ||  \t{2}\t{3}".format(predictA, predictB, predictC, predictD))
            context += "{0:.0%},{1:.0%}, , , , ,{2:.0%},{3:.0%}\n".format(r.sRatio, 1-r.sRatio, r.tRatio, 1-r.tRatio)
            context += "{0},{1}, , , , ,{2},{3}\n\n".format(predictA, predictB, predictC, predictD)
    i += 1


file.write(context)
file.close()
