import cv2

# Load the image
image = cv2.imread('vangen999.jpg')

# Define quality requirements
min_width = 500
min_height = 500
max_sharpness = 110  # Adjusted for lower sharpness

# Check image quality
height, width, _ = image.shape
laplacian = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F)
sharpness = laplacian.var()
print("Sharpness:", sharpness)
# Compare to requirements
if width >= min_width and height >= min_height and sharpness <= max_sharpness:  # Inverted the condition
    print("Image quality meets the requirements.")
else:
    print("Image quality does not meet the requirements.")