from PIL import Image
import os
import io
from tqdm import tqdm

# Set the maximum image pixels to a high value to handle large images
Image.MAX_IMAGE_PIXELS = None

# Convert all PNG files to JPG whilst maintaining the original quality
def convert_png_to_jpg():
    print("Converting PNG files to JPG...")
    for filename in tqdm(os.listdir("."), desc="Converting", unit="file"):
        if filename.endswith(".png"):
            img = Image.open(filename)

            # Convert RGBA images to RGB
            if img.mode == "RGBA":
                img = img.convert("RGB")

            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            img.save(jpg_filename, "JPEG", quality=100)

# Delete all original PNG files
def delete_original_png_files():
    print("Deleting original PNG files...")
    for filename in tqdm(os.listdir("."), desc="Deleting", unit="file"):
        if filename.endswith(".png"):
            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            if os.path.isfile(jpg_filename):
                os.remove(filename)

# Remove alpha channel and resize all images to have a height of 2160 pixels,
# respecting the original aspect ratio, with a maximum file size of 3MB,
# and maintaining the highest possible quality
def resize_jpg_files():
    print("Resizing JPG files...")
    for filename in tqdm(os.listdir("."), desc="Resizing", unit="file"):
        if filename.endswith(".jpg"):
            try:
                img = Image.open(filename)

                # Remove alpha channel for RGBA images
                if img.mode == "RGBA":
                    img = img.convert("RGB")

                original_width, original_height = img.size
                new_height = 2160
                new_width = int(original_width * (new_height / original_height))
                img = img.resize((new_width, new_height), Image.LANCZOS)

                # Binary search for the optimal quality to meet the file size constraint
                min_quality = 1
                max_quality = 100
                target_size = 3000000  # 3MB in bytes
                current_quality = 95   # Starting quality

                while max_quality - min_quality > 1:
                    img_file = io.BytesIO()
                    img.save(img_file, "JPEG", quality=current_quality, optimize=True, dpi=(300, 300))
                    img_size = img_file.getbuffer().nbytes

                    if img_size < target_size:
                        min_quality = current_quality
                        current_quality = (current_quality + max_quality) // 2
                    else:
                        max_quality = current_quality
                        current_quality = (current_quality + min_quality) // 2

                # Save the image with the final determined quality
                jpg_filename = "4K_" + filename
                jpg_filename, _ = os.path.splitext(jpg_filename)
                jpg_filename += ".jpg"
                img.save(jpg_filename, "JPEG", quality=min_quality, optimize=True, dpi=(300, 300))

                # Delete original file if 4K_ file was successfully created
                if os.path.isfile(jpg_filename):
                    os.remove(filename)

            except Exception as e:
                print(f"\nError processing {filename}: {str(e)}", flush=True)

if __name__ == "__main__":
    convert_png_to_jpg()
    delete_original_png_files()
    resize_jpg_files()

