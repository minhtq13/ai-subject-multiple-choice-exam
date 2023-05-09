import os
import gc
import cv2
import numpy as np
import math
import torch
import torch.nn as nn
import torchvision.transforms as torchvision_T
from torchvision.models.segmentation import deeplabv3_resnet50
from torchvision.models.segmentation import deeplabv3_mobilenet_v3_large
import imutils
from math import ceil
from collections import defaultdict
from ultralytics import YOLO


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    pts = np.array(pts)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect.astype("int").tolist()


def find_dest(pts):
    (tl, tr, br, bl) = pts
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    destination_corners = [[0, 0], [maxWidth, 0],
                           [maxWidth, maxHeight], [0, maxHeight]]
    return order_points(destination_corners)


def image_preproces_transforms(
    mean=(0.4611, 0.4359, 0.3905), std=(0.2193, 0.2150, 0.2109)
):
    common_transforms = torchvision_T.Compose(
        [torchvision_T.ToTensor(), torchvision_T.Normalize(mean, std), ]
    )

    return common_transforms


def load_model(num_classes=1, model_name="mbv3", checkpoint_path=None, device=None):

    if model_name == "mbv3":
        model = deeplabv3_mobilenet_v3_large(num_classes=num_classes)

    else:
        model = deeplabv3_resnet50(num_classes=num_classes)

    model.to(device)
    checkpoints = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoints, strict=False)
    model.eval()

    _ = model(torch.randn((2, 3, 384, 384)))

    return model


CHECKPOINT_MODEL_PATH = r"Data/Model/model_mbv3_iou_mix_2C049.pth"

trained_model = load_model(num_classes=2, model_name="mbv3",
                           checkpoint_path=CHECKPOINT_MODEL_PATH, device=device)
preprocess_transforms = image_preproces_transforms()


def extract(image_true=None, trained_model=None, image_size=384, BUFFER=10):
    global preprocess_transforms

    IMAGE_SIZE = image_size
    half = IMAGE_SIZE // 2

    imH, imW, C = image_true.shape

    image_model = cv2.resize(
        image_true, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_NEAREST)

    scale_x = imW / IMAGE_SIZE
    scale_y = imH / IMAGE_SIZE

    image_model = preprocess_transforms(image_model)
    image_model = torch.unsqueeze(image_model, dim=0)

    with torch.no_grad():
        out = trained_model(image_model)["out"].cpu()

    del image_model
    gc.collect()

    out = torch.argmax(out, dim=1, keepdims=True).permute(
        0, 2, 3, 1)[0].numpy().squeeze().astype(np.int32)
    r_H, r_W = out.shape

    _out_extended = np.zeros(
        (IMAGE_SIZE + r_H, IMAGE_SIZE + r_W), dtype=out.dtype)
    _out_extended[half: half + IMAGE_SIZE, half: half + IMAGE_SIZE] = out * 255
    out = _out_extended.copy()

    del _out_extended
    gc.collect()

    canny = cv2.Canny(out.astype(np.uint8), 225, 255)
    canny = cv2.dilate(canny, cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (5, 5)))
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    page = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    epsilon = 0.02 * cv2.arcLength(page, True)
    corners = cv2.approxPolyDP(page, epsilon, True)

    corners = np.concatenate(corners).astype(np.float32)

    corners[:, 0] -= half
    corners[:, 1] -= half

    corners[:, 0] *= scale_x
    corners[:, 1] *= scale_y

    if not (np.all(corners.min(axis=0) >= (0, 0)) and np.all(corners.max(axis=0) <= (imW, imH))):

        left_pad, top_pad, right_pad, bottom_pad = 0, 0, 0, 0

        rect = cv2.minAreaRect(corners.reshape((-1, 1, 2)))
        box = cv2.boxPoints(rect)
        box_corners = np.int32(box)

        box_x_min = np.min(box_corners[:, 0])
        box_x_max = np.max(box_corners[:, 0])
        box_y_min = np.min(box_corners[:, 1])
        box_y_max = np.max(box_corners[:, 1])

        if box_x_min <= 0:
            left_pad = abs(box_x_min) + BUFFER

        if box_x_max >= imW:
            right_pad = (box_x_max - imW) + BUFFER

        if box_y_min <= 0:
            top_pad = abs(box_y_min) + BUFFER

        if box_y_max >= imH:
            bottom_pad = (box_y_max - imH) + BUFFER

        image_extended = np.zeros(
            (top_pad + bottom_pad + imH, left_pad + right_pad + imW, C), dtype=image_true.dtype)
        image_extended[top_pad: top_pad + imH,
                       left_pad: left_pad + imW, :] = image_true
        image_extended = image_extended.astype(np.float32)

        box_corners[:, 0] += left_pad
        box_corners[:, 1] += top_pad

        corners = box_corners
        image_true = image_extended

    corners = sorted(corners.tolist())
    corners = order_points(corners)
    destination_corners = find_dest(corners)
    M = cv2.getPerspectiveTransform(np.float32(
        corners), np.float32(destination_corners))

    final = cv2.warpPerspective(
        image_true, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv2.INTER_LANCZOS4)
    final = np.clip(final, a_min=0., a_max=255.)

    return final


def get_x(s):
    return s[1][0]


def get_y(s):
    return s[1][1]


def get_h(s):
    return s[1][3]


def get_x_ver1(s):
    s = cv2.boundingRect(s)
    return s[0] * s[1]


def crop_image(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (9, 9), 0)
    img_canny = cv2.Canny(blurred, 0, 20)
    cnts = cv2.findContours(
        img_canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    ans_blocks = []
    x_old, y_old, w_old, h_old = 0, 0, 0, 0

    if len(cnts) > 0:
        cnts = sorted(cnts, key=get_x_ver1)

        for i, c in enumerate(cnts):
            x_curr, y_curr, w_curr, h_curr = cv2.boundingRect(c)
            if w_curr * h_curr > 170000 and w_curr * h_curr < 250000:
                check_xy_min = x_curr * y_curr - x_old * y_old
                check_xy_max = (x_curr + w_curr) * (y_curr +
                                                    h_curr) - (x_old + w_old) * (y_old + h_old)

                if len(ans_blocks) == 0:
                    ans_blocks.append(
                        (gray_img[y_curr:y_curr + h_curr, x_curr:x_curr + w_curr], [x_curr, y_curr, w_curr, h_curr]))
                    x_old = x_curr
                    y_old = y_curr
                    w_old = w_curr
                    h_old = h_curr
                elif check_xy_min > 20000 and check_xy_max > 20000:
                    ans_blocks.append(
                        (gray_img[y_curr:y_curr + h_curr, x_curr:x_curr + w_curr], [x_curr, y_curr, w_curr, h_curr]))
                    x_old = x_curr
                    y_old = y_curr
                    w_old = w_curr
                    h_old = h_curr

        sorted_ans_blocks = sorted(ans_blocks, key=get_x)

        return sorted_ans_blocks


def process_ans_blocks(ans_blocks):
    list_answers = []
    for ans_block in ans_blocks:
        ans_block_img = np.array(ans_block[0])
        offset1 = ceil(ans_block_img.shape[0] / 6)
        for i in range(6):
            box_img = np.array(ans_block_img[i * offset1:(i + 1) * offset1, :])
            height_box = box_img.shape[0]
            box_img = box_img[14:height_box - 14, :]
            offset2 = ceil(box_img.shape[0] / 5)
            for j in range(5):
                list_answers.append(box_img[j * offset2:(j + 1) * offset2, :])

    return list_answers


def predictAns(img, model, index):
    choice = ''
    imProcess = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w, _ = imProcess.shape
    results = model.predict(imProcess)
    data = results[0].boxes.data
    for i, data in enumerate(data):
        x1 = int(data[0])
        y1 = int(data[1])
        x2 = int(data[2])
        y2 = int(data[3])
        confi = float(data[4])
        class1 = int(data[5])
        if class1 == 0 and confi > 0.8:
            choice = get_choice(iw=w, ix=x1)
            continue

    return choice


def get_choice(iw, ix):
    newIw = iw - 9
    choiceA = (ix - 30) / newIw
    choiceB = (ix - 25) / newIw
    choiceC = (ix - 15) / newIw
    choiceD = (ix - 5) / newIw
    if choiceA <= 0.25:
        choice = "A"
    elif 0.25 < choiceB <= 0.5:
        choice = "B"
    elif 0.5 < choiceC <= 0.75:
        choice = "C"
    elif 0.75 < choiceD <= 1:
        choice = "D"
    else:
        choice = ""
    return choice


def get_answer(img, number_answer):
    list_ans_boxes = crop_image(cv2.convertScaleAbs(img * 255))
    list_ans = process_ans_blocks(list_ans_boxes)
    pWeight = 'Data/Model/best.pt'
    model = YOLO(pWeight)
    # Get result
    dict_results = {}
    for i, answer in enumerate(list_ans):
        selected_answer = predictAns(img=answer, model=model, index=i)
        dict_results[f'{i+1}'] = selected_answer
        if i == (number_answer - 1):
            break
    return dict_results


def crop_image_1(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (9, 9), 0)
    img_canny = cv2.Canny(blurred, 0, 20)
    cnts = cv2.findContours(
        img_canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    ans_blocks = []
    x_old, y_old, w_old, h_old = 0, 0, 0, 0
    if len(cnts) > 0:
        cnts = sorted(cnts, key=get_x_ver1)
        for i, c in enumerate(cnts):
            x_curr, y_curr, w_curr, h_curr = cv2.boundingRect(c)
            if 35000 < w_curr * h_curr < 45000 or 17500 < w_curr * h_curr < 25000 and h_curr > 200:
                check_xy_min = x_curr * y_curr - x_old * y_old
                check_xy_max = (x_curr + w_curr) * (y_curr +
                                                    h_curr) - (x_old + w_old) * (y_old + h_old)
                if len(ans_blocks) == 0:
                    ans_blocks.append(
                        (gray_img[y_curr:y_curr + h_curr, x_curr:x_curr + w_curr], [x_curr, y_curr, w_curr, h_curr]))
                    x_old = x_curr
                    y_old = y_curr
                    w_old = w_curr
                    h_old = h_curr
                elif check_xy_min > 2000 and check_xy_max > 2000:
                    ans_blocks.append(
                        (gray_img[y_curr:y_curr + h_curr, x_curr:x_curr + w_curr], [x_curr, y_curr, w_curr, h_curr]))
                    x_old = x_curr
                    y_old = y_curr
                    w_old = w_curr
                    h_old = h_curr

        sorted_ans_blocks = sorted(ans_blocks, key=get_x)
        return sorted_ans_blocks


def process_info_blocks(ans_blocks):
    list_info_cropped = []
    for info_block in ans_blocks:

        info_block_img = np.array(info_block[0])
        wh_block = info_block_img.shape[1]
        if wh_block > 100:
            offset1 = math.floor(wh_block // 6)
            for i in range(6):
                box_img = np.array(
                    info_block_img[:, i * offset1:(i + 1) * offset1])
                list_info_cropped.append(box_img)
        else:
            offset1 = math.floor(wh_block // 3)
            for i in range(3):
                box_img = np.array(
                    info_block_img[:, i * offset1:(i + 1) * offset1])
                list_info_cropped.append(box_img)
    return list_info_cropped


def predictInfo(img, model, index):
    choice = ''
    imProcess = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w, _ = imProcess.shape
    results = model.predict(imProcess)
    data = results[0].boxes.data

    for i, data in enumerate(data):
        x1 = int(data[0])
        y1 = int(data[1])
        x2 = int(data[2])
        y2 = int(data[3])
        class1 = int(data[5])

        if class1 == 0:
            choice = get_choose(ix=y1)
    return choice


def get_choose(ix):
    if ix <= 15:
        choose = "0"
    elif 30 < ix <= 50:
        choose = "1"
    elif 60 < ix <= 80:
        choose = "2"
    elif 90 < ix <= 110:
        choose = "3"
    elif 120 < ix <= 140:
        choose = "4"
    elif 150 < ix <= 170:
        choose = "5"
    elif 180 < ix <= 200:
        choose = "6"
    elif 210 < ix <= 230:
        choose = "7"
    elif 240 < ix <= 260:
        choose = "8"
    else:
        choose = "9"
    return choose


def get_info(img):

    left = 700
    top = 0
    right = 1056
    bottom = 500
    cropped_image = img[top:bottom, left:right]
    box_info = crop_image_1(cv2.convertScaleAbs(cropped_image * 255))
    list_info_cropped = process_info_blocks(box_info)
    pWeight = './Data/Model/info.pt'
    model = YOLO(pWeight)
    dict_results = {}
    for index, info in enumerate(list_info_cropped):
        selected_info = predictInfo(
            img=info, model=model, index=index)

        dict_results[f'{index+1}'] = selected_info
    mssv = ''.join(list(dict_results.values())[:6])
    madethi = ''.join(list(dict_results.values())[-3:])
    result_info = {}
    result_info["SBD"] = mssv
    result_info["MDT"] = madethi
    return result_info


if __name__ == '__main__':
    image = cv2.imread('./Data/Test/f13.jpg',
                       cv2.IMREAD_COLOR)[:, :, ::-1]
    document = extract(image_true=image, trained_model=trained_model)
    document = document / 255.0
    img = cv2.resize(document, (1056, 1500), interpolation=cv2.INTER_AREA)
    number_answer = 120
    result_answer = get_answer(img, number_answer)
    result_info = get_info(img)
    print(result_answer)
    print("Số báo danh: " + result_info["SBD"])
    print("Mã đề thi: " + result_info["MDT"])
