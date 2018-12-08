#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser

import cv2
import dlib
import numpy

from utils import ImgUtil

conf = configparser.ConfigParser()
conf.read('config.ini')

class TooManyFaces(Exception):
    # 定位到太多脸
    pass


class NoFaces(Exception):
    # 没脸
    pass


class Faceswapper():
    def __init__(self):
        self.PREDICTOR_PATH = conf.get("file_path", "face_dat_file_path")
        self.SCALE_FACTOR = 1
        self.FEATHER_AMOUNT = 11
        # 五官等标记点
        self.FACE_POINTS = list(range(17, 68))
        self.MOUTH_POINTS = list(range(48, 61))
        self.RIGHT_BROW_POINTS = list(range(17, 22))
        self.LEFT_BROW_POINTS = list(range(22, 27))
        self.RIGHT_EYE_POINTS = list(range(36, 42))
        self.LEFT_EYE_POINTS = list(range(42, 48))
        self.NOSE_POINTS = list(range(27, 35))
        self.JAW_POINTS = list(range(0, 17))

        # 人脸的完整标记点
        self.ALIGN_POINTS = (self.LEFT_BROW_POINTS + self.RIGHT_EYE_POINTS + self.LEFT_EYE_POINTS +
                        self.RIGHT_BROW_POINTS + self.NOSE_POINTS + self.MOUTH_POINTS)

        # 来自第二张图（脸）的标记点，眼、眉、鼻子、嘴，这一部分标记点将覆盖第一张图的对应标记点
        self.OVERLAY_POINTS = [
            self.LEFT_EYE_POINTS + self.RIGHT_EYE_POINTS + self.LEFT_BROW_POINTS + self.RIGHT_BROW_POINTS,
            self.NOSE_POINTS + self.MOUTH_POINTS,
        ]

        # 颜色校正参数
        self.COLOUR_CORRECT_BLUR_FRAC = 0.6
        # 特征提取器（predictor）
        self.detector = dlib.get_frontal_face_detector()
        # 人脸检测器（detector）
        self.predictor = dlib.shape_predictor(self.PREDICTOR_PATH)

    # get_landmarks()函数将一个图像转化成numpy数组，并返回一个68 x2元素矩阵，输入图像的每个特征点对应每行的一个x，y坐标。

    # 特征提取器（predictor）要一个粗糙的边界框作为算法输入，由传统的能返回一个矩形列表的人脸检测器（detector）提供，其每个矩形列表在图像中对应一个脸。
    def get_landmarks(self, im):
        rects = self.detector(im, 1)

        if len(rects) > 1:
            raise TooManyFaces('Too Many Faces')
        if len(rects) == 0:
            raise NoFaces('No Faces')

        return numpy.matrix([[p.x, p.y] for p in self.predictor(im, rects[0]).parts()])

    def annotate_landmarks(self, im, landmarks):
        im = im.copy()
        for idx, point in enumerate(landmarks):
            pos = (point[0, 0], point[0, 1])
            cv2.putText(im, str(idx), pos,
                        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                        fontScale=0.4,
                        color=(0, 0, 255))
            cv2.circle(im, pos, 3, color=(0, 255, 255))
        return im

    def draw_convex_hull(self, im, points, color):
        points = cv2.convexHull(points)
        cv2.fillConvexPoly(im, points, color=color)

    def get_face_mask(self, im, landmarks):
        im = numpy.zeros(im.shape[:2], dtype=numpy.float64)

        for group in self.OVERLAY_POINTS:
            self.draw_convex_hull(im,
                                  landmarks[group],
                                  color=1)

        im = numpy.array([im, im, im]).transpose((1, 2, 0))

        im = (cv2.GaussianBlur(im, (self.FEATHER_AMOUNT, self.FEATHER_AMOUNT), 0) > 0) * 1.0
        im = cv2.GaussianBlur(im, (self.FEATHER_AMOUNT, self.FEATHER_AMOUNT), 0)

        return im

    def transformation_from_points(self, points1, points2):
        """
        现在我们已经有了两个标记矩阵，每行有一组坐标对应一个特定的面部特征（如第30行给出的鼻子的坐标）。
        我们现在要搞清楚如何旋转、翻译和规模化第一个向量，使它们尽可能适合第二个向量的点。
        想法是，可以用相同的变换在第一个图像上覆盖第二个图像。
        把它们更数学化，寻找T，s和R，令下面这个表达式的结果最小：
        图片描述
        R是个2 x2正交矩阵，s是标量，T是二维向量，pi和qi是上面标记矩阵的行。
        事实证明，这类问题可以用“常规普氏分析法” (Ordinary Procrustes Analysis) 解决
        """

        # 将输入矩阵转换为浮点数。这是之后步骤的必要条件。
        points1 = points1.astype(numpy.float64)
        points2 = points2.astype(numpy.float64)
        # 每一个点集减去它的矩心。一旦为这两个新的点集找到了一个最佳的缩放和旋转方法，
        # 这两个矩心c1和c2就可以用来找到完整的解决方案
        c1 = numpy.mean(points1, axis=0)
        c2 = numpy.mean(points2, axis=0)
        points1 -= c1
        points2 -= c2

        s1 = numpy.std(points1)
        s2 = numpy.std(points2)
        # 同样，每一个点集除以它的标准偏差。这消除了问题的组件缩放偏差
        points1 /= s1
        points2 /= s2
        # 使用Singular Value Decomposition计算旋转部分。
        # 可以在维基百科上看到关于解决正交普氏问题的细节（https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem）
        U, S, Vt = numpy.linalg.svd(points1.T * points2)
        R = (U * Vt).T
        # 利用仿射变换矩阵（https://en.wikipedia.org/wiki/Transformation_matrix#Affine_transformations）
        # 返回完整的转化。
        return numpy.vstack([numpy.hstack(((s2 / s1) * R,
                                           c2.T - (s2 / s1) * R * c1.T)),
                             numpy.matrix([0., 0., 1.])])

    def read_im_and_landmarks(self, fname):
        im = cv2.imread(fname, cv2.IMREAD_COLOR)
        im = cv2.resize(im, (im.shape[1] * self.SCALE_FACTOR, im.shape[0] * self.SCALE_FACTOR))
        # get_landmarks()函数将一个图像转化成numpy数组，并返回一个68 x2元素矩阵，输入图像的每个特征点对应每行的一个x，y坐标
        s = self.get_landmarks(im)
        return im, s

    # 可以插入OpenCV的cv2.warpAffine函数，将图像二映射到图像一
    def warp_im(self, im, M, dshape):
        output_im = numpy.zeros(dshape, dtype=im.dtype)
        cv2.warpAffine(im,
                       M[:2],
                       (dshape[1], dshape[0]),
                       dst=output_im,
                       borderMode=cv2.BORDER_TRANSPARENT,
                       flags=cv2.WARP_INVERSE_MAP)
        return output_im

    def correct_colours(self, im1, im2, landmarks1):
        blur_amount = self.COLOUR_CORRECT_BLUR_FRAC * numpy.linalg.norm(
            numpy.mean(landmarks1[self.LEFT_EYE_POINTS], axis=0) -
            numpy.mean(landmarks1[self.RIGHT_EYE_POINTS], axis=0))
        blur_amount = int(blur_amount)
        if blur_amount % 2 == 0:
            blur_amount += 1
        im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
        im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

        # Avoid divide-by-zero errors.
        im2_blur += (128 * (im2_blur <= 1.0)).astype(im2_blur.dtype)

        return (im2.astype(numpy.float64) * im1_blur.astype(numpy.float64) /
                im2_blur.astype(numpy.float64))

    def wapper(self,head,face,result_path,image_name):
        try:
            # 1．使用dlib提取面部标记
            im1, landmarks1 = self.read_im_and_landmarks(head)
            im2, landmarks2 = self.read_im_and_landmarks(face)
            # 用普氏分析(Procrustes analysis)调整脸部
            M = self.transformation_from_points(landmarks1[self.ALIGN_POINTS],
                                                landmarks2[self.ALIGN_POINTS])
            # 把第二张图像的特性混合在第一张图像中
            mask = self.get_face_mask(im2, landmarks2)
            # 插入OpenCV的cv2.warpAffine函数，将图像二映射到图像一
            warped_mask = self.warp_im(mask, M, im1.shape)
            combined_mask = numpy.max([self.get_face_mask(im1, landmarks1), warped_mask],
                                      axis=0)

            warped_im2 = self.warp_im(im2, M, im1.shape)
            # 校正第二张图像的颜色
            warped_corrected_im2 = self.correct_colours(im1, warped_im2, landmarks1)

            output_im = im1 * (1.0 - combined_mask) + warped_corrected_im2 * combined_mask
            fileName=image_name+'.png'
            face_result= result_path+fileName
            cv2.imwrite(face_result, output_im)
            # 添加水印
            ImgUtil.ImgUtil().addFont(face_result, face_result, 25, 55, 30, '颜智', (255, 255, 255))
            return fileName
        except Exception as e:
            print(e)
            return ''


#if __name__ == '__main__':
    #Faceswapper().wapper()
