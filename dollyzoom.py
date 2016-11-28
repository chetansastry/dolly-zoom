"""
General Process

1. Read images
2. For each successive pair of images (from closer to farther)
    2.1 Find matching pair of features
    2.2 Find a transform from image 2 to image 1
    2.3 Apply transform to image 2
    2.4 Crop image 2 and save
"""

import cv2
import numpy as np
from cv2 import ORB


def findMatchesBetweenImages(image_1, image_2, num_matches, mask_offset, mask_size):
    """
    Return the top list of matches between two input images.

    Args:
    ----------
        image_1 : numpy.ndarray
            The first image (can be a grayscale or color image)

        image_2 : numpy.ndarray
            The second image (can be a grayscale or color image)

        num_matches : int
            The number of desired matches. If there are not enough, return
            as many matches as you can.

    Returns:
    ----------
        image_1_kp : list[cv2.KeyPoint]
            A list of keypoint descriptors in the first image

        image_2_kp : list[cv2.KeyPoint]
            A list of keypoint descriptors in the second image

        matches : list[cv2.DMatch]
            A list of matches between the keypoint descriptor lists of
            length no greater than num_matches
    """
    matches = None       # type: list of cv2.DMath
    image_1_kp = None    # type: list of cv2.KeyPoint items
    image_1_desc = None  # type: numpy.ndarray of numpy.uint8 values.
    image_2_kp = None    # type: list of cv2.KeyPoint items.
    image_2_desc = None  # type: numpy.ndarray of numpy.uint8 values.

    orb = ORB()

    offset = (mask_offset[0] * image_1.shape[0], mask_offset[1] * image_1.shape[1])
    size = (mask_size[0] * image_1.shape[0], mask_size[1] * image_1.shape[1])
    mask = np.zeros(image_1.shape[:2], dtype=np.uint8)
    mask[offset[0] - size[0]/2:offset[0] + size[0]/2, offset[1] - size[1]/2:offset[1] + size[1]/2] = 255

    image_1_kp, image_1_desc = orb.detectAndCompute(image_1, mask)
    image_2_kp, image_2_desc = orb.detectAndCompute(image_2, mask)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(image_1_desc, image_2_desc)
    matches = sorted(matches, key=lambda x: x.distance)[:num_matches]

    return image_1_kp, image_2_kp, matches


def findAffineTransform(image_1_kp, image_2_kp, matches):
    """
    Returns the homography describing the transformation between the
    keypoints of image 1 and image 2.

    """
    image_1_points = np.zeros((len(matches), 1, 2), dtype=np.float32)
    image_2_points = np.zeros((len(matches), 1, 2), dtype=np.float32)

    for idx, match in enumerate(matches):
        image_1_points[idx, 0, :] = image_1_kp[match.queryIdx].pt
        image_2_points[idx, 0, :] = image_2_kp[match.trainIdx].pt

    transform = cv2.estimateRigidTransform(image_1_points, image_2_points, fullAffine=False)

    return transform


def applyTransform(next_img, transform, img):
    """
    Apply the provided affine transform to the second image while keeping the dimension (cropping it) to
    match the first image.
    """
    return cv2.warpAffine(next_img, transform, img.shape[1::-1])
