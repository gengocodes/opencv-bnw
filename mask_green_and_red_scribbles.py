import cv2
import numpy as np

input_path = "input_image_path.png"
output_mask = "output_image_path.png"

image = cv2.imread(input_path)
if image is None:
    raise FileNotFoundError(f"Could not load image: {input_path}")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# RED
lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([15, 255, 255])
lower_red2 = np.array([150, 50, 50])
upper_red2 = np.array([180, 255, 255])
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

# GREEN
lower_green = np.array([30, 30, 30])
upper_green = np.array([90, 255, 255])
mask_green = cv2.inRange(hsv, lower_green, upper_green)

# COMBINE
mask = cv2.bitwise_or(mask_red, mask_green)

# CLEAN MASK
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

# EXPAND A LITTLE BIT
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)

# WHITE = INPAINT, BLACK = KEEP ORIGINAL
_, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

cv2.imwrite(output_mask, mask)
print(f"Mask saved as: {output_mask}")
