"""
You can use this file to execute your code. You are NOT required
to use this file, and ARE ALLOWED to make ANY changes you want in
THIS file. This file will not be submitted with your assignment
or report, so if you write code for above & beyond effort, make sure
that you include important snippets in your writeup. CODE ALONE IS
NOT SUFFICIENT FOR ABOVE AND BEYOND CREDIT.

    DO NOT SHARE CODE (INCLUDING TEST CASES) WITH OTHER STUDENTS.
"""

import dollyzoom
import os
from os import path
import cv2
import argparse
import errno

SRC_FOLDER = "images/input"
OUT_FOLDER = "images/output"
EXTENSIONS = set(["bmp", "jpeg", "jpg", "png", "tif", "tiff"])


def main(image_folder, output_folder, mask_size, mask_offset):

    image_files = [os.path.join(image_folder, name) for name in os.listdir(image_folder)]
    inputs = ((name, cv2.imread(name)) for name in sorted(image_files)
              if path.splitext(name)[-1][1:].lower() in EXTENSIONS)

    # start with the first image in the folder and process each image in order
    name, img = inputs.next()
    print "\n  Starting with: {}".format(name)
    index = 0
    cv2.imwrite(path.join(output_folder, "img_{:04d}.jpg".format(index)), img)
    for name, next_img in inputs:

        if next_img is None:
            print "\nUnable to proceed: {} failed to load.".format(name)
            return

        print "  Adding: {}".format(name)
        image1_kp, image2_kp, matches = dollyzoom.findMatchesBetweenImages(next_img, img, 50, mask_offset, mask_size)
        transform = dollyzoom.findAffineTransform(image1_kp, image2_kp, matches)
        result = dollyzoom.applyTransform(next_img, transform, img)

        img = result
        index += 1
        cv2.imwrite(path.join(output_folder, "img_{:04d}.jpg".format(index)), result)

    print "  Done!"


if __name__ == "__main__":
    """
    Generate dolly zoom from the images in each subdirectory of SRC_FOLDER
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", help="Source directory that contains the images")
    parser.add_argument("output_dir", help="Destination directory for images")
    parser.add_argument("--mask_offset", default=[0.5, 0.5], metavar=("y", "x"), type=float, help="Mask offset relative to image size. e.g. 0.5 0.5", nargs=2)
    parser.add_argument("--mask_size", default=[0.5, 0.5], metavar=("y", "x"), type=float, help="Mask size relative to image size. e.g. 0.2 0.2", nargs=2)

    args = parser.parse_args()

    try:
        os.makedirs(args.output_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    main(args.source_dir, args.output_dir, args.mask_offset, args.mask_size)


