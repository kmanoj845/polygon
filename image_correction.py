import cv2
from PIL import Image
import numpy as np

def do_image_correction(image_path, blue_w=0, green_w=0, red_w=0):
    
    image = cv2.imread(image_path)

    if all(w == 0 for w in (blue_w, green_w, red_w)):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("All weights are zero. Using cv2.COLOR_BGR2GRAY to make grayscale image.")
    else:
        RGB_image = image
        blue = RGB_image[:,:,0]
        green = RGB_image[:,:,1]
        red = RGB_image[:,:,2]
        image = (blue_w * blue) + (green_w * green) + (red_w * red)
        image = image.astype(np.uint8)
    
    # Median blur
    filtered_image = cv2.medianBlur(image, ksize=5)  # ksize must be odd
    
    #Erode the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    eroded_image = cv2.erode(255 - filtered_image, kernel, iterations=1)
    
    # Convert the NumPy array to a PIL Image
    image = Image.fromarray(255 - eroded_image)
    return image
