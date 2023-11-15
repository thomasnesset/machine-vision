import cv2
import numpy as np

def read_image(file_path):
    """Read an image from a file."""
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def find_face(image):
    """Detect faces in an image and return the first found face."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) == 0:
        return None
    
    x, y, w, h = faces[0]
    face = image[y:y+h, x:x+w]
    return face

def compare_faces(face1, face2):
    """Compare two faces and return True if they are similar."""
    if face1 is None or face2 is None:
        return False

    # Resize faces to the same size for comparison
    face1 = cv2.resize(face1, (100, 100))
    face2 = cv2.resize(face2, (100, 100))

    # Calculate the difference and similarity
    difference = cv2.absdiff(face1, face2)
    similarity = np.sum(difference)

    # A lower similarity score means more similar faces
    threshold = 1000000 # Adjust this threshold as needed
    return similarity < threshold

# Load the reference image and the image to compare
reference_image = read_image("reference.jpg") 
image_to_compare = read_image("other_image.jpg") # replace with designated picture

# Find faces in both images
reference_face = find_face(reference_image)
comparison_face = find_face(image_to_compare)

# Compare the faces
if compare_faces(reference_face, comparison_face):
    print("Faces match.")
else:
    print("Faces do not match.")
