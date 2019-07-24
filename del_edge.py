import os
import msvcrt
import shutil
import glob
import cv2
import numpy as np
import sys
import io
from matplotlib import pyplot as plt

PIC_PATH = r'.'
THRESH_TOL = 10


def get_8_pt_bgr(img):
    height, width, _ = img.shape
    top_left = img[0][0]
    top_right = img[0][-1]
    bot_left = img[-1][0]
    bot_right = img[-1][-1]
    top_center = img[0][int(width/2)]
    bot_center = img[-1][int(width/2)]
    left_center = img[int(height/2)][0]
    right_center = img[int(height/2)][-1]

    return (top_left, top_right, bot_left, bot_right,
            top_center, bot_center, left_center, right_center)


def similar_color_method(img, pt_brg):
    # print(pt_brg)
    # lower = np.array(pt_brg) - THRESH_TOL
    # upper = np.array(pt_brg) + THRESH_TOL
    # # print(lower)
    # # upper_hsv = np.array([34,255,255])
    # mask = cv2.inRange(img, lower, upper)
    # img_result = cv2.bitwise_not(cv2.bitwise_xor(
    #     cv2.bitwise_and(img, img, mask=mask), img))

    color_3 = cv2.split(img)
    b, g, r = cv2.split(img)
    # print(b)
    # print(b.shape)
    # # print(mask)
    # # print(mask.shape)
    # # print(img.shape)
    # print(b[400][400])
    # b[(b > 170) & (b < 180)] = 255
    # print(b[400][400])
    # # print(b)
    # # print(b.shape)
    # # print(mask)

    for i in range(3):
        var = int(pt_brg[i])
        lower = var-THRESH_TOL if var-THRESH_TOL >= 0 else 0
        upper = var+THRESH_TOL if var+THRESH_TOL <= 255 else 255
        color = color_3[i].copy()
        color[(color >= lower) & (color <= upper)] = 255
        color_3[i] = color
    img_result = cv2.merge([color_3[0], color_3[1], color_3[2]])
    print(img[0][0])
    print(img_result[0][0])

    return img_result


def merge_thresh_rgb(img, pt_bgr):
    img_b = img.copy()
    img_b[:, :, 1] = 0
    img_b[:, :, 2] = 0

    img_g = img.copy()
    img_g[:, :, 0] = 0
    img_g[:, :, 2] = 0

    img_r = img.copy()
    img_r[:, :, 0] = 0
    img_r[:, :, 1] = 0

    img_3_color = [img_b, img_g, img_r]

    img_result = img.copy()
    img_result[:, :, :] = 0

    for i in range(3):
        _, th0 = cv2.threshold(
            img_3_color[i], pt_bgr[i], 255, cv2.THRESH_BINARY)
        img_result = cv2.bitwise_or(img_result, th0)
        # _, th1 = cv2.threshold(
        #     img_3_color[i], pt_bgr[i] + THRESH_TOL, 255, cv2.THRESH_BINARY)
        # img_result = cv2.bitwise_or(img_result, th1)

    return img_result


def do_a_pic(file):
    # img = cv2.imread(file)
    img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), -1)
    print('imgsize: ', img.shape)
    # jpg_file = os.path.splitext(file)[0]+'_tojpg.jpg'
    # cv2.imwrite(jpg_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    # # cv2.imencode('.jpg', img)[1].tofile(jpg_file)
    # print('%s -> %s' % (file, jpg_file))

    pt8_bgr = get_8_pt_bgr(img)

    # img_result0 = img.copy()
    # img_result0[:, :, :] = 0

    # for pt_bgr in pt8_bgr:
    #     img_result0 = cv2.bitwise_or(
    #         img_result0, merge_thresh_rgb(img, pt_bgr))

    img_result2 = img.copy()
    img_result2[:, :, :] = 0

    for pt_bgr in pt8_bgr:
        img_result2 = cv2.bitwise_or(
            img_result2, similar_color_method(img, pt_bgr))

    # img_result1 = cv2.bitwise_or(img_result0, img)

    # res0 = merge_thresh_rgb(img, pt8_bgr[0])
    # res1 = merge_thresh_rgb(img, pt8_bgr[1])
    # res2 = merge_thresh_rgb(img, pt8_bgr[2])
    # res3 = merge_thresh_rgb(img, pt8_bgr[3])
    # res4 = merge_thresh_rgb(img, pt8_bgr[4])
    # res5 = merge_thresh_rgb(img, pt8_bgr[5])
    # res6 = merge_thresh_rgb(img, pt8_bgr[6])
    # res7 = merge_thresh_rgb(img, pt8_bgr[7])

    res0 = similar_color_method(img, pt8_bgr[0])
    res1 = similar_color_method(img, pt8_bgr[1])
    res2 = similar_color_method(img, pt8_bgr[2])
    res3 = similar_color_method(img, pt8_bgr[3])
    res4 = similar_color_method(img, pt8_bgr[4])
    res5 = similar_color_method(img, pt8_bgr[5])
    res6 = similar_color_method(img, pt8_bgr[6])
    res7 = similar_color_method(img, pt8_bgr[7])

    cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('image', img_result2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # images = [img, img_result0, img_result1, img_result2]
    images = [res0, res4, res2, res6, img_result2, res7, res2, res5, res3]
    for i in range(9):
        img1 = images[i]
        b, g, r = cv2.split(img1)
        img2 = cv2.merge([r, g, b])
        plt.subplot(3, 3, i+1), plt.imshow(img2)
        plt.xticks([]), plt.yticks([])

    plt.show()


def main():
    # sys.stdout = io.TextIOWrapper(
    #     sys.stdout.buffer, encoding='gb18030', line_buffering=True)

    files = glob.glob(PIC_PATH + '\\*.jpg')
    for f in files:
        print(f)
        do_a_pic(f)


if __name__ == '__main__':
    main()
