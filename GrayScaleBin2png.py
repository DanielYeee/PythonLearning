from PIL import Image
import numpy as np

# Parameters (example values, modify as needed)
width = 256
height = 256

# Step 1: Read the binary file
with open('input.bin', 'rb') as f:
    data = f.read()

# Step 2: Interpret the data
# Assuming the binary data represents grayscale values
image_data = np.frombuffer(data, dtype=np.uint8).reshape((height, width))

# Step 3: Create the image
image = Image.fromarray(image_data, 'L')
image.save('output.png')
