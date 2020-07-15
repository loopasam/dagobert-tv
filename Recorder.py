import cv2
import datetime
import time
from pathlib import Path


class Recorder:
    def __init__(self):
        self.frame_counter = 0
        self.is_recording = False
        self.timestamp = None
        self.prebuffer = []
        self.prebuffer_size = 20
        self.movie_buffer = []
        self.minimum_start_movement_area = 700
        self.minimum_keep_movement_area = 50

        # Meta information to debug
        self.n_total_frames = 0
        self.total_movement_area = 0
        self.start_movement_area = 0
        self.n_resets = 0

        # Prepare the log file if not existing
        log = Path('/home/loopasam/Google Drive/ubuntu-bin/log.tsv')
        if not log.exists():
            with open('/home/loopasam/Google Drive/ubuntu-bin/log.tsv', 'w') as log:
                log.write('file\tn_total_frames\ttotal_movement_area\tstart_movement_area\tn_resets\n')

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

        if not self.is_recording and movement_area > self.minimum_start_movement_area:
            self.is_recording = True
            self.timestamp = self.get_timestamp()
            self.movie_buffer = self.prebuffer[:]

            # Register the metadata
            self.start_movement_area = movement_area
            self.total_movement_area = movement_area

            print('starting recording...')
            print(self.timestamp)

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

                # Save and reset the meta-data
                # print('n_total_frames', self.n_total_frames)
                # print('total_movement_area', self.total_movement_area)
                # print('start_movement_area', self.start_movement_area)
                # print('n_resets', self.n_resets)

                with open('/home/loopasam/Google Drive/ubuntu-bin/log.tsv', 'a') as log:
                    line = '\t'.join([str(self.timestamp), str(self.n_total_frames), str(self.total_movement_area),
                                      str(self.start_movement_area), str(self.n_resets)])
                    log.write(line + '\n')

                self.n_total_frames = 0
                self.total_movement_area = 0
                self.start_movement_area = 0
                self.n_resets = 0

            else:
                # Continue to record
                self.frame_counter += 1
                # print(self.frame_counter)
                self.n_total_frames += 1

            if movement_area > self.minimum_keep_movement_area:
                self.frame_counter = 0
                self.n_resets += 1
                self.total_movement_area += movement_area

            self.movie_buffer.append(frame)
