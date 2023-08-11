import os
import random
import string
import mimetypes

# Function to generate a random name (8 characters long) for the new image
def generate_random_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Get the current directory
current_dir = os.getcwd()

# Loop through all files in the current directory
for img in os.listdir(current_dir):
    img_path = os.path.join(current_dir, img)

    # Check if the file is a regular file
    if os.path.isfile(img_path):
        # Use the 'mimetypes' module to get the MIME type of the file
        file_type, _ = mimetypes.guess_type(img_path)
        
        # Check if the file is an image (has MIME type starting with "image/")
        if file_type and file_type.startswith("image/"):
            # Extract the image extension from the MIME type
            extension = file_type.split('/')[-1]
            
            # Generate a random name (8 characters long) for the new image
            newname = generate_random_name()
            
            # Rename the image file with the new random name and appropriate extension
            new_img_path = os.path.join(current_dir, f"{newname}.{extension}")
            os.rename(img_path, new_img_path)
