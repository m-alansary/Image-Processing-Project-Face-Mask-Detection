def test_and_detect():
    import cv2

    # Load the cascade
    cascadeFace = cv2.CascadeClassifier('haarcascade_default.xml')

    # Capture the video from webcam
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = cascadeFace.detectMultiScale(gray, 1.3, 5, minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE)

        for (p1, p2, p3, p4) in faces:
            cv2.rectangle(img, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2) # BGR

        cv2.imshow('Test Camera', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
