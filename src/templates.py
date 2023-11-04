import cv2


def match(image, template, threshold=0.9):
    """Apply template matching to an image.

    Args:
        image: The image to apply template matching to.
        template: The template to match.
        threshold: The minimum score required for a match. Defaults to 0.9.

    Returns:
        True if the template matches the image with a score greater than or
        equal to the threshold, False otherwise.
    """
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val >= threshold


def match_set(identification, directory, threshold=0.9):
    """Apply template matching to all templates in directory.

    Each directory is expected to contain one or more templates, which
    corresponds to a set of templates. This function will try to match the
    identification against all templates in the directory, and return True if
    all templates matches the image with a score greater than or equal to the
    threshold.

    Args:
        identification: The image to apply template matching to.
        directory: The directory to the template set to match against.
        threshold: The minimum score required for a match. Defaults to 0.9.

    Returns:
        True if all templates within directory matches the identification with
        a score greater than or equal to the threshold, False otherwise.
    """
    print(f"Matching identification against [{directory.name}]")

    matched_template = False
    for template in directory.glob("*"):
        template_image = cv2.imread(str(template))
        matched_template = match(identification, template_image, threshold)
        if not matched_template:
            return False

    print(f"All templates in [{directory.name}] matched identification.")
    return True
