import logging
import time

import cv2


import api.background_check as background_check
import api.blur_check as blur_check
import api.file_format_check as file_format_check
import api.file_size_check as file_size_check
import api.grey_black_and_white_check as grey_black_and_white_check
import api.head_check as head_check

logging.basicConfig(level=logging.INFO)


def main(imgPath):
    initial = time.time()
    message = ""

    # Check image file format
    is_file_format_valid = file_format_check.check_image(imgPath)
    message = message + "File format check: " + ('Passed' if is_file_format_valid else 'Failed') + "\n"
    logging.info(message)

    # if not is_file_format_valid:
    #     return "Not Valid Format"

    # Check image file size
    is_file_size_valid = file_size_check.check_image(imgPath)
    message = message + "File size check: " + ('Passed' if is_file_format_valid else 'Failed') + "\n"
    logging.info(message)

    # if not is_file_size_valid:
    #     return "Not Valid File Size"

    # Check height of the image
    is_file_height_valid = file_size_check.check_height(imgPath)
    message = message + "File Height check: " + ('Passed' if is_file_height_valid else 'Failed') + "\n"
    logging.info(message)

    # if not is_file_height_valid:
    #     return "Not Valid File Height"

  # Check width of the image
    is_file_width_valid = file_size_check.check_width(imgPath)
    message = message + "File Height check: " + ('Passed' if is_file_width_valid else 'Failed') + "\n"
    logging.info(message)

    # if not is_file_width_valid:
    #     return "Not Valid File Height"

    # Load the image
    img = cv2.imread(imgPath)

    is_corrupted = file_format_check.is_corrupted_image(img)
    message = message + "File Open Test: " + ('Passed' if not is_corrupted else 'Failed') + "\n"
    logging.info(message)
    if file_format_check.is_corrupted_image(img):
        exit()

    message = message + "Greyscale check: " + ('Passed' if not grey_black_and_white_check.is_grey(img) else 'Failed') + "\n"
    logging.info(message)

    # Check image for blurness
    is_blur = blur_check.check_image_blurness(img)
    message = message + "Blurness check: " + ('Passed' if not is_blur else 'Failed') + "\n"
    logging.info(message)

    # Check the background of image
    is_background_ok = background_check.background_check(img)
    message = message + "Background check: " + ('Passed' if is_background_ok else 'Failed') + "\n"
    logging.info(message)

    # Check image for head position and coverage
    is_head_valid = head_check.valid_head_size(img)
    message = message + "Head check: " + ('Passed' if is_head_valid else 'Failed') + "\n"
    logging.info(message)

    # Check Eye Covered
    is_eye_covered = head_check.is_eye_covered(img)
    message = message + "Eye check: " + ('Passed' if not is_eye_covered else 'Failed') + "\n"
    logging.info(message)

    # Display the imported image
    # cv2.imshow('Application Photo', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    final = time.time()
    logging.info("Total time in second = "+ str(final-initial))
    return message
