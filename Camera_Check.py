import cv2


def CheckCamera():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error: Could not load Haar cascade classifier.")
        return
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        ret, img = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.5, 5, minSize=(30, 30), flags=cv2.CASCADE_DO_CANNY_PRUNING)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
            # Display
            cv2.imshow('Webcam Check', img)
            # Stop if escape key is pressed
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()

