import cv2


def quality(image):
    min_width = 1500
    min_height = 1200
    max_sharpness = 700

    height, width, _ = image.shape
    laplacian = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F)
    sharpness = laplacian.var()
    if width >= min_width and height >= min_height and sharpness <= max_sharpness:
        print("Image quality meets the requirements.")
        return True
    else:
        print("Image quality does not meet the requirements.")
        return False
