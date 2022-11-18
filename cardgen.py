from PIL import Image, ImageDraw, ImageFont
import csv
import shutil
import os

isStarEnabled = True

def save_with_name(name, direction, backgroundImage, number = 1):
    defaultFileName = "outcards/" + name.replace(" ", "") + direction + str(number) + ".png"
    if (os.path.exists(defaultFileName)):
        save_with_name(name, direction, backgroundImage, number + 1)
    else:
        backgroundImage.save(defaultFileName)

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

def draw_card( name, cost, value, effect, rotation):
    for direction in "LR":
        backgroundImage = Image.open('resources/genericCard.png')
        arrow = Image.open("resources/" + direction + "arrow.png")
        draw = ImageDraw.Draw(backgroundImage)
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=15)
        draw.text((53, 32), name, font=font)
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=25)
        draw.text((25, 25), str(cost), font=font, fill="black")
        if isStarEnabled:
            draw.text((25, 150), str(value), font=font, fill="black")
        draw.text((110, 150), str(rotation), font=font, fill="black")
        
        font = ImageFont.truetype("fonts/Roboto-Thin.ttf", size=12)
        
        effectText = get_wrapped_text(effect, font, 80)
        draw.multiline_text((53,53),effectText, fill="black")
        backgroundImage.paste(arrow, (85, 155))
        save_with_name(name, direction, backgroundImage)

try:
    shutil.rmtree("outcards/")
finally:
    os.mkdir("outcards")

with open('cards.csv', newline='') as csvfile:
    for row in csv.reader(csvfile, delimiter=';', quotechar='|'):
        draw_card(row[0], row[1], row[2], row[4], row[3])

#draw_card("Lockdown", 6, 6, "Once the second lockdown is played, every other player gets one more turn.", 1)
