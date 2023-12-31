import face_recognition


def match_face(id_, snapshot_):
    id = face_recognition.load_image_file(id_)
    id_face_enc = face_recognition.face_encodings(id)[0]

    snapshot = face_recognition.load_image_file(snapshot_)
    snapshot_face_enc = face_recognition.face_encodings(snapshot)
    if snapshot_face_enc.__len__() == 0:
        return False

    return face_recognition.compare_faces([snapshot_face_enc[0]], id_face_enc)
