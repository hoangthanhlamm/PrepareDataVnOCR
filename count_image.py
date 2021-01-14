import os
import argparse

dir_path = os.path.dirname(__file__)


def parse_args():
    parser = argparse.ArgumentParser(description='Recommendation System')

    parser.add_argument(
        '-f', '--folder',
        help='Folder to count',
        default='0'
    )

    return parser.parse_args()


def count_image():
    args = parse_args()
    folder = args.folder
    folder_path = os.path.join(os.path.join(dir_path, 'data'), folder)

    files = os.listdir(folder_path)
    print("Number of images in folder {:}: {:}".format(folder, len(files)))


if __name__ == '__main__':
    count_image()
