import read_roi
import json
import io
import os
from os import walk
path = "."

#ROI arrays
filenames = [

]
zips = [

]
#scanning
for r, d, f in os.walk(path):
    for file in f:
        if '.png' in file:
            filenames.append(os.path.join(r, file))
        elif '.zip' in file:
            zips.append(os.path.join(r, file))
#Sorting
zips.sort()
filenames.sort()
#looping and decoding...
for i in range(len(zips)):
    # declare ROI file
    roi = read_roi.read_roi_zip(zips[i])
    roi_list = list(roi.values())
    # ROI related file informations
    filename = filenames[i].replace("./","")
    size = os.path.getsize(filename)
    try:
        f = open("via_region_data.json")
        original = json.loads(f.read())
        print("Writing...")
        # Do something with the file
    except FileNotFoundError:
        print("File not exisited, creating new file...")
        original = {}

    data = {
        filename+str(size): {
            "fileref":  "",
            "size":  size,
            "filename": filename,
            "base64_img_data": "",
            "file_attributes": {},
            "regions": {
                }
            }
        }

    # write json

    length = len(list(roi.values()))
    for a in range(length):
        # parameters
        x_list = roi_list[a]['x']
        y_list = roi_list[a]['y']
        x_list.append(roi_list[a]['x'][0])
        y_list.append(roi_list[a]['y'][0])
        regions = {
            str(a): {
                "shape_attributes": {
                    "name":  "polygon",
                    "all_points_x": x_list,
                    "all_points_y": y_list
                },
                "region_attributes": {
                    "name": "cell"
                }
            } 
        }
        data[filename+str(size)]["regions"].update(regions)
    original.update(data)
    with io.open('via_region_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(original, ensure_ascii=False))
