import face_recognition
import cv2

def match_id_face(id_):
    # Press space to take a picture
    input("Press ENTER to take picture..")
    cam = cv2.VideoCapture(0)
    res, img = cam.read()

    if res:
        cv2.imwrite("person.jpg", img)
        cv2.destroyAllWindows()

    id = face_recognition.load_image_file(id_)
    id_face_enc = face_recognition.face_encodings(id)[0]

    person = face_recognition.load_image_file("person.jpg")
    p_face_enc = face_recognition.face_encodings(person)[0]

    return face_recognition.compare_faces([p_face_enc], id_face_enc)[0]
