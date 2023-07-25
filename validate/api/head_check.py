import cv2

def head_percentage(image):

    faces = getFaces(image)

    # Return false if there's not exactly one face in the picture
    if len(faces) != 1:
        return False

    # Get the only face data
    face = faces[0]
    width = face[2]
    height = face[3]

    # Calculate head percentage based on face percentage, multiplied by 1.25 to assume 75% of head is face
    head_percentage = (width*height)/(image.shape[0]*image.shape[1]) * 1.25 * 100

    # Image is valid if head percentage is between 30% and 80%
    if 20 <= head_percentage <= 80:
        return True
    return False

def getFaces(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Load cascade classifier training file for haarcascade
    haar_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Detect multiscale (some images may be closer to camera than others) images
    return haar_face_cascade.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=3);

def is_eye_covered(image):
    faces = getFaces(image)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes =[]
    if len(faces) < 0:
        return True
    for (x, y, w, h) in faces:
        roi_gray = gray_img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
    return len(eyes) == 0




def valid_head_size(image):
    if not head_percentage(image):
        return False
    return True

