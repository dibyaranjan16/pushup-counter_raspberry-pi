import cv2
import mediapipe as mp
import os
import pyttsx3

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

counter = 0
stage = None
create = None
opname = "output.avi"
x=0

# Initialize the TTS engine
engine = pyttsx3.init()

def findPosition(image, draw=True):
    lmList = []
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            # cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return lmList

cap = cv2.VideoCapture(0)

with mp_pose.Pose(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as pose:

    while cap.isOpened():
        success, image = cap.read()
        image = cv2.resize(image, (640, 480))

        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        lmList = findPosition(image, draw=True)

        if len(lmList) != 0:
            cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
            cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)
            cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
            cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)

            if (lmList[12][2] and lmList[11][2] >= lmList[14][2] and lmList[13][2]):
                cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 255, 0), cv2.FILLED)
                cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 255, 0), cv2.FILLED)
                stage = "down"

            if (lmList[12][2] and lmList[11][2] <= lmList[14][2] and lmList[13][2]) and stage == "down":
                stage = "up"
                counter += 1
                counter2 = str(int(counter))
                print(counter)
                x+=1
                # Announce the message using TTS
                engine.say(f"{x} Push-up completed")
                engine.runAndWait()  # Wait for the announcement to complete
                # Optionally, you can also save the announcement to an audio file:
                # engine.save_to_file("Push-up completed", "pushup_completed.mp3")
        text = "{}:{}".format("Push Ups", counter)
        cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)
        cv2.imshow('MediaPipe Pose', image)

        if create is None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            create = cv2.VideoWriter(opname, fourcc, 30, (image.shape[1], image.shape[0]), True)
        create.write(image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

cv2.destroyAllWindows()