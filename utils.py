# ! /usr/bin/env python
# coding=gbk
import requests
import json
import smtplib
# import webbrowser
from email.mime.text import MIMEText
# from twilio.rest import Client
from urllib.request import urlopen, quote
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']


# ʹ��Twilio������ֻ��ŷ��Ͷ���
# # ����Ҫ�ڹ���������һ���˺ţ������ǹ�����https://www.twilio.com/
# def send_sms(msg='��ã������������Լ����ֻ�������Ϣ��', my_number='+8618217235290'):
#     # �ӹ������������Ϣ
#     account_sid = 'ACaf4b6a367d3dc718ba8c1ccaaaff91a9'
#     auth_token = '1d561065ea4b8857ec0537c25f9add1a'
#     twilio_number = '+12067456298'
#
#     client = Client(account_sid, auth_token)
#     try:
#         client.messages.create(to=my_number, from_=twilio_number, body=msg)
#         print('�����Ѿ����ͣ�')
#     except ConnectionError as e:
#         print('����ʧ�ܣ���������˺��Ƿ���Ч�������Ƿ����ã�')
#         return e


# ���ͼ������˻ظ�
# ��Ҫ��������������Msg�������ı����߱��飬����ֵ���ǻظ�����
# Key�ǽ���ͼ���������Ҫ����Կ����Ҫ�Լ���������ȡ
# def get_response(Msg, Key, Userid='ItChat'):
def get_response(Msg):
    # url = 'http://www.tuling123.com/openapi/api'
    # payloads = {'key': Key, 'info': Msg, 'userid': Userid, }
    # try:
        # r = requests.post(url, data=json.dumps(payloads)).json()
    # appid=""
    # sess = requests.get('https://api.ownthink.com/bot?appid='+appid+'&userid=userid&spoken='+Msg)
    sess = requests.get('https://api.ownthink.com/bot?spoken='+Msg)
    # answer = sess.text
    # answer = json.loads(answer)
    ans = json.loads(sess.text)
    answer = ans['data']['info']['text']

    return answer
    # except ConnectionError:
    #     return None
    # if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000):
    #     return
    # if r['code'] == 100000:  # �ı���
    #     return '\n'.join([r['text'].replace('<br>', '\n')])
    # elif r['code'] == 200000:  # ������
    #     return '\n'.join([r['text'].replace('<br>', '\n'), r['url']])
    # elif r['code'] == 302000:  # ������
    #     l = [r['text'].replace('<br>', '\n')]
    #     for n in r['list']: l.append('%s - %s' % (n['article'], n['detailurl']))
    #     return '\n'.join(l)
    # elif r['code'] == 308000:  # ������
    #     l = [r['text'].replace('<br>', '\n')]
    #     for n in r['list']: l.append('%s - %s' % (n['name'], n['detailurl']))
    #     return '\n'.join(l)
    # elif r['code'] == 313000:  # ������
    #     return '\n'.join([r['text'].replace('<br>', '\n')])
    # elif r['code'] == 314000:  # ʫ����
    #     return '\n'.join([r['text'].replace('<br>', '\n')])


# ʹ��QQ���䷢���ʼ�
# Content�Ƿ��͵����ݣ���ʽΪ{'header':'��ķ�������','text':'�����������'}
# HostUserName���Լ���QQ������
# KEY��QQ������Ȩ�룬ע�⣬�������룬��λ�ȡ��Ȩ����ٶ�
# ToUserName�����շ��������˺�
# def send_mail(Content, HostUserName, KEY, ToUserName):
#     # ��������˺�
#     _user = HostUserName
#     # ������д������Ȩ�룬��λ��QQ������Ȩ�룬��ٶ�
#     _pwd = KEY
#     # �����ǽ��շ������˺�
#     _to = ToUserName
#
#     msg = MIMEText(Content['text'])
#     msg["Subject"] = Content['header']
#     msg["From"] = _user
#     msg["To"] = _to
#
#     try:
#         s = smtplib.SMTP_SSL("smtp.qq.com", 465)
#         s.login(_user, _pwd)
#         s.sendmail(_user, _to, msg.as_string())
#         s.quit()
#         print("���ͳɹ���")
#     except smtplib.SMTPException as e:
#         print("����ʧ��,%s" % e)
#         return e
#

# ���ݵ�����þ�γ����Ϣ
def GetLngLat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'x2ZTlRkWM2FYoQbvGOufPnFK3Fx4vFR1'
    add = quote(address)
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    try:
        req = urlopen(uri)
    except ConnectionRefusedError as e:
        return e
    res = req.read().decode()
    temp = json.loads(res)  # ��json���ݽ��н���
    return temp


# ͳ�ƺ�����Ϣ
def frinds_info(UserName):
    male = 0
    female = 0
    other = 0
    pro_city = {}
    signature = {}
    star_friend = []

    for user in UserName:
        # �Ա�����
        if user['Sex'] == 1:
            male += 1
        elif user['Sex'] == 2:
            female += 1
        else:
            other += 1
        # ��������
        if (user['Province'] + ' ' + user['City']) in pro_city:
            pro_city[user['Province'] + ' ' + user['City']] += 1
        else:
            pro_city[user['Province'] + ' ' + user['City']] = 1
        # ǩ������
        if user['RemarkName'] == '':
            signature[user['RemarkName']] = user['Signature']
        else:
            signature[user['NickName']] = user['Signature']
        # �Ǳ�����
        if user['StarFriend'] == 1:
            star_friend.append(user['RemarkName'])

    return male, female, other, pro_city, signature, star_friend


# ���ӻ�������Ϣ
def view_info(male, female, other, pro_city, star_friend):
    # ��ʾ�Ա����
    labels = 'Male(%s)' % male, 'Female(%s)' % female, 'Other(%s)' % other, 'StarFriend(%s)' % len(star_friend)
    fracs = [male, female, other, len(star_friend)]

    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    patches, l_texts, p_texts = plt.pie(x=fracs, labels=labels, autopct='%3.1f %%', shadow=False,
                                        labeldistance=1.1, startangle=90, pctdistance=0.8)
    '''
    labeldistance���ı���λ����Զ���ж�Զ��1.1ָ1.1���뾶��λ��
    autopct��Բ������ı���ʽ��%3.1f%%��ʾС������λ��������һλ�ĸ�����
    shadow�����Ƿ�����Ӱ
    startangle����ʼ�Ƕȣ�0����ʾ��0��ʼ��ʱ��ת��Ϊ��һ�顣һ��ѡ���90�ȿ�ʼ�ȽϺÿ�
    pctdistance���ٷֱȵ�text��Բ�ĵľ���
    patches, l_texts, p_texts��Ϊ�˵õ���ͼ�ķ���ֵ��p_texts��ͼ�ڲ��ı��ģ�l_texts��ͼ��label���ı�
    '''
    # �ı��ı��Ĵ�С
    # �����ǰ�ÿһ��text����������set_size����������������
    for t in l_texts:
        t.set_size = 30
    for t in p_texts:
        t.set_size = 20

    fig = plt.gcf()
    # fig.set_size_inches(20, 20)
    fig.savefig('sex.png', dpi=500)
    # plt.show()

    # ��ʾ���зֲ�,ʹ�ðٶȵ�api�����Ӧ���еľ�γ�ȣ�Ȼ��ʹ��heatmap.json��������ͼ������html�ļ�
    json_data = ''
    # �ѳ�������תΪ��γ��
    for city, value in pro_city.items():
        try:
            pos = GetLngLat(city)
        except ConnectionError:
            pos = None
        if pos is not None and pos['status'] == 0:
            lng = pos['result']['location']['lng']
            lat = pos['result']['location']['lat']
            json_temp = '{"lng":' + str(lng) + ',"lat":' + str(lat) + ', "count":' + str(value) + '}, '
            json_data += '\n' + json_temp

    # ����html��ʽ����ͼ�ļ�
    try:
        head, rear = html_code()
        html_file = head + json_data + rear
        with open('heatmap.html', 'w', encoding='utf-8') as f:
            f.write(html_file)
            # ��ҳ��ʾ
            # webbrowser.open('heatmap.html', new=0, autoraise=True)
    except AttributeError:
        return AttributeError


# ���ӻ�����ͼhtml����
def html_code():
    head = '''<!DOCTYPE html>\n<html>\n<head>\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n    <script type="text/javascript" src="http://gc.kis.v2.scr.kaspersky-labs.com/C8BAC707-C937-574F-9A1F-B6E798DB62A0/main.js" charset="UTF-8"></script><script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=x2ZTlRkWM2FYoQbvGOufPnFK3Fx4vFR1"></script>\n    <script type="text/javascript" src="http://api.map.baidu.com/library/Heatmap/2.0/src/Heatmap_min.js"></script>\n    <title>����ͼ����ʾ��</title>\n    <style type="text/css">\n		ul,li{list-style: none;margin:0;padding:0;float:left;}\n		html{height:100%}\n		body{height:100%;margin:0px;padding:0px;font-family:"΢���ź�";}\n		#container{height:500px;width:100%;}\n		#r-result{width:100%;}\n    </style>	\n</head>\n<body>\n	<div id="container"></div>\n	<div id="r-result">\n		<input type="button"  onclick="openHeatmap();" value="��ʾ����ͼ"/><input type="button"  onclick="closeHeatmap();" value="�ر�����ͼ"/>\n	</div>\n</body>\n</html>\n<script type="text/javascript">\n    var map = new BMap.Map("container");          // ������ͼʵ��\n\n    var point = new BMap.Point(105.418261, 35.921984);\n    map.centerAndZoom(point, 5);             // ��ʼ����ͼ���������ĵ�����͵�ͼ����\n    map.enableScrollWheelZoom(); // �����������\n  \n    var points =['''
    rear = ''']\n   \n    if(!isSupportCanvas()){\n    	alert('����ͼĿǰֻ֧����canvas֧�ֵ������,����ʹ�õ����������ʹ������ͼ����~')\n    }\n	//��ϸ�Ĳ���,���Բ鿴heatmap.js���ĵ� https://github.com/pa7/heatmap.js/blob/master/README.md\n	//����˵������:\n	/* visible ����ͼ�Ƿ���ʾ,Ĭ��Ϊtrue\n     * opacity ������͸����,1-100\n     * radius ����ͼ��ÿ����İ뾶��С   \n     * gradient  {JSON} ����ͼ�Ľ������� . gradient������ʾ\n     *	{\n			.2:'rgb(0, 255, 255)',\n			.5:'rgb(0, 110, 255)',\n			.8:'rgb(100, 0, 255)'\n		}\n		���� key ��ʾ��ֵ��λ��, 0~1. \n		    value Ϊ��ɫֵ. \n     */\n	heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":20});\n	map.addOverlay(heatmapOverlay);\n	heatmapOverlay.setDataSet({data:points,max:10});\n	//�Ƿ���ʾ����ͼ\n    function openHeatmap(){\n        heatmapOverlay.show();\n    }\n	function closeHeatmap(){\n        heatmapOverlay.hide();\n    }\n	openHeatmap();\n    function setGradient(){\n     	/*��ʽ������ʾ:\n		{\n	  		0:'rgb(102, 255, 0)',\n	 	 	.5:'rgb(255, 170, 0)',\n		  	1:'rgb(255, 0, 0)'\n		}*/\n     	var gradient = {};\n     	var colors = document.querySelectorAll("input[type='color']");\n     	colors = [].slice.call(colors,0);\n     	colors.forEach(function(ele){\n			gradient[ele.getAttribute("data-key")] = ele.value; \n     	});\n        heatmapOverlay.setOptions({"gradient":gradient});\n    }\n	//�ж�������Ƿ�֧��canvas\n    function isSupportCanvas(){\n        var elem = document.createElement('canvas');\n        return !!(elem.getContext && elem.getContext('2d'));\n    }\n</script>'''

    return head, rear


if __name__ == '__main__':
    # HostUserName = "yooongchun@foxmail.com"
    # KEY = "ynfrkvjmyhwwcfij"
    # ToUserName = "zyc121561@sjtu.edu.cn"
    # send_mail({'text': '�������������һ�������ʼ���', 'header': '�����ʼ�'}, HostUserName, KEY, ToUserName)

    # ͼ������˽�����Ҫʹ�õ�key����Ҫ�Լ���ͼ������˹�������
    # key = ''

    result = get_response('Ҧ�����')
    print(result)
    # ������
    # send_sms()
