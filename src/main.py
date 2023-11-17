#!/usr/bin/python3

from pathlib import Path
import sys

import cv2

import cli
import image_verification
import match
import recognition


if __name__ == "__main__":
    args = cli.init_argparse()

    have_id = False
    if args.id_image:
        if not Path(args.id_image).is_file():
            print(f"File [{args.id_image}] not found.", file=sys.stderr)
            exit()
        have_id = True

    if have_id:
        image = cv2.imread(args.id_image)
        if not image_verification.quality(image):
            print("Image quality for ID card is too low.", file=sys.stderr)
            exit()

        best_match = best_match = match.match_id(image)
        if best_match:
            exit()

        match = recognition.match_id_face(args.id_image)
        if match:
            print("ID matches person!")
        else:
            print("ID does not match person!")
