from sys import exc_info
from xlogging import Logger, LogLevel
from xexcerr import *
from cxtk import CanvasContainer

# canvas values
width = 976
height = 976
pad = 25.0
total_W = width + 2*pad
total_H = height + 2*pad

cvc = CanvasContainer(total_W, total_H)
cvc.create_border(int(pad))

# dotsize
size_D = 20

# letter size
width_L = 95
height_L = 95
width_M = int(width / width_L)
height_M = int(height / height_L)

hist = [""]
letters = dict()
letterBoxes = list()
settings = [0, "],[", "],["]

logger = Logger(LogLevel.EXC)

def changeSetting( index, newval):
    if index is 1:
        intersect = set(str(newval)) & set("abcdefghijklmnopqrstuvwxyz,[]_^<>")
        if len(intersect) is not 0:
            logger.log(LogLevel.EXC, "Intersection of: " + str(intersect))
            raise IllegalCharacterException("Illegal seperator '"+str(newval)+"'.", None)
        else:
            logger.log(LogLevel.MSG, "Changing existing letters")
            for letter in letters.keys():
                logger.log(LogLevel.DEBUG, "Letter: " + letter.upper())
                logger.log(LogLevel.DEBUG, "Old: " + letters[letter])
                letters[letter] = letters[letter].replace(settings[index],newval)
                logger.log(LogLevel.DEBUG, "New: " + letters[letter])
    elif index is 0:
        logger.log(LogLevel.MSG, "Setting position to index " + str(newval))
    settings[index] = newval

def incLetterCount():
    settings[0] = settings[0] + 1

def fold(fnct, lst):
    for elem in lst:
        fnct(elem)

def definePath(name, strlst):
    letters[str(name)] = strlst

def drawPath(strarg, name=None):
    strlst = ""
    if strarg in letters.keys():
        strlst = letters[strarg]
    else:
        raise NoDefinitionException("No draw definition for given key: " + str(strarg), None)
    lst = list()
    count = settings[0] % len(letterBoxes)
    incLetterCount()
    for s in strlst.split(settings[1]):
        xadjust = 0.2 * width_L
        yadjust = 0.2 * height_L
        logger.log(LogLevel.DEBUG, "Split: " + str(s))
        #s = s.split(",")
        #logger.log(LogLevel.DEBUG, "After: " + str(s))
        vp = list([0,0])
        if "left" in s or "l" in s:
            vp[0] = letterBoxes[count][0][0]#left
        elif "center" in s or "c" in s:
            vp[0] = letterBoxes[count][0][1]#center
        else:
            vp[0] = letterBoxes[count][0][2]#right
        if "<" in s:
            vp[0] -= xadjust
        elif ">" in s:
            vp[0] += xadjust
        if "up" in s or "u" in s:
            vp[1] = letterBoxes[count][1][0]#up
        elif "mid" in s or "m" in s:
            vp[1] = letterBoxes[count][1][1]#mid
        else:
            vp[1] = letterBoxes[count][1][2]#down
        if "_" in s:
            vp[1] += yadjust
        elif "^" in s:
            vp[1] -= yadjust
        lst.append(vp)
    prv = -1
    for elem in lst:
        if prv == -1:
            prv = elem
        else:
            cvc.create_line([prv[0],prv[1],elem[0],elem[1]], name)
            prv = elem

def drawMany( strarg, numarg):
    for _x in range(0,int(numarg)):
        drawPath( strarg, name=str(settings[0] % len(letterBoxes)))

# letter boxes
for row in range(0, height-int(pad+height_L), height_L + height_M):
    row += pad
    rowu = row + 0.0 * height_L
    rowm = row + 0.5 * height_L
    rowd = row + 1.0 * height_L
    for col in range(0,width-int(pad+width_L), width_L + width_M):
        col += pad
        coll = col + 0.0 * width_L
        colc = col + 0.5 * width_L
        colr = col + 1.0 * width_L
        letterBoxes.append([[coll,colc,colr],[rowu,rowm,rowd]])
logger.log(LogLevel.VERBOSE, "count: " + str(len(letterBoxes)))

# relative y values
up = 0.0 * height + pad
mid = 0.5 * height + pad
down = 1.0 * height + pad
# relative x values
left = 0.0 * width + pad
center = 0.5 * width + pad
right = 1.0 * width + pad

# setting spot names as list
spots = list()
for h in ["up","mid","down"]:
    for w in ["left","center","right"]:
        spots.append(h+w)

# initializing dict
dots = dict()
for spot in spots:
    dots[spot] = list([0,0,0,0])
    if "up" in spot or "u" in spot:
        dots[spot][1] = up - size_D*0.5
        dots[spot][3] = up + size_D*0.5
    elif "mid" in spot or "m" in spot:
        dots[spot][1] = mid - size_D*0.5
        dots[spot][3] = mid + size_D*0.5
    else:
        dots[spot][1] = down - size_D*0.5
        dots[spot][3] = down + size_D*0.5
    if "left" in spot or "l" in spot:
        dots[spot][0] = left - size_D*0.5
        dots[spot][2] = left + size_D*0.5
    elif "center" in spot or "c" in spot:
        dots[spot][0] = center - size_D*0.5
        dots[spot][2] = center + size_D*0.5
    else:
        dots[spot][0] = right - size_D*0.5
        dots[spot][2] = right + size_D*0.5

dss = "#"*14 +" "*5+ "x1 |" +" "*4+ "y1 |" +" "*4+ "x2 |" +" "*4+ "y2 |\n"
for k in dots:
    dss += str(k) + ":" + " "*(12-len(str(k))) + "| "
    for v in dots[k]:
        dss += " "*(7-len(str(v))) + str(v) + "|"
    dss += "\n"
logger.log(LogLevel.VERBOSE, dss)

cmds = dict()
cmds[""] = lambda: logger.log(LogLevel.MSG, "Try !h")
cmds["!q"] = lambda: logger.log(LogLevel.MSG, "Exiting...")
cmds["!h"] = lambda: logger.log(LogLevel.MSG, *(list(cmds.keys()))[1:],sep="\n", indent=3)

cmds["hist"] = lambda: logger.log(LogLevel.MSG, *hist[1:],sep="\n", indent=3)
cmds["list"] = lambda: logger.log(LogLevel.MSG, *cvc.getElements(),sep="\n", indent=3)

cmds["dots"] = lambda: fold(cvc.create_oval, dots.values() )
cmds["draw"] = lambda arg: drawPath(arg, name=str(settings[0] % len(letterBoxes)))
cmds["drawmany"] = lambda sarg, narg: drawMany( sarg, narg)

cmds["log"] = lambda narg: logger.level(int(narg))

cmds["rem"] = lambda arg: logger.log(LogLevel.MSG, "Removed " + str(arg)) if cvc.remove(arg) else logger.log(LogLevel.MSG, "No such key")
cmds["remmany"] = lambda arglist: logger.log(LogLevel.MSG, "Removed " + str(cvc.removeMany(str(arglist).split(","))) )
cmds["pos"] = lambda arg: changeSetting( 0, int(arg) % len(letterBoxes))

cmds["def"] = lambda name, lst: definePath(name, lst)
cmds["sep"] = lambda sep: changeSetting(1,sep) if sep!='' else changeSetting(1,settings[2])

# in code path def
aletter = "[[left,down],[center,up],[right,down]]"
letters["a"] = aletter
letters["xc"] = "[u^l<],[u^l>],[u_l>],[u_l<],[u^l<],[u_l>],[u_l<],[u^l>],[u^r<],[u^r>],[u_r>],[u_r<],[u^r<],[u_r>],[u_r<],[u^r>],[d^r>],[d^r<],[d^r>],[d_r>],[d_r<],[d^r<],[d_r>],[d_r<],[d^r>],[d_r>],[d_l<],[d^l<],[d^l>],[d_l>],[d_l<],[d^l<],[d_l>],[d_l<],[d^l>],[d^l<],[u^l<]"
letters["x"] = "[ur],[dl],[mc],[ul],[dr]"
letters["box"] = "[ur],[ul],[dl],[dr],[ur]"
# function usage
definePath("b", "[[up,left],[mid,right],[mid,left],[down,right],[down,left],[up,left]]")

while hist[len(hist)-1] != "!q" :
    cvc.updateCanvas(True)
    usrin = input("....> ").lower().strip()
    hist.append(usrin)
    cvc.updateCanvas(True)
    try:
        usrcmd = usrin.split(" ")[0]
        usrprm = usrin.split(" ")[1:]
        cmds[usrcmd](*usrprm)
    except:
        logger.log(LogLevel.ERR, exc_info()[:-1])
        if usrcmd not in cmds.keys():
            logger.log(LogLevel.EXC, "Unknown command '"+ str(usrin) +"'.")
            logger.log(LogLevel.MSG, "Type '!h' to list available commands.")
cvc.updateCanvas(False)