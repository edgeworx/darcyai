import cv2
import os
import pathlib

from darcyai.perceptor.coral.image_classification_perceptor import ImageClassificationPerceptor
from darcyai.input.camera_stream import CameraStream
from darcyai.output.live_feed_stream import LiveFeedStream
from darcyai.pipeline import Pipeline

def perceptor_input_callback(input_data, pom, config):
    return input_data.data


def live_feed_callback(pom, input_data):
    frame = input_data.data.copy()

    if len(pom.image_classification[0]) == 0:
        return frame

    label = pom.image_classification[1][0]
    cv2.putText(frame, str(label), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame


camera = CameraStream(video_device="/dev/video0", fps=20)

pipeline = Pipeline(input_stream=camera)

live_feed = LiveFeedStream(path="/", port=3456, host="0.0.0.0")
pipeline.add_output_stream("output", live_feed_callback, live_feed)

script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, "mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite")
labels_file = os.path.join(script_dir, "inat_bird_labels.txt")
image_classification = ImageClassificationPerceptor(model_path=model_file, threshold=0.5, labels_file=labels_file, top_k=1)

pipeline.add_perceptor("image_classification", image_classification, input_callback=perceptor_input_callback)

pipeline.run()
