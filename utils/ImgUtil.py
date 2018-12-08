#!/usr/bin/python
#coding=utf-8
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os,imageio,time
import configparser
conf = configparser.ConfigParser()
conf.read('config.ini')
class ImgUtil:
    """
    source 图片路径
    result 图片保存路径
    size 字体大小
    x 字体的x起始位置
    y 字体的y起始位置
    txt 添加的文字
    color 字体的颜色 (255,255,255)
    """
    def addFont(self,source,result,size,x,y,txt,color):
        # 添加水印
        # 设置所使用的字体 C:\Windows\Fonts
        font = ImageFont.truetype(conf.get("file_path", "font_path"), size)
        # 画图51270088
        font_img = Image.open(source)
        draw = ImageDraw.Draw(font_img)
        x=font_img.width-x
        y = font_img.height - y
        draw.text((x, y), u""+txt+"", color, font=font)  # 设置文字位置/内容/颜色(255,255,255)/字体
        font_img.save(result)
    #创建GIF
    def createGif( self,imgdir,save_path):
        image_list=os.listdir(imgdir)
        frames = []
        for image_name in image_list:
            frames.append(imageio.imread(imgdir+image_name))
        filename = save_path+"/"+str((int(round(time.time() * 1000))))+".gif"
        imageio.mimsave(filename, frames, 'GIF', duration=0.4)
        return filename