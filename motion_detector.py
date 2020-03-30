from Camera import Camera
from Recorder import Recorder


def main():
    # TODO pass the configuration, such as sensitivity, etc.
    recorder = Recorder()
    camera = Camera()

    while camera.is_opened():

        frame, movement_area = camera.run()

        recorder.record(frame, movement_area)

    # Release cap resource
    camera.release()


if __name__ == "__main__":
    main()
