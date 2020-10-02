import face_recognition


def main():
    # Load a sample picture and learn how to recognize it.
    obama_image = face_recognition.load_image_file("obama.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    biden_image = face_recognition.load_image_file("biden.jpg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Load a second sample picture and learn how to recognize it.
    andre_image = face_recognition.load_image_file("andre.jpg")
    andre_face_encoding = face_recognition.face_encodings(andre_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding,
        andre_face_encoding
    ]
    known_face_names = [
        "Barack Obama",
        "Joe Biden",
        "Andrezio"
    ]

    return known_face_encodings, known_face_names


