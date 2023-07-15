import logging
import os.path
import time
from shutil import copy

import cv2

import api.background_check as  background_check
import api.blur_check as blur_check
import api.file_format_check as file_format_check
import api.file_size_check as file_size_check
import api.grey_black_and_white_check as grey_black_and_white_check
import api.head_check as head_check

logging.basicConfig(level=logging.INFO)


def main(directory):
    initialTime = time.time()

    # make valid and invalid directories
    validDirectory = directory + "/" + "valid/"
    invalidDirectory = directory + "/" + "invalid/"
    resultFile = directory + '/result.csv'

    if  not os.path.exists(validDirectory):
         os.mkdir(validDirectory)
    if not os.path.exists(invalidDirectory):
        os.mkdir(invalidDirectory)
    if os.path.exists(resultFile):
        os.remove(resultFile)

    error_message = {}
    fileLists = sorted(os.listdir(directory))
    for image in fileLists:
        logging.info("processing Image: " + image)

        messages = []

        imagePath = directory + "/" + image

        if  os.path.isdir(imagePath):
            continue

        # Check image file format
        is_file_format_valid = file_format_check.check_image(imagePath)
        if not is_file_format_valid:
            messages.append("File format check failed")
       

        is_file_size_valid = file_size_check.check_image(imagePath)
        if not is_file_size_valid:
            messages.append("File size check failed")
           

        is_file_height_valid = file_size_check.check_height(imagePath)
        if not is_file_height_valid:
            messages.append("File height check failed")
          

        is_file_width_valid = file_size_check.check_width(imagePath)
        if not is_file_width_valid:
            messages.append("File width check failed")
       

        # Load the image
        img = cv2.imread(imagePath)

        # Check if corrupted image
        if file_format_check.is_corrupted_image(img):
            messages.append("Corrupted Image")

        # Check for grey image
        if grey_black_and_white_check.is_grey(img):
            messages.append("GreyScale Check Failed")

        # Check image for blurness
        if blur_check.check_image_blurness(img):
            messages.append("Blurness Check Failed")

        # Check the background of image
        if not background_check.background_check(img):
            messages.append("Background check failed")

        # Check image for head position and coverage

        if not head_check.valid_head_size(img):
            messages.append("Head check Faied")

        if head_check.is_eye_covered(img):
            messages.append("Eye checked failed")

        logging.info("Copying valid and invalid images to respective folders...")
        if len(messages) > 0:
            error_message[image] = messages
            copy(imagePath, invalidDirectory)
        else:
            copy(imagePath, validDirectory)
        # Display the imported image
        # cv2.imshow('Application Photo', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    csv_string = ""

    if (len(error_message) > 0):
        for name in error_message.keys():
            csv_string = csv_string + name
            for category in error_message[name]:
                csv_string = csv_string + ',' + category + "\n"
    else:
        print("There are no invalid images")
    logging.info("Writing result to result.csv... ")
    f = open(resultFile, 'w')
    f.write(csv_string)  # Give your csv text here.
    ## Python will convert \n to os.linesep
    f.close()
    # print(csv_string)
    finalTime = time.time()

    logging.info("Total Image Parsed = " + str(len(fileLists)))
    logging.info("Total Invalid Image = " + str(len(error_message)))
    logging.info("Total time taken to validate "
                 + str(len(fileLists)) + " images = " + str(finalTime - initialTime) + " seconds")


if __name__ == '__main__':
    main()
