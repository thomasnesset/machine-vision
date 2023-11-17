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
        template_path = Path("images/templates")
        files = [file for file in template_path.iterdir() if file.is_file()]
        matched_id = []
        image = cv2.imread(args.id_image)
        if not image_verification.quality(image):
            print("Image quality for ID card is too low.", file=sys.stderr)
            exit()

        for file in files:
            template = cv2.imread(str(file))
            score = match.match_orb(image, template, 100, 10)
            print(f"template: {str(file)}, Score: {score}")
            if score >= 0.5:
                matched_id.append({"filename": file, "score": score})

        if matched_id.__len__() == 0:
            print("Could not match ID.", file=sys.stderr)
            exit()

        match = recognition.match_id_face(args.id_image)
        if match:
            print("ID matches person!")
        else:
            print("ID does not match person!")

        best_match = max(matched_id, key=lambda x: x["score"])
        print(f"ID matched with [{best_match['filename'].name}]")
