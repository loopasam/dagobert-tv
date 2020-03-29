import cv2
import datetime
import time


class Recorder:
    def __init__(self):
        self.frame_counter = 0
        self.is_recording = False
        self.movie = None
        self.buffer = []

    @staticmethod
    def get_new_movie():
        ts = time.time()
        time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        movie = cv2.VideoWriter(time_stamp + '.mp4', fourcc, 20.0, (640, 480))
        return movie

    def record(self, frame, size_area):

        # TODO keep a buffer with n images always full, to be added in the beginning of the recording
        self.buffer.append(frame)
        if len(self.buffer) > 100:
            del self.buffer[0]

        if not self.is_recording and size_area > 700:
            self.is_recording = True
            print('starting recording...')
            self.movie = self.get_new_movie()
            for frame in self.buffer:
                self.movie.write(frame)

        if self.is_recording:
            if self.frame_counter > 100:
                self.is_recording = False
                print('saving recording...')
                self.movie.release()
                print('saved recording...')
            else:
                # Continue to record
                self.frame_counter += 1
                print(self.frame_counter)

            if size_area > 700:
                self.frame_counter = 0

            # TODO record eveything using a RAM buffer
            self.movie.write(frame)
