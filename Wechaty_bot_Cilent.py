# 导入第三方库
import os
from wechaty import (
    Contact,
    FileBox,
    Message,
    ScanStatus,
    Wechaty,
    Friendship,
    FriendshipType
)
import asyncio
from config import config_list
import config
from typing import Optional
import paddlehub as hub
import json, requests
import hashlib
import time
import random
import string
from urllib.parse import quote

import cv2
import uuid

# Paddlehub文本模型
text_model1 = hub.Module(name='ernie_gen_lover_words')     # 情话模型
text_model2 = hub.Module(name="ernie_gen_acrostic_poetry", line=4, word=7)   # 藏头诗模型



import requests
import json


def getScore(username, password):
    data = {'username': username, 'password': password, 'year': 2020, 'term': 12}
    url = "https://py.lqb666.cn/grade"
    res = requests.post(url, data)
    res = res.text
    res = json.loads(res)
    list_score=[]
    if(res['success'] == True):
        for item in res['grades']:
            chengji="课程名称："+item['kcmc']+" 成绩："+item['cj']
            list_score.append(chengji)
        list_score_s=str(list_score).replace('[','').replace(',',', \n').replace(']','')
        return list_score_s
    else:
        return res['message']



def getclass(username, password):
    data = {'username': username, 'password': password, 'year': 2020, 'term': 12}
    url = "https://py.lqb666.cn/curriculum"
    res = requests.post(url, data)
    res = res.text
    res = json.loads(res)
    list_class=[]
    if(res['success'] == True):
        for item in res['course']:

            kecheng="课程名称："+item['kcmc']+" 地点："+item['cdmc']+" 节数："+item['jc']+" 星期："+item['xqjmc']+" 周数："+item['zcd']
            list_class.append(kecheng)
        return list_class
            #print("课程名称："+item['kcmc']+" 地点："+item['cdmc']+" 节数："+item['jc']+" 星期："+item['xqjmc']+" 周数："+item['zcd'])
    else:
        return res['message']
        # print(res['message'])




def test_download():
    cap = cv2.VideoCapture("http://[2409:8a6c:51c:a540:acca:734a:6030:77b4]:5000/video_feed")
    # cap = cv2.VideoCapture("rtsp://admin:12345@192.168.1.64/main/Channels/1")
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_s = cap.get(5)
    print(frame_s)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    ret, frame = cap.read()
    time_frame = frame_s*3*1#设置保存时间为20秒一保存
    num = 0
    while ret:
        if num == 0:
            filename = str(uuid.uuid4())+".mp4"
            video_writer = cv2.VideoWriter(filename, fourcc, frame_s, size, True)  # 参数：视频文件名，格式，每秒帧数，宽高，是否灰度
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        img = cv2.resize(frame,(640,360),interpolation=cv2.INTER_LINEAR)
        video_writer.write(frame)
        num  = num+1
        if num == time_frame :
            video_writer.release()
            num = 0
            break
    # video_writer.release()
    cv2.destroyAllWindows()
    cap.release()






    


# 获取城市天气
def get_weather_data(city_name):
    weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city={}".format(city_name)  # 将链接定义为一个字符串
    response = requests.get(weatherJsonUrl)  # 获取并下载页面，其内容会保存在respons.text成员变量里面
    response.raise_for_status()  # 这句代码的意思如果请求失败的话就会抛出异常，请求正常就上面也不会做
    # 将json文件格式导入成python的格式
    weather_dict = json.loads(response.text)
    # print(weather_dict)
    if weather_dict['desc'] == 'invilad-citykey':
        weather_info = '请输入正确的城市名!'
    else:
        forecast = weather_dict.get('data').get('forecast')
        city = '城市：' + weather_dict.get('data').get('city') + '\n'
        date = '日期：' + forecast[0].get('date') + '\n'
        type = '天气：' + forecast[0].get('type') + '\n'
        wendu = '温度：' + weather_dict.get('data').get('wendu') + '℃ ' + '\n'
        high = '高温：' + forecast[0].get('high') + '\n'
        low = '低温：' + forecast[0].get('low') + '\n'
        ganmao = '感冒提示：' + weather_dict.get('data').get('ganmao') + '\n'
        fengxiang = '风向：' + forecast[0].get('fengxiang')
        weather_info = city + date + type + wendu + high + low + ganmao + fengxiang
    return weather_info


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


def get_params(plus_item):
    global params
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key
    # 注册地址：https://ai.qq.com/product/nlpchat.shtml
    app_id = '2171755636'    # your appid
    app_key = 'HYFEyQEF5U3Zkbjo'   # your app_key
    params = {'app_id': app_id,
              'question': plus_item,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'session': '10000'
              }
    sign_before = ''
    # 要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params

def get_content(plus_item):
    global payload, r
    # 聊天的API地址
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数
    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item)
    r = requests.post(url, data=payload)
    res = r.json()["data"]["answer"]
    if len(res) == 0:
        res = '请换个问题!'
    return res


# 文本消息处理--机器对话
def chat_bot(content, mode):
    res = ''
    if mode == '0':
        res = get_content(content)
        # print(res)
    elif mode == '1':
        res = text_model1.generate(texts=[content], use_gpu=False, beam_width=1)
        if res is None:
            return
        res = res[0][0]
        # print(res)
    elif mode == '2':
        res = text_model2.generate(texts=[content], use_gpu=False, beam_width=1)
        if res is None:
            return
        res = res[0][0]
    return res

# debug时分割线
def dividing_line(info='分割线'):
    print('-' * 30 + info + '-' * 30)


# 发送文本消息给联系人
async def sendTextMsgToContact(contact, text):
    if not contact:  # 好友不存在直接返回
        return
    await contact.say(text)  # 调用contact对象的say方法发送消息，contact对象很多方法，参考官方文档


# 发送媒体消息给联系人
async def sendMediaMsgToContact(contact, fileUrl, filePath):
    # print(contact)
    if not contact:  # 好友不存在直接返回
        return
    if fileUrl:
        fileBox1 = FileBox.from_url(url=fileUrl, name='wxapplet.png')
        await contact.say(fileBox1)
    if filePath:
        fileBox2 = FileBox.from_file(filePath)
        await contact.say(fileBox2)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """

    def __init__(self):
        super().__init__()

    async def on_message(self, msg: Message):
        """
        Message Handler for the Bot
        """
        contact = msg.talker()  # 发消息人
        content = msg.text()  # 消息内容
        room = msg.room()  # 是否是群消息
        contact_name = contact.name

        if room:  # 群聊入口，未做任何处理
            dividing_line()
            room_id = room.room_id
            print('群聊')
                
            print('群名:{},发消息人:{},内容:{}'.format(room_id, contact_name, content))
            print('使用API发送群消息')


            if room.room_id == config_list[room_id] and (msg.type() == Message.Type.MESSAGE_TYPE_TEXT):

                
                
                if msg.type() == Message.Type.MESSAGE_TYPE_TEXT:  # 处理文本类型消息
                    if content == 'ding':
                        await sendTextMsgToContact(contact=contact, text="这是自动回复: dong dong dong")

            



                
        else:
            dividing_line()
            print('非群聊')
            if msg.type() == Message.Type.MESSAGE_TYPE_TEXT:  # 处理文本类型消息
                if content == 'ding':
                    await sendTextMsgToContact(contact=contact, text="这是自动回复: dong dong dong")
                elif content == 'hi' or content == '你好' or content == "帮助":
                    info0 = "我是你的个人小助手，很高兴为您服务!\n"
                    info1 = "1.收到'ding',自动回复\n"
                    info2 = "2.收到'帮助',自动回复\n"
                    info3 = "3.收到'小程序'or'微信小程序'，自动回复\n"
                    info4 = "4.收到'情话@your_content',自动回复，例如 情话@春天\n"
                    info5 = "5.收到'藏头诗@your_content',自动回复，例如 藏头诗@我喜欢你\n"
                    info6 = "6.收到'city+天气',自动回复，例如 长沙天气\n"
                    info7 = "7.收到'查成绩+学号+密码',自动回复，例如 查成绩201802060124+教务系统密码"
                    info8 = "8.收到'昆明地铁自动回复',自动回复"
                    info9 = "9.收到'校园美景',自动回复"
                    info10 = "10.收到'学校简介',自动回复"
                    info11 = "7.收到'查课表+学号+密码',自动回复，例如 查课表201802060124+教务系统密码"
                    help_info = info0 + info1 + info2 + info3 + info4 + info5 + info6 + info7
                    await sendTextMsgToContact(contact=contact, text=help_info)
                elif content == '小程序' or content == "微信小程序":
                    file_url = 'http://botbay.leceshi.cn/mini.jpg'
                    await sendMediaMsgToContact(contact=contact, fileUrl=file_url, filePath='')
                elif '天气' in content:
                    city_name = content[:-2]
                    weather_info = get_weather_data(city_name)
                    await contact.say(weather_info)
#查成绩201802060124 song13888001203
                elif '查成绩' in content:
                    username = content[3:15]
                    password = content.replace('查成绩'+username+'+','')
                    score_info = getScore(username,password)
                    await contact.say(score_info)

                elif '查课表' in content:
                    username = content[3:15]
                    password = content.replace('查课表'+username+'+','')
                    class_info = getclass(username,password)
                    await contact.say(class_info)

                elif '校园美景' in content:
                    file_url = 'http://www.oxbridge.cn/Libs/XYMJ/KG/8.jpg'
                    await sendMediaMsgToContact(contact=contact, fileUrl=file_url, filePath='')

                elif '家里情况' in content:
                    
                    test_download()

                    #获取文件夹下的所有文件名
                    lists = os.listdir(r'D:\wechaty\wechaty机器人\paddlehub_wechaty-master\paddlehub_wechaty-master')
                    #按照修改时间排序文件
                    lists.sort(key=lambda x:os.path.getmtime(r'D:\wechaty\wechaty机器人\paddlehub_wechaty-master\paddlehub_wechaty-master' +'/'+x))
                    #得到最新文件的文件名
                    file_new = lists[-1]
                    #若需要，给最新文件的文件名加上路径
                    file_new = os.path.join(r'D:\wechaty\wechaty机器人\paddlehub_wechaty-master\paddlehub_wechaty-master',lists[-1])
                    
                    time.sleep(3)

                    await sendMediaMsgToContact(contact=contact, fileUrl='', filePath=file_new)


                elif '学校简介' in content:
                    information = '昆明理工大学津桥学院（以下简称“学校”）成立于2001年，是由昆明理工大学申办、云南省国有大型企业云南省康旅控股集团有限公司'\
                                    '（原云南省城市建设投资集团有限公司）投资，经云南省教育厅审核、国家教育部批准的全日制本科独立学院。'\
                                    '学校以工科为主，经、管、文、法、理、教育多学科协调发展，现设有电气与信息工程学院、建筑工程学院、'\
                                    '经济管理学院、语言文化学院、法学院、理工学院6个二级学院和思想政治理论课、'\
                                    '体育课2个教学部，开办40个本科专业，在校生11630人。学校校园占地面积共1209.28亩，分为高新、空港两个校区。'
                    await sendTextMsgToContact(contact=contact, text=information)
                
                elif '昆明地铁' in content:
                    file_url = 'http://botbay.leceshi.cn/ditie.jpg'
                    await sendMediaMsgToContact(contact=contact, fileUrl=file_url, filePath='')
                    time.sleep(4)
                    await sendTextMsgToContact(contact=contact, text='可能我是世界上最皮的地铁了')


                elif "情话" in content:
                    content = content[3:]
                    res = chat_bot(content=content, mode='1')
                    await contact.say(res)
                elif "藏头诗" in content:
                    # 藏头诗模式
                    content = content[4:]
                    res = chat_bot(content=content, mode='2')
                    await contact.say(res)
                else:
                    res = chat_bot(content=content, mode='0')
                    await contact.say(res)
            #  处理图片类型消息
            elif msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
                dividing_line()
                await contact.say('不好意思,暂时处理不了图片类型消息,我们已经在催程序员小哥哥日夜加班优化项目了!希望您能够理解!')


    async def on_scan(self, qr_code: str, status: ScanStatus,
                      data: Optional[str] = None):
        """
        Scan Handler for the Bot
        """
        print('Scan QR Code to login: {}\n'.format(status))
        print('View QR Code Online: https://wechaty.js.org/qrcode/{}'.format(qr_code))

    async def on_login(self, contact: Contact):
        """
        Login Handler for the Bot
        """
        print(f'User {contact} logged in\n')
        # TODO: To be written

    async def on_logout(self, contact: Contact):
        print(f'User <{contact}> logout')

    async def on_friendship(self, friendship: Friendship):
        name = friendship.contact().name
        hello = friendship.hello()
        logMsg = name + '发送了好友请求'
        print(logMsg)
        # print(hello)
        try:
            if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
                if len(config.ACCEPTFRIEND) == 0:
                    print('无认证关键词,自动通过好友请求')
                    await friendship.accept()
                elif len(config.ACCEPTFRIEND) > 0 and (hello in config.ACCEPTFRIEND):
                    print('触发关键词{},自动通过好友请求'.format(hello))
                    await friendship.accept()
            elif friendship.type() == Friendship.Type.Confirm:
                logMsg = name + '已确认添加好友'
                print(logMsg)
            else:
                print('我不能同意你成为我的好友')
        except:
            print('添加好友出错')


async def main():
    """
    Async Main Entry
    """
    # 配置token
    os.environ['WECHATY_PUPPET'] = "wechaty-puppet-sevice"
    # 对应docker部署的token
    
    # os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = "162.219.121.99:8080"
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_padlocal_48b0323381df4a518b4bc9e1cc92ca42'
    # 对应docker部署的地址
    # os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = "81.69.14.8:8080"
    # Make sure we have set WECHATY_PUPPET_SERVICE_TOKEN in the environment variables.
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')
    global bot
    bot = MyBot()
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
