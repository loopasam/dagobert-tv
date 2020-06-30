import cv2
import datetime
import time


class Recorder:
    def __init__(self):
        self.frame_counter = 0
        self.is_recording = False
        self.timestamp = None
        self.prebuffer = []
        self.prebuffer_size = 100
        self.movie_buffer = []
        self.minimum_movement_area = 200

    @staticmethod
    def get_new_movie(timestamp):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        path = '/home/loopasam/Google Drive/ubuntu-bin/'
        movie = cv2.VideoWriter(path + timestamp + '.mp4', fourcc, 20.0, (640, 480))
        return movie

    @staticmethod
    def get_timestamp():
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    def record(self, frame, movement_area):

        self.prebuffer.append(frame)
        if len(self.prebuffer) > self.prebuffer_size:
            del self.prebuffer[0]

        if not self.is_recording and movement_area > self.minimum_movement_area:
            self.is_recording = True
            print('starting recording...')
            self.timestamp = self.get_timestamp()
            self.movie_buffer = self.prebuffer[:]

        if self.is_recording:
            if self.frame_counter > 100:
                self.is_recording = False
                self.frame_counter = 0
                print('saving recording...')
                movie = self.get_new_movie(self.timestamp)
                for frame in self.movie_buffer:
                    movie.write(frame)
                movie.release()
                print('saved recording...')
            else:
                # Continue to record
                self.frame_counter += 1
                print(self.frame_counter)

            if movement_area > self.minimum_movement_area:
                self.frame_counter = 0

            self.movie_buffer.append(frame)
