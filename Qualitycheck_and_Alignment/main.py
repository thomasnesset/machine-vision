import cv2
import numpy as np

def main():
    selfie = cv2.imread('vangen99.jpg')
    template_id = cv2.imread('template.jpg')
    id = cv2.imread('uia.jpg')
    quality(selfie)
    good_match_precent = 0.15
    max_features = 2500
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
    cv2.imwrite("matches.jpg", imMatches)
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    h, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
    height, width, channels = template_id.shape
    im1Reg = cv2.warpPerspective(id, h, (width, height))
    return im1Reg, h

def quality(selfie):
    # Define quality requirements
    min_width = 1000
    min_height = 700
    max_sharpness = 75  # Adjusted for lower sharpness

    # Check selfie quality
    height, width, _ = selfie.shape
    laplacian = cv2.Laplacian(cv2.cvtColor(selfie, cv2.COLOR_BGR2GRAY), cv2.CV_64F)
    sharpness = laplacian.var()
    print("Sharpness:", sharpness)

    # Compare to requirements
    if width >= min_width and height >= min_height and sharpness <= max_sharpness:
        print("selfie quality meets the requirements.")
    else:
        print("selfie quality does not meet the requirements.")

if __name__ == "__main__":
    main()