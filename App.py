#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser
import shutil

import hashlib
import os
import time
import tornado.web
from tornado.options import define, options

from face import Faceswapper
from utils import ImgUtil

conf = configparser.ConfigParser()
conf.read('config.ini')

define("port", default=5000, help="run on the given port ", type=int)
define("log_path", default=conf.get("file_path", "log_path"), help="log path ", type=str)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            result = self.check_signature(signature, timestamp, nonce)
            if result:
                self.write(echostr)
            else:
                self.write("")
        except Exception as e:
            self.write("")

    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正确"""
        token = conf.get("wei_xin", "token")
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        return sha1 == signature
class FaceswapperHandler1(tornado.web.RequestHandler):
    def post(self):
        try:
            upload_path = conf.get("file_path", "face_upload_temp_path")  # 文件的暂存路径
            file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
            #name = self.get_argument("user")
            face=''
            head = conf.get("file_path", "template_picture_path")+'head.png'
            for meta in file_metas:
                filename = str((int(round(time.time() * 1000))))+'.jpg'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
                face=filepath
            if face !='':
                result_path=conf.get("file_path", "result_picture_path")
                face_result=Faceswapper.Faceswapper().wapper(head, face,result_path)
                if face_result != '':
                    self.write('{"code":"0000","data":"' + str(face_result) + '"}')
                else:
                    self.write('{"code":"9999","data":null}')
            else:
                self.write('{"code":"9999","data":null}')
        except:
            self.write('{"code":"9999","data":null}')
#图片模板换脸
class FaceswapperImgHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            upload_path = conf.get("file_path", "face_upload_temp_path")  # 文件的暂存路径
            file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
            template = self.get_argument("tpl")
            user = self.get_argument("user")
            face=''
            head = conf.get("file_path", "template_picture_path")+template
            for meta in file_metas:
                filename = str((int(round(time.time() * 1000))))
                filepath = os.path.join(upload_path, filename+'.jpg')
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
                face=filepath
            if face !='' and template !=None and template !='':
                result_path = conf.get("file_path", "result_picture_path")
                face_result=Faceswapper.Faceswapper().wapper(head, face,result_path,filename)
                if face_result != '':
                    self.write('{"code":"0000","data":"' + str(face_result) + '"}')
                else:
                    self.write('{"code":"9999","data":null}')
            else:
                self.write('{"code":"9999","data":null}')
        except:
            self.write('{"code":"9999","data":null}')
#视频模板换脸
class FaceswapperVideoHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            upload_path = conf.get("file_path", "face_upload_temp_path")  # 文件的暂存路径
            file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
            template = self.get_argument("tpl")
            user = self.get_argument("user")
            face=''
            head = conf.get("file_path", "template_video_path")+template+"/"
            for meta in file_metas:
                filename = str((int(round(time.time() * 1000))))+'.jpg'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
                face=filepath
            if face !='' and template !=None and template !='':
                image_list = os.listdir(head)
                swapper_result=conf.get("file_path", "result_video_temp_path")+user+"_"+template+"/"
                os.makedirs(swapper_result)
                for image_name in image_list:
                    Faceswapper.Faceswapper().wapper(head+image_name, face,swapper_result,image_name[:-4])
                gif= ImgUtil.ImgUtil().createGif(swapper_result, conf.get("file_path", "result_video_gif_path"))
                shutil.rmtree(swapper_result)
                self.write('{"code":"0000","data":"'+gif+'"}')
            else:
                self.write('{"code":"9999","data":"参数异常"}')
        except Exception as e:
            self.write('{"code":"9999","data":"'+repr(e)+'"}')
class TestHandler(tornado.web.RequestHandler):
    def get(self):
        head = conf.get("file_path", "template_picture_path") + 'head.png'
        face = conf.get("file_path", "face_upload_temp_path")+'1.jpg'
        swapper_result='E:/study/python/resource/images/result/picture/'
        image_name='123'
        face_result = Faceswapper.Faceswapper().wapper(head, face,swapper_result,image_name)
        self.write(face_result)
if __name__ == "__main__":
    # 启动tornado实例
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/auth", MainHandler),
        (r"/faceswapperVideo", FaceswapperVideoHandler),
        (r"/faceswapperImg", FaceswapperImgHandler),
        (r"/test", TestHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()