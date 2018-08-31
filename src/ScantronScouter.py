import cv2
import numpy as np
import math
import configparser
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog

# INTERPRET SCANTRON VALUE
def single(values):
    for i, value in enumerate(reversed(values)):
        if value:
            return str(len(values)-i-1) + ","
    return ","
def multiple(values):
    tmp = ""
    for i, value in enumerate(values, start=1):
        tmp += (str(i) + "/") if value else ""
    return tmp[:-1] + ","
def binary(values):
    return str(sum(2**i for i, v in enumerate(values) if v)) + ","
def tf(values):
    return (str(values[0]) if True in values[0:2] else "") + ","
def custom(values, list_options):
    list_options = list_options.split(",")
    tmp = ""
    for i, value in enumerate(values):
        tmp += (list_options[i] + "/") if value else ""
    return tmp[:-1] + ","

# DRAW DOT ON IMAGE, ADD POSITION TO LIST
def draw_dot(x, y, cont, flag):
    global mod, positions, values, slope, width, height, main, label_text

    x_ = x + .5
    y_ = y + (1.5 if slope < 0 else .5)
    x0 = top[0] + int(math.sin(slope)*height/19*y_ + math.cos(-slope)*width/13*x_)
    y0 = top[1] + int(math.cos(slope)*height/19*y_ + (bottom[3] if slope > -0.05 else 0) + math.sin(-slope)*width/13*x_)
    if flag:
        positions.append((x, y, x0, y0))
        values[y][x] = mod[y0, x0] > 20
    cv2.line(cont, (x0, y0), (x0+1, y0+1), (0,255,0) if values[y][x] else (255,0,255), 2)
# HANDLE CLICK EVENTS
def click(event, x, y, flags, param):
    global cont, positions, values

    if event == cv2.EVENT_LBUTTONDOWN:
        min = math.sqrt(np.shape(cont)[0]**2 + np.shape(cont)[1]**2)
        minp = (0,0)
        for p in positions:
            if math.sqrt((p[2]-x)**2 + (p[3]-y)**2) < min:
                min = math.sqrt((p[2]-x)**2 + (p[3]-y)**2)
                minp = (p[0], p[1])
        values[minp[1]][minp[0]] = not values[minp[1]][minp[0]]
        draw_dot(minp[0], minp[1], cont, False)
        cv2.imshow('img', cont)

# IMPORT AND PROCESS IMAGE
def process():
    global mod, cont, top, bottom, positions, values, slope, width, height, main, label_text, config_file

    # IMPORT IMAGE
    try:
        img = cv2.imread(filedialog.askopenfilename(initialdir=image_dir, title="Choose Image File", filetypes=(("image files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("all files", "*.*"))), cv2.IMREAD_GRAYSCALE)
        if np.shape(img)[1] > main.winfo_screenheight():
            img = cv2.resize(img, None, fx=main.winfo_screenheight() / np.shape(img)[1] * .8,
                             fy=main.winfo_screenheight() / np.shape(img)[1] * .8, interpolation=cv2.INTER_CUBIC)
    except:
        label_text.set("Data not entered.")
        main.update()
        return

    # THRESHOLD CALIBRATION BARS AND ANSWERS
    thresh1 = cv2.inRange(img, 0, 60)
    thresh2 = cv2.inRange(img, 70, 200)

    # FILL IN ANSWERS
    mod = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    mod = cv2.morphologyEx(mod, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

    # FIND CALIBRATION BARS
    contours = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    areas = []
    for c in contours:
        areas.append(cv2.contourArea(c))
    contours = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)

    top, bottom = (cv2.boundingRect(contours[0][1]), cv2.boundingRect(contours[1][1])) if \
        cv2.boundingRect(contours[0][1])[1] < cv2.boundingRect(contours[1][1])[1] else \
        (cv2.boundingRect(contours[1][1]), cv2.boundingRect(contours[0][1]))

    slope = math.atan((bottom[0] - top[0]) / (bottom[1] - top[1]))
    width = (top[2] + bottom[2]) / 2 / math.cos(slope)
    height = (bottom[1] - top[1]) / math.cos(slope)

    cont = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cont = cv2.rectangle(cont, (top[0], top[1]), (top[0]+top[2], top[1]+top[3]), (0,255,0))
    cont = cv2.rectangle(cont, (bottom[0], bottom[1]), (bottom[0]+bottom[2], bottom[1]+bottom[3]), (0,0,255))
    cont = cv2.line(cont, (top[0], top[1] + (top[3] if slope > -0.05 else 0)), (
    top[0] + int(math.cos(-slope) * width), top[1] + int(math.sin(-slope) * width) + (top[3] if slope > -0.05 else 0)),
                    (255, 0, 0), 2)
    cont = cv2.line(cont, (top[0], top[1] + (top[3] if slope > -0.05 else 0)), (
    int(top[0] + math.sin(slope) * height), int(top[1] + math.cos(slope) * height) + (bottom[3] if slope > -0.05 else 0)),
                    (255, 0, 0), 2)

    # READ ANSWERS
    values = [[0 for x in range(13)] for y in range(18)]
    positions = []
    for y in range(18):
        for x in range(13):
            draw_dot(x, y, cont, True)

    # SHOW IMAGE, WAIT FOR CORRECTIONS
    cv2.imshow('img', cont)
    cv2.setMouseCallback('img', click)
    while True:
        try:
            a = cv2.waitKey(20)
            if cv2.getWindowProperty("img", 0) == -1:   # CHECK WINDOW CLOSED
                label_text.set("Data not entered.")
                main.update()
                cv2.destroyAllWindows()
                return
            if a in [13, 32]:  # SPACE OR ENTER
                cv2.destroyAllWindows()
                break
            elif a == 27:    # ESC
                label_text.set("Data not entered.")
                main.update()
                cv2.destroyAllWindows()
                return
        except ValueError:
            pass

    # READ TEAM, MATCH NUMBER
    match = int(single(values[2][:10])[:-1]) + int(single(values[1][:10])[:-1])*10 + (100 if values[1][10] else 0)
    position = int(single(values[0][:6])[:-1])
    team = matches[match][position]
    replay = values[0][6]

    # WRITE TO DATA FILE
    try:
        file_path = config_file + ("" if single_file else (str(team)+".csv"))
        exists = Path(file_path).is_file()
        with open(file_path, "a+") as file:
            if not exists:
                file.write("Team,Match," if single_file else (str(team)+"\nMatch,"))
                for i in range(1, 17):
                    file.write(config["Question "+str(i)]["Name"] + ",")
                file.write("\n")
            file.write(((str(team) + ",") if single_file else "") + str(match) + ("R" if replay else "") + "," + ["R1","R2","R3","B1","B2","B3"][position] + ",")
            for i, value in enumerate(values[3:], start=1):
                if config["Question " + str(i)]["Type"] == "Single":
                    file.write(single(value))
                elif config["Question " + str(i)]["Type"] == "Binary":
                    file.write(binary(value))
                elif config["Question " + str(i)]["Type"] == "TF":
                    file.write(tf(value))
                elif config["Question " + str(i)]["Type"] == "Multiple":
                    file.write(multiple(value))
                else:
                    file.write(custom(value, config["Question " + str(i)]["Type"]))
            file.write("\n")
    except:
        label_text.set("Data file error.")
        main.update()
        return
    label_text.set("Data successfully entered for team " + str(team) + " in match " + str(match) + ".")
    main.update()

mod = None
cont = None
top = (0,0)
bottom = (0,0)
positions = []
values = []
slope = 0
width = 0
height = 0

main = tk.Tk()
main.geometry('%dx%d+%d+%d' % (310, 50, (main.winfo_screenwidth()-310)/2, main.winfo_screenheight()/3-50/2))
main.resizable(0,0)
main.title("ScantronScouter")
main.pack_propagate(0)
label_text = tk.StringVar(main, value="Click \"Add Data\" to begin.")
tk.Label(main, textvariable=label_text, wraplength=450).pack(fill=tk.X)
tk.Button(main, text="Add Data", command=process).pack(side=tk.LEFT, padx=10)
tk.Button(main, text="Exit", command=lambda:sys.exit(0)).pack(side=tk.LEFT, padx=5)

# OPEN CONFIG FILE
config = configparser.ConfigParser()
try:
    config.read("../config.ini")
    image_dir = config["DEFAULT"]["Default_Image_Directory"]
    image_dir = image_dir[(1 if image_dir[0] == '/' else 0):]

    config_file = config["DEFAULT"]["Data_File"]
    config_file = config_file[(1 if config_file[0] == '/' else 0):]
    single_file = "." in config_file
    config_file += "/" if not single_file and config_file[-1] not in ["/", "\\"] else ""
except:
    label_text.set("Config file missing/invalid.")
    main.update()

# READ TBA DATA FROM FILE
with open(config["DEFAULT"]["TBA_DATA_FILE"]) as file:
    lines = [(line[:-1].split(",")) for line in file.readlines()]
    event = lines[0][0]
    if event != config["DEFAULT"]["EventKey"]:
        label_text.set("Event data does not match the event in the config file.")
        main.update()
    matches = {}
    for l in lines[2:]:
        matches[int(l[0])] = l[1:]

tk.mainloop()
