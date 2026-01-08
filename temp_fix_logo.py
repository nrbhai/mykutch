from PIL import Image
import os

path = r"c:\website_project\newkutch\assets\images\logo.png"

try:
    img = Image.open(path)
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Check for white (allow slight variance)
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(path, "PNG")
    print(f"Successfully made {path} transparent.")
except Exception as e:
    print(f"Error processing image: {e}")
