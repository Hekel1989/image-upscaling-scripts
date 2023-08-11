import os
from PIL import Image

# Create the "ToBeUpscaled" folder if it doesn't exist
os.makedirs("ToBeUpscaled", exist_ok=True)

# Find all images with height < 2000 pixels and move them to the "ToBeUpscaled" folder
for image in os.listdir():
    if image.lower().endswith(('.jpg', '.jpeg', '.png')):
        try:
            with Image.open(image) as img:
                height = img.size[1]
                if height < 2000:
                    os.rename(image, os.path.join("ToBeUpscaled", image))
                    print(f"Moved: {image}")
        except Exception as e:
            # If the image cannot be opened or other error occurs, skip it
            print(f"Error processing '{image}': {e}")

# Inform the user about the process completion
print("All images with height < 2000 pixels have been moved to the 'ToBeUpscaled' folder.")
