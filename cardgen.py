from PIL import Image, ImageDraw, ImageFont
import csv
import shutil
import os
from enum import Enum
import random

class ResourceType (Enum):
    NUMBERS = 1
    RPS = 2
    ONION = 3
    COLORS = 4

currentResource = ResourceType.COLORS

isStarEnabled = True

def save_with_name(name, direction, backgroundImage, number = 1):
    defaultFileName = "outcards/" + name.replace(" ", "") + direction + str(number) + ".png"
    if (os.path.exists(defaultFileName)):
        save_with_name(name, direction, backgroundImage, number + 1)
    else:
        backgroundImage = backgroundImage.convert('RGB')
        # Uncomment this if doing rapid prototyping
        backgroundImage = backgroundImage.resize((144, 198))
        backgroundImage.save(defaultFileName, format="PNG")

def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return '\n'.join(lines)

def GetRPS(costString):
    cost = int(costString)
    if cost == 1:
        image = Image.open('resources/rock.png')
    elif cost == 2:
        image = Image.open('resources/paper.png')
    elif cost == 3:
        image = Image.open('resources/scissors.png')
    else:
        return None
    return image

def GetResourceColor(costString):
    cost = int(costString)
    if cost == 1:
        return 'purple'
    elif cost == 2:
        return 'green'
    elif cost == 3:
        return 'orange'
    elif cost == 4:
        return 'pink'
    else:
        return None

    
def draw_card(name, cost, value, effect, rotation):
    if currentResource == ResourceType.COLORS:
        colors = ['1','2','3','4']
        numColorReps = 2
    else:
        numColorReps = 1

    for x in range(numColorReps):
        for direction in "LR":
            finalImage = Image.new("RGB", (600, 825), color=0)
            back = Image.open('resources/genericCard.png')
            
            finalImage.paste(back)

            draw = ImageDraw.Draw(finalImage)

            #title text
            titleFontSize= 50
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=50)
            while (font.getlength(name) > 600):
                titleFontSize -= 1
                font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=titleFontSize)
                
            draw.text((250, 120), ''.join([i for i in name if not i.isdigit()]), font=font)
            colorVal = ""
            # cost text
            if currentResource == ResourceType.NUMBERS:
                font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=110)
                draw.text((100, 100), str(cost), font=font, fill=0)
            elif currentResource == ResourceType.RPS:
                image = GetRPS(cost)
                image = image.resize((160, 160))
                finalImage.paste(image, (60, 90), mask=image)
            elif currentResource == ResourceType.ONION:
                image = Image.open('resources/Onion' + cost + ".png")
                image = image.resize((160, 160))
                finalImage.paste(image, (60, 90), mask=image)
            elif currentResource == ResourceType.COLORS:
                colorVal = str(colors[random.randrange(len(colors))])
                color = GetResourceColor(colorVal)
                image = ImageDraw.Draw(finalImage)
                image.rectangle([(88, 117), (188, 217)], fill = color, outline = 'black')
                colors.remove(colorVal)

            if isStarEnabled:
                draw.text((130, 680), str(value), font=font, fill=0, anchor="mm")
            
            # Effect descriptions
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=50)
            effectText = get_wrapped_text(effect, font, 350)
            draw.multiline_text((210,220),effectText, fill=0, font=font)


            arrow = Image.open("resources/" + direction + "arrow.png")
            if arrow.mode == 'RGBA':
                alpha = arrow.split()[3]
                bgmask = alpha.point(lambda x: 255-x)
                arrow = arrow.convert('RGB')
                arrow.paste((255,255,255), None, bgmask)

            arrow = arrow.resize((160, 176))
            finalImage.paste(arrow, (400, 600))
            #Rotation text
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=110)
            draw.text((450, 600), str(rotation), font=font, fill=0)
            save_with_name(name + colorVal, direction, finalImage)

try:
    shutil.rmtree("outcards/")
finally:
    os.mkdir("outcards")

with open('cards.csv', newline='') as csvfile:
    for row in csv.reader(csvfile, delimiter=';', quotechar='|'):
        if currentResource == ResourceType.RPS:
            draw_card(row[0] + '1', 1, row[2], row[4], row[3])
            draw_card(row[0] + "2", 2, row[2], row[4], row[3])
            draw_card(row[0] + "3", 3, row[2], row[4], row[3])
        if currentResource == ResourceType.COLORS:
            draw_card(row[0], 1, row[2], row[4], row[3])
        else:
            draw_card(row[0], row[1], row[2], row[4], row[3])

#draw_card("Lockdown", 6, 6, "Once the second lockdown is played, every other player gets one more turn.", 1)
