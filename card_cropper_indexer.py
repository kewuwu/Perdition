from PIL import Image
import os

X_INTER_OFFSET = 50
Y_INTER_OFFSET = 105

CARD_HEIGHT = 1020
CARD_WIDTH = 705

order = [
    "Common Greed",
    "Common Lust",
    "Common Sloth",
    "Common Gluttony",
    "Common Envy",
    "Common Wrath",
    "Rare Misc 1",
    "Rare Misc 2",
    "Rare Misc 3",
    "Rare and Leg Misc 1",
    "Leg Misc 2",
    "Leg Misc 3",
    "playercards",
    "Divine Revelation 1",
    "Divine Revelation 2",
    "Archdaemons",
    "Layer Event Cards 1",
    "Layer Event Cards 2",
    "Layer Event Cards 3",
]

fpath = "./Raw_Cards"

files = os.listdir(fpath)
new_files = []
for o in order:
    new_files.append([f for f in files if o in f][0])
i = 0

for file in new_files:

    img = Image.open(os.path.join(fpath, file))
    rect = img.getbbox()
    ci = img.crop(rect)

    for x in range(4):
        for y in range(2):
            left = x * (CARD_WIDTH + X_INTER_OFFSET)
            up = y * (CARD_HEIGHT + Y_INTER_OFFSET)

            if left > ci.width:
                continue
            if up > ci.height:
                continue

            rect = (left, up, CARD_WIDTH + left, CARD_HEIGHT + up)
            cropped_im = ci.crop(rect)
            if not cropped_im.getbbox():
                continue
            # cropped_im.show()
            cropped_im.save(os.path.join(fpath, f"{i}.png"))
            i += 1
    
