#!/usr/bin/python3

from pathlib import Path
import sys

import cv2

import cli
import templates

if __name__ == "__main__":
    args = cli.init_argparse()
    template_path = Path("images/templates")
    directories = [
        directory for directory in template_path.iterdir() if directory.is_dir()
    ]

    matched_id = False
    matched_template = None
    if args.id_image:
        if not Path(args.id_image).is_file():
            sys.exit(f"File [{args.id_image}] not found.", 1)

        image = cv2.imread(args.id_image)
        for directory in directories:
            matched_id = templates.match_set(image, directory)
            if matched_id:
                matched_template = directory.name
                break
