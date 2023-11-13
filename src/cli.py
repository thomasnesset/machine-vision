import argparse


def init_argparse():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate identification and match with facial image.",
    )
    parser.add_argument(
        "-i",
        "--id-image",
        type=str,
        help="File path to identification image",
    )
    parser.add_argument(
        "-f",
        "--face-image",
        type=str,
        help="File path to facial image",
    )

    args = parser.parse_args()
    if args.id_image is None and args.face_image is None:
        parser.error("One of --id-image or --face-image is required")

    return args
