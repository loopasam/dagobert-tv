import cv2


class Camera:
    def __init__(self):
        # capturing video
        self.cap = cv2.VideoCapture(0)
        # reading back-to-back frames(images) from video
        ret, self.frame1 = self.cap.read()
        ret, self.frame2 = self.cap.read()

    def is_opened(self):
        return self.cap.isOpened()

    def run(self):
        # Difference between frame1(image) and frame2(image)
        diff = cv2.absdiff(self.frame1, self.frame2)

        # Converting color image to gray_scale image
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # cv2.imshow('gray', gray)

        # Converting gray scale image to GaussianBlur, so that change can be find easily
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # If pixel value is greater than 20, it is assigned white(255) otherwise black
        _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=4)

        # finding contours of moving object
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # making rectangle around moving object
        movement_area = 0
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            movement_area = cv2.contourArea(contour)
            if movement_area > 5:
                pass
                # register the fact that a mvt has been spotted: either add to current recording or srat a new one:
                cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (0, 255, 255), 2)

        # Display original frame
        cv2.imshow('Motion Detector', self.frame1)

        # Display Difference Frame
        # cv2.imshow('Difference Frame', thresh)

        # Assign frame2(image) to frame1(image)
        self.frame1 = self.frame2

        # Read new frame2
        ret, self.frame2 = self.cap.read()

        cv2.waitKey(40)

        return self.frame2, movement_area

    def release(self):
        self.cap.release()
        # Destroy all windows
        cv2.destroyAllWindows()

