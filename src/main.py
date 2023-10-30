import cv2

imgPath = 'img/id.jpg'
img = cv2.imread(imgPath)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_classifier = cv2.CascadeClassifier(
    'src/haarcascade_frontalface_default.xml'
)

face = face_classifier.detectMultiScale(
    gray_img, scaleFactor=1.1, minNeighbors=5
)

for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)

cv2.imwrite("img/output.jpg", img)