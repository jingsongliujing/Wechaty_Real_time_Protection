#app.py

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, Response

# 导入 camera
from camera import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """视频流主页"""
    return render_template('index.html')


def gen(camera):
    """视频流生成函数"""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """视频流路由(route).放到 img 标签的 src 属性."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='2409:8a6c:51c:a540:acca:734a:6030', debug=True, threaded=True)  #默认是0.0.0.0，改成ipv6地址就可以远程访问，不用局限于家庭内网了
