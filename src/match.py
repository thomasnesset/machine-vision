from pathlib import Path
import sys

import cv2
import numpy as np


def match_orb(image, ref_image, max_features, num_matches, debug=None):
    """Match images using ORB.

    Args:
        image: The image to match.
        ref_image: The reference image to match against.
        max_features: The maximum number of features to detect.
        num_matches: The number of matches to use.
        debug: The filename to write the debug image to. Defaults to None.
    Returns:
        The ratio of matched keypoints to total keypoints.
    """
    image1_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(max_features)
    keypoints1, descriptors1 = orb.detectAndCompute(image1_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2, None)

    matches = sorted(matches, key=lambda x: x.distance)

    good_matches = int(len(matches) * num_matches)
    matches = matches[:good_matches]

    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
    ratio = float(mask.sum()) / mask.size

    if debug:
        debug_filename = f"match_orb-{debug}"
        print(f"DEBUG: Matching ratio: {ratio}")
        matched_image = cv2.drawMatches(
            image, keypoints1, ref_image, keypoints2, matches, None
        )
        print(f"DEBUG: Writing image with matches to '{debug_filename}'")
        cv2.imwrite(debug_filename, matched_image)

    return ratio


def match_id(image):
    template_path = Path("images/templates")
    files = [file for file in template_path.iterdir() if file.is_file()]

    matched_id = []
    for file in files:
        template = cv2.imread(str(file))
        score = match_orb(image, template, 100, 10)
        print(f"template: {str(file)}, Score: {score}")
        if score >= 0.3:
            matched_id.append({"filename": file, "score": score})

    if matched_id.__len__() == 0:
        print("Could not match ID.", file=sys.stderr)
        return None
    return max(matched_id, key=lambda x: x["score"])
