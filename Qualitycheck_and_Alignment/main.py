import cv2
import numpy as np

def main():
    selfie = cv2.imread('WIN_20231016_11_29_08_Pro.jpg')
    #id = cv2.imread('id.jpg')
    type = input("Which type of ID do you want to use? For Passport type 1, Drivers license type 2, or ID card type 3: ")
    if type == "1":
        id = cv2.imread('passs.jpg')
        template_id = cv2.imread('passport_template.jpg')
    elif type == "2":
        template_id = cv2.imread('template.jpg')
        id = cv2.imread('id.jpg')
    elif type == "3":
        id = cv2.imread('id_kort.png')
        template_id = cv2.imread('id_card_template.png')
    else:
        print("Invalid ID type selected. Using the default template.")
        return -1
    #template_id = cv2.imread('id_card_template.png')
    quality(selfie)
    variabel = quality(id)
    good_match_precent = 0.15
    max_features = 10000
    imReg, h = align(id, template_id, max_features, good_match_precent)

    print("Estimated homography : \n", h)
    cv2.imshow("Aligned", imReg)  # Display the aligned image
    #cv2.imshow("matches", align(id, template_id, max_features, good_match_precent))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def align(id, template_id, max_features, good_match_precent):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(id, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(template_id, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(max_features)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    matches = sorted(matches, key=lambda x: x.distance)
    numGoodMatches = int(len(matches) * good_match_precent)
    matches = matches[:numGoodMatches]
    imMatches = cv2.drawMatches(id, keypoints1, template_id, keypoints2, matches, None)
    #cv2.imwrite("matches.jpg", imMatches)
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    h, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
    height, width, channels = template_id.shape
    im1Reg = cv2.warpPerspective(id, h, (width, height))
    return im1Reg, h


def quality(image):
    min_width = 1500
    min_height = 1200
    max_sharpness = 700

    height, width, _ = image.shape
    laplacian = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F)
    sharpness = laplacian.var()
    print("Sharpness:", sharpness)
    if width >= min_width and height >= min_height and sharpness <= max_sharpness:
        print("Image quality meets the requirements.")
        return True
    else:
        print("Image quality does not meet the requirements.")
        return False

if __name__ == "__main__":
    main()