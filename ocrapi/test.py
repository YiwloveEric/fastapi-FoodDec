# coding=utf-8
from ocrapi import SparkApi
import sys
import json
import base64
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

IS_PY3 = True
# 防止https证书校验不正确
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class ocr_image():
    def __init__(self, img_dir):
        self.image_url = img_dir
        ssl._create_default_https_context = ssl._create_unverified_context
        # 以下密钥信息从控制台获取
        self.appid = "768b44c9"  # 填写控制台中获取的 APPID 信息
        self.api_secret = "NTk4ZjhkMTE1ODU4Yzk0M2E3M2VhYjVi"  # 填写控制台中获取的 APISecret 信息
        self.api_key = "1ea1f8eef0ba6afadafe7661968c2ed8"  # 填写控制台中获取的 APIKey 信息

        # 用于配置大模型版本，默认“general/generalv2”
        self.domain = "generalv3"  # v1.5版本
        # domain = "generalv2"    # v2.0版本
        # 云端环境的服务地址
        self.Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v1.5环境的地址
        # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

        self.text = []

        self.API_KEY = 'EMHEZPxO1XGhg6z5Og1BTAG9'
        self.SECRET_KEY = 'kg9KrENam3CjyBWidrcubKiV0FdmDtSO'
        self.OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

        """  TOKEN start """
        self.TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

    def getText(self, role, content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        self.text.append(jsoncon)
        return self.text

    """
        获取token
    """

    def fetch_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.API_KEY,
                  'client_secret': self.SECRET_KEY}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(self.TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print(err)
        if (IS_PY3):
            result_str = result_str.decode()

        result = json.loads(result_str)

        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not 'brain_all_scope' in result['scope'].split(' '):
                print('please ensure has check the  ability')
                exit()
            return result['access_token']
        else:
            print('please overwrite the correct API_KEY and SECRET_KEY')
            exit()

    """
        读取文件
    """

    def read_file(self, image_path):
        f = None
        try:
            f = open(image_path, 'rb')
            return f.read()
        except:
            print('read image file fail')
            return None
        finally:
            if f:
                f.close()

    """
        调用远程服务
    """

    def request(self, url, data):
        req = Request(url, data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
            if (IS_PY3):
                result_str = result_str.decode()
            return result_str
        except  URLError as err:
            print(err)

    def process(self):

        # 获取access token
        token = self.fetch_token()

        # 拼接通用文字识别高精度url
        image_url = self.OCR_URL + "?access_token=" + token

        text1 = ""

        # 读取测试图片
        file_content = self.read_file(self.image_url)

        # 调用文字识别服务
        result = self.request(image_url, urlencode({'image': base64.b64encode(file_content)}))

        # 解析返回结果
        result_json = json.loads(result)
        print(result_json)
        for words_result in result_json["words_result"]:
            text1 = text1 + words_result["words"]
        # 打印文字
        print(text1)
        question = self.getText("user", "请返回其中的配料表，返回的格式为：‘配料表:xxx,xxx,xxx’,如果一个配料后面有括号，括号里面包含多个配料，则舍去括号里面的配料。"+
                                        "例如复合氨基酸粉（亮氨酸、异亮氨氨酸、苏氨酸、蛋氨酸、苯丙氨酸、丙氨酸)，则只要复合氨基酸粉" + text1)
        SparkApi.answer = ""
        SparkApi.main(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, question)
        word = self.getText("assistant", SparkApi.answer)
        return SparkApi.answer

    def result(self):
        word = self.process()
        # 找到配料表的索引
        index = word.find("：")
        if index != -1:
            # 获取冒号后面的字符串
            ingredients_after_colon = word[index + 1:].strip()[:-1]
        else:
            ingredients_after_colon = []
        return ingredients_after_colon.split('、')


if __name__ == "__main__":
    ocr_tes = ocr_image('./test2.jpg')  # 传入图片的本地路径
    print(ocr_tes.result())
