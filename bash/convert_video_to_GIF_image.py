# mp4_converter_gui.py

import glob
import os
import shutil

import cv2
from PIL import Image

file_types = [("MP4 (*.mp4)", "*.mp4"), ("All files (*.*)", "*.*")]


def convert_mp4_to_jpgs(path):
    print(f"\n - exporting pictures from the video {path}")
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0
    if os.path.exists("output"):
        # remove previous GIF frame files
        shutil.rmtree("output")
    try:
        os.mkdir("output")
    except IOError:
        print("Error occurred creating output folder")
        return

    while still_reading:
        cv2.imwrite(f"output/frame_{frame_count:05d}.jpg", image)
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1


def make_gif(gif_path, frame_folder="output"):
    print(f"\n - making the GIF {gif_path}")
    images = glob.glob(f"{frame_folder}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(
        gif_path,
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=50,
        loop=0,
    )


def main():
    mp4_path = "docs/sentiment-analysis.mp4"
    gif_path = "docs/sentiment-analysis.gif"

    convert_mp4_to_jpgs(mp4_path)
    make_gif(gif_path)
    print(f"GIF created: {gif_path}")


if __name__ == "__main__":
    main()
