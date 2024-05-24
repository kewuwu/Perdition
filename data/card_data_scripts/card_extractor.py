import json
import os
from PIL import Image
import psutil
import keras_ocr

{
    "name": " ",
    "id": " ",
    "type": " ",
    "front_png": " ",
    "back_png": " ",
    "vp": " ",
    "effect": "",
    "sin": "",
    "reffect": " ",
    "ceffect": " ",
    "layerCards": " ",
    "layer": " ",
    "guilt": " ",
    "rarity": " ",
}


def detect_with_keras_ocr(image_path):
    im_txt = keras_ocr.tools.read(image_path)
    prediction_group = pipeline.recognize([im_txt])
    return prediction_group


def sort_left_right(keras_array):
    temp = []
    for i in keras_array:
        for y in i:
            temp.append([y[0], y[1][0][0]])
    temp.sort(key=lambda x: x[1])
    return temp


def crop_and_keras_soul(im, soul_array):
    card_data = {}
    im = im.crop(im.getbbox())
    im_name = im.crop([152, 70, 632, 100])
    im_name.save("crop_name_" + file)
    im_rarity_sin = im.crop([70, 522, 630, 560])
    im_rarity_sin.save("crop_rarity_sin_" + file)
    pred1 = detect_with_keras_ocr("crop_name_" + file)
    pred2 = detect_with_keras_ocr("crop_rarity_sin_" + file)
    sorted1 = sort_left_right(pred1)
    name = ""
    for i in sorted1:
        name = name + " " + i[0]
    name = name.strip()
    sorted2 = sort_left_right(pred2)
    card_data["name"] = name
    card_data["id"] = int(file.split(".")[0])
    card_data["type"] = "soul"
    card_data["rarity"] = sorted2[0][0]
    card_data["sin"] = sorted2[1][0]
    if sorted2[0][0] == "common":
        card_data["vp"] = 1
    elif sorted2[0][0] == "rare":
        card_data["vp"] = 2
    else:
        card_data["vp"] = 5
    card_data["image_path"] = os.path.join(
        os.getcwd(), "Card_Assets", file
    )
    soul_array.append(card_data)
    os.remove("crop_name_" + file)
    os.remove("crop_rarity_sin_" + file)
    return soul_array


def crop_and_keras_player(im, player_array):
    card_data = {}
    im = im.crop(im.getbbox())
    im_name = im.crop([152, 70, 632, 100])
    im_name.save("crop_name_" + file)
    pred1 = detect_with_keras_ocr("crop_name_" + file)
    sorted1 = sort_left_right(pred1)
    name = ""
    for i in sorted1:
        name = name + " " + i[0]
    name = name.strip()
    card_data["name"] = name
    card_data["id"] = int(file.split(".")[0])
    card_data["type"] = "player"
    card_data["max_guilt"] = 11
    card_data["current_guilt"] = 5
    card_data["image_path"] = os.path.join(
        os.getcwd(), "Card_Assets", file
    )
    player_array.append(card_data)
    os.remove("crop_name_" + file)
    return player_array


def crop_and_keras_divine(im, divine_array):
    card_data = {}
    im = im.crop(im.getbbox())
    im_name = im.crop([152, 70, 632, 100])
    im_name.save("crop_name_" + file)
    pred1 = detect_with_keras_ocr("crop_name_" + file)
    sorted1 = sort_left_right(pred1)
    name = ""
    for i in sorted1:
        name = name + " " + i[0]
    name = name.strip()
    card_data["name"] = name
    card_data["id"] = int(file.split(".")[0])
    card_data["type"] = "divine"
    card_data["image_path"] = os.path.join(
        os.getcwd(), "Card_Assets", file
    )
    card_data["vp"] = "1"
    divine_array.append(card_data)
    os.remove("crop_name_" + file)
    return divine_array


def crop_and_keras_layer_event(im, layer_event_array):
    card_data = {}
    im = im.crop(im.getbbox())
    im_name = im.crop([152, 70, 632, 100])
    im_name.save("crop_name_" + file)
    im_sin = im.crop([70, 522, 630, 560])
    im_sin.save("crop_sin_" + file)
    pred1 = detect_with_keras_ocr("crop_name_" + file)
    pred2 = detect_with_keras_ocr("crop_sin_" + file)
    sorted1 = sort_left_right(pred1)
    sorted2 = sort_left_right(pred2)
    name = ""
    for i in sorted1:
        name = name + " " + i[0]
    name = name.strip()
    card_data["name"] = name
    card_data["id"] = int(file.split(".")[0])
    card_data["type"] = "layer_event"
    card_data["sin"] = sorted2[0][0]
    card_data["image_path"] = os.path.join(
        os.getcwd(), "Card_Assets", file
    )
    layer_event_array.append(card_data)
    os.remove("crop_name_" + file)
    os.remove("crop_sin_" + file)
    return layer_event_array


def crop_and_keras_archdaemon(im, archdaemon_array):
    card_data = {}
    im = im.crop(im.getbbox())
    im_name = im.crop([152, 70, 632, 100])
    im_name.save("crop_name_" + file)
    pred1 = detect_with_keras_ocr("crop_name_" + file)
    sorted1 = sort_left_right(pred1)
    name = ""
    for i in sorted1:
        name = name + " " + i[0]
    name = name.strip()
    print(name)
    card_data["name"] = name
    card_data["id"] = int(file.split(".")[0])
    card_data["sin"] = name.split(" ")[2]
    card_data["type"] = "archdaemon"
    card_data["image_path"] = os.path.join(
        os.getcwd(), "Card_Assets", file
    )
    archdaemon_array.append(card_data)
    os.remove("crop_name_" + file)
    return archdaemon_array


fpath = os.path.join(os.getcwd(), "Card_Assets")
files = sorted(os.listdir(fpath), key=lambda x: int(x.split(".")[0]))
all_cards = []
pipeline = keras_ocr.pipeline.Pipeline()
for file in files:
    im = Image.open(os.path.join(fpath, file))
    j = int(file.split(".")[0])
    if j <= 95:
        crop_and_keras_soul(im, all_cards)
    elif 96 <= j and j <= 103:
        crop_and_keras_player(im, all_cards)
    elif 104 <= j and j <= 114:
        crop_and_keras_divine(im, all_cards)
    elif 115 <= j and j <= 121:
        crop_and_keras_archdaemon(im, all_cards)
    else:
        crop_and_keras_layer_event(im, all_cards)
print(all_cards)
with open("./all_cards.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(all_cards, ensure_ascii=False, indent=4))
