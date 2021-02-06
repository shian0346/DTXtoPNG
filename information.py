import os
import sys
from math import gcd

# reduces chart into 0's and 1's
def boolify(ot):
    ct = ""
    while ot:
        if ot[0:2] == "00":
            ct += "0"
        else:
            ct += "1"
        ot = ot[2:]
    return ct

# reduces chart into positions with respect to the bar length
def numerify(lane, lenghts):
    numerified_lane = []
    current_position = 0
    for i in range(len(lane)):
        if lane[i] != '':
            for j in range(len(lane[i])):
                if lane[i][j] == '1':
                    note_pos = current_position + float(j/len(lane[i]))*lenghts[i]
                    numerified_lane.append(note_pos)
        current_position += lenghts[i]
    return numerified_lane

# fill '0.0's of LEN
def fillify(lengths):
    filled_lengths = lengths
    temp_len = filled_lengths[0]
    for i in range(len(filled_lengths)):
        if filled_lengths[i] == float(0):
            filled_lengths[i] = temp_len
        temp_len = filled_lengths[i]
    return filled_lengths

# stores where and how the BPM changes
def puctufy(d):
    index = 0
    BPMCHANGEPOINT = []
    VALS = d["BPMval"]
    for element in d["BPM"]:
        
        if element != '':
            for i in range(0, len(element), 2):
                if element[i:i+2] != '00':
                    pos = d["BPMCHANGEPOINT"][index]
                    val = VALS[str(element[i:i+2])]
                    tup = (pos,val)
                    BPMCHANGEPOINT.append(tup)
                    index += 1
    return BPMCHANGEPOINT

# combines two lanes into one (Left Bass Drum and Left Hi-Hat Pedal)
def combiner(l1,l2):
    e1 = ""
    e2 = ""
    d = gcd(len(l1), len(l2))
    l3 = ""
    # extend l1 to e1
    for i in l1:
        e1 += i
        for j in range(int(len(l2)/d)-1):
            e1 += "0"
    # extend l2 to e2
    for i in l2:
        e2 +=   i
        for j in range(int(len(l1)/d)-1):
            e2 += "0"
    # combine e1 and e2 into l3
    for i in range(len(e1)):
        if e1[i] == "1" or e2[i] == "1":
            l3 += "1"
        else:
            l3 += "0"
    return l3

# turn *.dtx file into a dictionary form
def dictify(dir):
    try:
        f = open(dir, 'r', encoding='utf16')
        t = f.read()
    except:
        try:
            f = open(dir, 'r', encoding="shiftjis")
            t = f.read()
        except UnicodeError:
            print(dir)
            print("FATAL ERROR: simfile's encoding not supported")
            sys.exit(1)
    f.close()

    # initialization
    t = os.linesep.join([s for s in t.splitlines() if s]).splitlines() # convert into a list
    d = {}              # dictionary
    i = len(t)-1        # index
    while not t[i][1].isdigit(): i -= 1
    if t[i][6].isdigit(): b = int(t[i][1:5])    # last bar number (This is an exception handling for bad dtx files that write like: #010261: ZY, which instead should be like: #10261: ZY)
    else: b = int(t[i][1:4])                    # last bar number
    i = 0               # initialize index

    # initialize chart info with bar count (song length)
    LC, LP, HH, SD, HT, BD, LT, FT, CY, BPM = (
        ["" for x in range(b+1)] for i in range(10))
    LEN = [float(0) for x in range(b+1)]
    LEN[0] = float(1)
    BPMval = {} # dictionary BPM value
    BPMCHANGEPOINT = ["" for x in range(b+1)]

    # store information
    for x in range(len(t)):
        # store chart information
        if t[i][1].isdigit():
            b = int(t[i][1:4])  # bar number
            l = t[i][4:6]       # lane number
            c = t[i][8:]        # chart
            if   l == "02" and b < len(LEN):
                LEN[b] = float(c)
            elif l == "08":
                BPM[b] = c
                BPMCHANGEPOINT[b] = boolify(c)
            elif l == "11":
                HH[b] = boolify(c)
            elif l == "12":
                SD[b] = boolify(c)
            elif l == "13":
                BD[b] = boolify(c)
            elif l == "14":
                HT[b] = boolify(c)
            elif l == "15":
                LT[b] = boolify(c)
            elif l == "16":
                CY[b] = boolify(c)
            elif l == "17":
                FT[b] = boolify(c)
            elif l == "1A":
                LC[b] = boolify(c)
            elif l == "1C" or l == "1B":
                if LP[b] != "":
                    LP[b] = combiner(LP[b], boolify(c))
                else:
                    LP[b] = boolify(c)

        # store song information
        else:
            if t[i].startswith('#TITLE:') or t[i].startswith('#ARTIST:') or t[i].startswith('#DLEVEL:') or t[i].startswith('#PREIMAGE:'):
                k = t[i].split()[0][1:-1]   # dictionary key
                v = t[i][len(k)+3:]         # dictionary value
                d[k] = v 
            elif t[i].startswith('#TITLE') or t[i].startswith('#ARTIST') or t[i].startswith('#DLEVEL') or t[i].startswith('#PREIMAGE'):
                k = t[i].split()[0][1:]   # dictionary key
                v = t[i][len(k)+2:]         # dictionary value
                d[k] = v 
            elif t[i].startswith('#BPM'):
                if t[i][4] != ":" and t[i][4] != " ":
                    k = t[i][4:6]        # BPM dictionary key
                    v = t[i][7:]         # BPM dictionary value
                    # empty BPM exception handling
                    if v != "":
                        v = float(v)
                    else:
                        if "BPMINFO" in d:
                            v = float(d["BPMINFO"])
                        else:
                            v = float(120)          
                    BPMval[k] = v
                else:
                    k = t[i].split()[0][1:-1]
                    v = t[i][len(k)+3:]         
                    d["BPMINFO"] = v 
        i += 1

    #if len(d["DLEVEL"]) == 1:
    #    d["DLEVEL"] = float(d["DLEVEL"])
    #elif len(d["DLEVEL"]) == 2:
    #    d["DLEVEL"] = float(d["DLEVEL"])/10
    #else:
    #    d["DLEVEL"] = float(d["DLEVEL"])/100
    
    # store note information
    d["LEN"] = fillify(LEN)
    d["HH"] = numerify(HH, d["LEN"])
    d["SD"] = numerify(SD, d["LEN"])
    d["BD"] = numerify(BD, d["LEN"])
    d["HT"] = numerify(HT, d["LEN"])
    d["LT"] = numerify(LT, d["LEN"])
    d["CY"] = numerify(CY, d["LEN"])
    d["FT"] = numerify(FT, d["LEN"])
    d["LC"] = numerify(LC, d["LEN"])
    d["LP"] = numerify(LP, d["LEN"])

    # construct d["BPMCHANGE"]
    d["BPMval"] = BPMval
    d["BPM"] = BPM
    d["BPMCHANGEPOINT"] = numerify(BPMCHANGEPOINT, d["LEN"])
    d["BPMCHANGE"] = puctufy(d)
    del d["BPMval"]
    del d["BPMCHANGEPOINT"]

    return d