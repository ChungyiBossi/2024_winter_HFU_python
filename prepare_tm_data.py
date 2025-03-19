import os
import cv2
import numpy as np


def list_all_files(folder):
    file_list = []
    for root, _, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def enhance_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)  # 轉換為 LAB 色彩空間
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)  # 只對亮度通道應用對比增強
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)  # 轉回 RGB


def adjust_gamma(image, gamma=1.2):
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma *
                     255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)


def enhance_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_files = list_all_files(input_folder)

    for img_path in all_files:
        img = cv2.imread(img_path)
        if img is None:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enhanced_img = enhance_contrast(img)
        enhanced_img = adjust_gamma(enhanced_img)
        enhanced_img = cv2.GaussianBlur(enhanced_img, (5, 5), 0)

        relative_path = os.path.relpath(img_path, input_folder)
        output_path = os.path.join(output_folder, relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, cv2.cvtColor(enhanced_img, cv2.COLOR_RGB2BGR))

    print(f"Enhanced images saved to: {output_folder}")


def generate_flip_img(input_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    all_files = list_all_files(input_folder)
    # 讀取資料夾內所有圖片
    for filename in all_files:
        print(filename)
        # 確保是圖片檔案
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # 讀取圖片
        img = cv2.imread(filename)

        # 進行上下左右翻轉
        flip_horizontal = cv2.flip(img, 1)  # 左右翻轉
        flip_vertical = cv2.flip(img, 0)  # 上下翻轉
        flip_both = cv2.flip(img, -1)  # 同時左右 + 上下翻轉

        # 取得圖片名稱（不含副檔名）
        img_name, ext = os.path.splitext(filename)

        # 儲存增強圖片
        cv2.imwrite(f'{img_name}_flip_h{ext}', flip_horizontal)
        cv2.imwrite(f'{img_name}_flip_v{ext}', flip_vertical)
        cv2.imwrite(f'{img_name}_flip_both{ext}', flip_both)

    print(f"已完成翻轉並儲存所有圖片至 {output_folder}/")


if __name__ == '__main__':
    # 原始圖片資料夾，需要把train/test的各類別資料都做預處理
    INPUT_FOLDER = 'datasets/pue_with_dot_dataset/train'
    OUTPUT_FOLDER = 'datasets/pue_with_dot_dataset/enhance/train'  # 預處理後的輸出資料夾
    enhance_images_in_folder(INPUT_FOLDER, OUTPUT_FOLDER)  # 光度與對比預處理
    generate_flip_img(OUTPUT_FOLDER, OUTPUT_FOLDER)  # 增加翻轉圖片
