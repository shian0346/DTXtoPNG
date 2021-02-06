import math

# prints song information
def getinfo(d):
    print("SONG TITLE :", d["TITLE"])
    print("ARTIST     :", d["ARTIST"])
    print("DLEVEL     :", d["DLEVEL"])
    print("BPM        :", d["BPMINFO"])

# get the running time
def gettime(pixel_length):
    import datetime 
    return (str(datetime.timedelta(seconds = (pixel_length/720))).split(".")[0])[3:]

# get the whole pixel length
def getlength(d):
    pixel_length = 0
    for i in range(len(d["BPMCHANGE"])):
        if not i == (len(d["BPMCHANGE"])-1):
            length = d["BPMCHANGE"][i+1][0] - d["BPMCHANGE"][i][0]
        else:
            length = sum(d["LEN"]) - d["BPMCHANGE"][i][0]
        BPM = d["BPMCHANGE"][i][1]
        pixel_length += 172800 * length / BPM
    return math.floor(float(pixel_length))

# turn float numbers into pixel positions with respect to the BPM
def pixify(notes, lanes, BPM):
    notes_pix = []
    cur_pos = float(0)
    cur_pos_pix = float(0)
    j = 0
    for i  in range(len(notes)):
        # is the current BPM the last BPM?
        if (j+1)==len(BPM): 
            length = notes[i] - cur_pos
            cur_pos = notes[i]
            cur_pos_pix += 172800 * length / BPM[j][1]
        else:
            # is there BPM change between the current and the next note?
            while (j+1)<len(BPM) and BPM[j+1][0] < notes[i]:
                length = BPM[j+1][0] - cur_pos
                cur_pos = BPM[j+1][0]
                cur_pos_pix += 172800 * length / BPM[j][1]
                j += 1
            length = notes[i] - cur_pos
            cur_pos = notes[i]
            cur_pos_pix += 172800 * length / BPM[j][1]
            # is the next BPM change at the next note?
            if (j+1)<len(BPM) and BPM[j+1][0] == notes[i]:
                j += 1

        tup = (math.floor(float(cur_pos_pix)), lanes[i])
        notes_pix.append(tup)
    return notes_pix

# get pixel positions for all elements
def getpixels(d):

    # initialization
    g = {}  # stores graphical information
    pixel_length = 0
    big_barline = []
    small_barline = []

    # get barline positions
    current_position = float(0)
    for i in range(len(d["LEN"])):
        big_barline.append(current_position)
        j = 0.25
        while j < d["LEN"][i]:
            small_barline.append(current_position+j)
            j += 0.25
        current_position += d["LEN"][i]
    g["big_barline"] = big_barline
    g["small_barline"] = small_barline

    # collect all notes into one list of tuples: (position, lane)
    all_notes = []
    for element in d["LC"]:
        tup = (element, int(0))
        all_notes.append(tup)
    for element in d["HH"]:
        tup = (element, int(1))
        all_notes.append(tup)
    for element in d["LP"]:
        tup = (element, int(2))
        all_notes.append(tup)
    for element in d["SD"]:
        tup = (element, int(3))
        all_notes.append(tup)
    for element in d["HT"]:
        tup = (element, int(4))
        all_notes.append(tup)
    for element in d["BD"]:
        tup = (element, int(5))
        all_notes.append(tup)
    for element in d["LT"]:
        tup = (element, int(6))
        all_notes.append(tup)
    for element in d["FT"]:
        tup = (element, int(7))
        all_notes.append(tup)
    for element in d["CY"]:
        tup = (element, int(8))
        all_notes.append(tup)
    for element in g["big_barline"]:
        tup = (element, int(9))
        all_notes.append(tup)
    for element in g["small_barline"]:
        tup = (element, int(10))
        all_notes.append(tup)
    from operator import itemgetter
    all_notes.sort(key=itemgetter(1), reverse=True)
    all_notes.sort(key=itemgetter(0))

    return pixify([i[0] for i in all_notes], [i[1] for i in all_notes], d["BPMCHANGE"])