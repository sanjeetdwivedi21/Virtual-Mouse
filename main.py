
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

##############################
# Camera Settings
wCam, hCam = 640, 480
frameR = 100
##############################

# Cursor Settings
smoothening = 7

# FPS
pTime = 0

# Previous and Current Cursor Positions
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# First Movement Detection
isMoving = False

# Click Cooldown
clickCooldown = 0.35
lastClickTime = 0

##############################
# Webcam Setup
cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

# Hand Detector
detector = htm.HandDetector(
    maxHands=1,
    detectionCon=0.8
)

# Screen Size
wScr, hScr = autopy.screen.size()

##############################

while True:

    success, img = cap.read()

    if not success:
        print("Camera not detected!")
        break

    # Mirror Camera
    img = cv2.flip(img, 1)

    # Detect Hands
    img = detector.findHands(img)

    # Get Landmarks
    lmList, bbox = detector.findPosition(img)

    # Draw Working Area
    cv2.rectangle(
        img,
        (frameR, frameR),
        (wCam - frameR, hCam - frameR),
        (255, 0, 255),
        2
    )

    if len(lmList) != 0:

        # Index and Middle Finger Tips
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check Fingers
        fingers = detector.fingersUp()

        # --------------------------------
        # MODE 1: CURSOR MOVEMENT
        # --------------------------------

        if fingers[1] == 1 and fingers[2] == 0:

            # Convert Camera Coordinates to Screen Coordinates
            x3 = np.interp(
                x1,
                (frameR, wCam - frameR),
                (0, wScr - 1)
            )

            y3 = np.interp(
                y1,
                (frameR, hCam - frameR),
                (0, hScr - 1)
            )

            # Keep Coordinates Inside Screen
            x3 = np.clip(x3, 0, wScr - 1)
            y3 = np.clip(y3, 0, hScr - 1)

            # Adaptive Smoothing
            if not isMoving:

                clocX, clocY = x3, y3
                isMoving = True

            else:

                distance = np.hypot(
                    x3 - clocX,
                    y3 - clocY
                )

                alpha = np.interp(
                    distance,
                    [0, 100],
                    [0.08, 0.35]
                )

                # Smooth Cursor
                clocX += (x3 - clocX) * alpha
                clocY += (y3 - clocY) * alpha

            # Move Mouse
            autopy.mouse.move(clocX, clocY)

            # Highlight Index Finger
            cv2.circle(
                img,
                (x1, y1),
                15,
                (255, 0, 255),
                cv2.FILLED
            )

            plocX, plocY = clocX, clocY

        # --------------------------------
        # MODE 2: LEFT CLICK
        # --------------------------------

        if fingers[1] == 1 and fingers[2] == 1:

            length, img, lineInfo = detector.findDistance(
                8, 12, img
            )

            currentTime = time.time()

            if (
                length < 40
                and currentTime - lastClickTime > clickCooldown
            ):

                cv2.circle(
                    img,
                    (lineInfo[4], lineInfo[5]),
                    15,
                    (0, 255, 0),
                    cv2.FILLED
                )

                autopy.mouse.click()

                lastClickTime = currentTime

        # Reset movement when hand changes mode
        else:
            if fingers[1] == 0 or fingers[2] == 1:
                isMoving = False

    # --------------------------------
    # FPS Calculation
    # --------------------------------

    cTime = time.time()

    fps = 1 / max(cTime - pTime, 0.001)

    pTime = cTime

    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (20, 50),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (255, 0, 0),
        2
    )

    # --------------------------------
    # Display
    # --------------------------------

    cv2.imshow("AI Virtual Mouse", img)

    # Press Q to Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release Resources
cap.release()
cv2.destroyAllWindows()
