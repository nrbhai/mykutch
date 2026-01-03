from PIL import Image
import os

def make_transparent(input_path, output_path):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    # Get background color from top-left pixel
    bg_color = datas[0]
    # Tolerance for background variation (e.g., JPEG artifacts)
    tolerance = 20

    new_data = []
    for item in datas:
        # Check if pixel is close to background color
        if all(abs(item[i] - bg_color[i]) < tolerance for i in range(3)):
            new_data.append((255, 255, 255, 0)) # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved transparent logo to {output_path}")

# Source is the uploaded file
source_image = r"C:/Users/Niraj/.gemini/antigravity/brain/46c1bb16-3854-4d63-88b5-810b2d1e73e6/uploaded_image_1767422733762.png"
# Destination is the site asset
dest_image = r"c:\website_project\mykutch\site\assets\images\logo.png"

make_transparent(source_image, dest_image)
