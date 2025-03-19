
import cv2
import tensorflow as tf
import time
import numpy as np
from teachable_machine_eval import load_model
from draw_chinese_text import put_chinese_text


def classify_image(classifier, cv2_image):

    # Convert BGR to RGB (opencv default color channel == BGR )
    # We need RGB for TM model input
    RGB_img = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # RGB_img = cv2_image

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(RGB_img, (224, 224), interpolation=cv2.INTER_LANCZOS4)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = classifier(image)  # Input 需要是 sRGB format, 為TM的輸入
    # prediction = model.predict(image)
    index = np.argmax(prediction)  # 最高分的label的編號
    class_name = class_names[index]  # label編號的對應名稱
    confidence_score = prediction[0][index]  # label編號對應的分數

    # Print prediction and confidence score
    top_one = class_name[2:].strip()  # 預測的種類名稱
    top_one_score = np.round(confidence_score * 100)  # 預測的分數

    return top_one, top_one_score


if __name__ == '__main__':
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    # model = load_model("keras_model.h5", compile=False)
    MODEL_PATH = "models/pue_tm_enhance_flip_model/with_dot_50"
    LABEL_PATH = "models/pue_tm_enhance_flip_model/labels.txt"
    model = load_model(MODEL_PATH)

    # Load the labels
    class_names = open(LABEL_PATH, "r", encoding="utf8").readlines()

    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    while True:
        start_time = time.time_ns()

        # Grab the webcamera's image.
        ret, raw_image = camera.read()
        if ret:
            top_one, top_one_score = classify_image(model, raw_image.copy())

            # Show the image in a window, and put some text
            if top_one_score >= 80:
                text_to_put = f'{top_one}: {top_one_score}%'
            else:
                text_to_put = "Recognizing...."

            drawed_image = put_chinese_text(raw_image, text_to_put)
            cv2.imshow("Webcam Image", drawed_image)

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

        period_time_in_ms = (time.time_ns() - start_time)/(10**6)
        print("Check time: ", period_time_in_ms)

    camera.release()
    cv2.destroyAllWindows()
