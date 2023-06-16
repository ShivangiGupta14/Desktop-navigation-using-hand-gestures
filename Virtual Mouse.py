import cv2
import numpy as np
import time
import HandTracking as htm
import pyautogui

""" Variables Declaration """
pTime = 0  # Used to calculate frame rate
width =640 # Width of Camera
height = 580 # Height of Camera
frameR = 100  # Frame Reduction
smoothening = 8  # Smoothening Factor
prev_x, prev_y = 0, 0  # Previous coordinates
curr_x, curr_y = 0, 0  # Current coordinates
cap = cv2.VideoCapture(0)  # Getting video feed from the webcam
cap.set(3, width)  # Adjusting size
cap.set(4, height)

screen_width, screen_height = pyautogui.size()  # Getting the screen size
detector = htm.handDetector(maxHands=1)  # Detecting one hand at max
while True:

    success, img = cap.read()
    img = detector.findHands(img)  # Finding the hand
    lmlist, bbox = detector.findPosition(img)  # Getting position of hand

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        # Smoothening the value
        x3 = np.interp(x1, (frameR, width - frameR), (0, screen_width))
        y3 = np.interp(y1, (frameR, height - frameR), (0, screen_height))

        curr_x = prev_x + (x3 - prev_x) / smoothening
        curr_y = prev_y + (y3 - prev_y) / smoothening

        fingers = detector.fingersUp()  # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255),
                      2)  # Creating boundary box

        if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0:  # If fore finger is up and thumb and middle
            # finger is down
            pyautogui.moveTo(screen_width - curr_x, curr_y)  # Moving the cursor
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[0] == 1 and fingers[1] == 1 and fingers[
            2] == 0:  # If fore finger & thumb both are up and middle finger is down
            length, img, lineInfo = detector.findDistance(4, 8, img)

            if length < 40:  # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='left')  # Perform left button Click

        if fingers[1] == 1 and fingers[2] == 1 and fingers[
            0] == 0 and fingers[3] == 0 and fingers[4] == 0:  # If fore finger & middle finger both are up and
            # remaining are down
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:  # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='right')  # Perform right button Click
            else:
                prev_posX, prev_posY = pyautogui.position()  # finding position of mousse
                pyautogui.moveTo(screen_width - curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y
                curr_posX, curr_posY = pyautogui.position()

                if curr_posY < prev_posY:
                    pyautogui.scroll(50)  # Scroll up
                    prev_posX, prev_posY = curr_posX, curr_posY
                elif curr_posY > prev_posY:
                    pyautogui.scroll(-50)  # Scroll down
                    prev_posX, prev_posY = curr_posX, curr_posY

        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:  # If
            # thumb, fore finger & middle finger all are up and remaining are down
            length1, img1, lineInfo1 = detector.findDistance(4, 8, img)
            length2, img2, lineInfo2 = detector.findDistance(8, 12, img)

            if length1 < 40 and length2 < 40:  # If all three fingers are really close to each other
                cv2.circle(img1, (lineInfo1[4], lineInfo1[5]), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img2, (lineInfo2[4], lineInfo2[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.doubleClick()  # Perform double(left button) click

    """ Calculating the frame rate and """
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()