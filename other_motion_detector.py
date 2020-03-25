import cv2
import numpy as np

# Frame counter
frame_counter = 0

# Recording flag
is_recording = False

# The video file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


# capturing video
cap = cv2.VideoCapture(0)

# reading back-to-back frames(images) from video
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():

    # Difference between frame1(image) and frame2(image)
    diff = cv2.absdiff(frame1, frame2)

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur, so that change can be find easily
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # If pixel value is greater than 20, it is assigned white(255) otherwise black
    # TODO this 20 is a hard value, that could be modified depending on desired sensitivity
    _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=4)

    # finding contours of moving object
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    movement_detected = False

    if is_recording:
        if frame_counter > 30:
            is_recording = False
            print('saving recording...')
            # TODO save the file
            out.release()
            print('saved recording...')
            # fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        else:
            # Continue to record
            frame_counter += 1

    # making rectangle around moving object
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 700:
            # register the fact that a mvt has been spotted
            if not is_recording:
                is_recording = True
                print('starting recording...')
            movement_detected = True
            frame_counter = 0
            # TODO reset the frame counter until end of video
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 255), 2)
            out.write(frame1)

    # if movement_detected:
    #     print('busted')

    # Display original frame
    cv2.imshow('Motion Detector', frame1)

    # Display Difference Frame
    # cv2.imshow('Difference Frame', thresh)

    # Assign frame2(image) to frame1(image)
    frame1 = frame2

    # Read new frame2
    ret, frame2 = cap.read()

    # Press 'esc' for quit
    # TODO no idea how to remove it from the code
    if cv2.waitKey(40) == 27:
        break


# Release cap resource
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
