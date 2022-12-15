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
        backgroundImage = backgroundImage.convert('RGB')
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

def draw_card( name, cost, value, effect, rotation):
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
            
        draw.text((250, 120), name, font=font)

        # cost text
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=110)
        draw.text((100, 100), str(cost), font=font, fill=0)
        if isStarEnabled:
            draw.text((130, 680), str(value), font=font, fill=0, anchor="mm")
        draw.text((450, 630), str(rotation), font=font, fill=0)
        
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=50)
        
        effectText = get_wrapped_text(effect, font, 350)
        draw.multiline_text((210,220),effectText, fill=0, font=font)


        arrow = Image.open("resources/" + direction + "arrow.png")
        if arrow.mode == 'RGBA':
            alpha = arrow.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            arrow = arrow.convert('RGB')
            arrow.paste((255,255,255), None, bgmask)

        arrow = arrow.resize((100, 110))
        finalImage.paste(arrow, (350, 630))
        save_with_name(name, direction, finalImage)

try:
    shutil.rmtree("outcards/")
finally:
    os.mkdir("outcards")

with open('cards.csv', newline='') as csvfile:
    for row in csv.reader(csvfile, delimiter=';', quotechar='|'):
        draw_card(row[0], row[1], row[2], row[4], row[3])

#draw_card("Lockdown", 6, 6, "Once the second lockdown is played, every other player gets one more turn.", 1)
