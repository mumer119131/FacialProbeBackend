import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import warnings
from PIL import Image
import io
from deepface import DeepFace
import numpy as np
import cv2


def generateImage(stability_api, prompt, random_img_name):
    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt=prompt,
        # seed=int(seed),
        steps=30,
        cfg_scale=8.0,
        width=512,
        height=512,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                # Save our generated images with their seed number as the filename.
                img.save(f"./images/{random_img_name}.png")


def compareImages(img_1_addr, img_2_addr):
    # Load the two images
    img1 = cv2.imread(img_1_addr)
    img2 = cv2.imread(img_2_addr)
    try:
        result = DeepFace.verify(img_1_addr, img_2_addr, model_name="Facenet")
    except:
        result = {'verified': False, 'distance': 1, 'threshold': 0.4}

    return result


def isFaceInImage(img_addr):
    # Load the two images
    img = cv2.imread(img_addr)
    try:
        result = DeepFace.extract_faces(img_addr, detector_backend='opencv')
    except:
        return False

    return True
