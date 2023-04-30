import argparse

def parse_arguments() -> argparse.Namespace:
    # Create argument parser and add webcam resolution argument
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", type=int, default=[640,480], nargs=2)
    args = parser.parse_args()
    return args
