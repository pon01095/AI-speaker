from flask import Flask, request
import urllib
import urllib.request
from bs4 import BeautifulSoup
from googletrans import Translator
from langdetect import detect
import parser
import re

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"

@app.route('/webhook', methods=['POST'])
def webhook():
    def langdetect(sentence):
        detected = detect(sentence)
        print(detected)
        return detected
        
    def translate2kor(chemicalId):
        translator = Translator()
        detected = langdetect(chemicalId)
        trans2 = translator.translate(chemicalId, src=detected, dest='ko')
        trans = trans2.text
        
        return trans

    def translate2foreign(chemicalId, kor_sentence):
        translator = Translator()
        detected = langdetect(chemicalId)
        
        trans2 = translator.translate(kor_sentence, src='ko', dest=detected)
        trans = trans2.text
        
        return trans

    def chemid_data(chemicalId):
        searchword_kor = translate2kor(chemicalId).split(" ")
        
        return searchword_kor
        

    def chemid_trans(chemicalId):
     
        searchword_kor = chemid_data(chemicalId)
        c=0
        for i in searchword_kor:
            if '이' in i:
                i = i.replace('이', '')
                searchword=i
                c=1
                break
                print(i)
            if '가' in i:
                i = i.replace('가', '')
                searchword = i
                c = 1
                break
                print(i)
            if '을' in i:
                i = i.replace('을', '')
                searchword = i
                c = 1
                break
                print(i)
            if '를' in i:
                i = i.replace('를', '')
                searchword = i
                c = 1
                break
                print(i)
        
        if c == 0:
            chemid = '이가을를없음'
            searchword = chemid
        
        return searchword

    def chemid_decode(chemicalId):
        searchword = chemid_trans(chemicalId)
        if searchword == '이가을를없음':
            ValueError
        
        else:

            searchword1 = searchword.encode('UTF-8')
            searchword1 = str(searchword1)
            searchword1 = searchword1.replace("\\x", "%")
            searchword1 = searchword1.replace("'", "")
            searchword1 = searchword1[1:]
            print(searchword1)
        
        return searchword1
            
    def material_number(chemicalId):  
        searchword1 = chemid_decode(chemicalId)
        searchword = chemid_trans(chemicalId)
        url = "http://msds.kosha.or.kr/openapi/service/msdschem/chemlist?searchCnd=0&searchWrd=" + searchword1 + "&ServiceKey=" + serviceKey
        print(url)
        response = urllib.request.urlopen(url)
        response_code = response.getcode()
        # print(response_code)
        if response_code == 200:
            response_body = response.read().decode('utf-8')  # decode('utf-8') : 바이트열 -> 문자열(복호화)
            # print(response_body)
            soup = BeautifulSoup(response_body, 'html.parser')  # xml도 가능
            # print(soup.prettify())

            result = soup.find_all('item')
            # print(result)
            b = 0
            # print(result.text)
            for item in result:
                # print(item)
                chemkor = item.find('chemnamekor')
                chemkor = chemkor.text
                print(chemkor)
                print(searchword)
                if chemkor in searchword:
                    chemid_ele = item.find('chemid')
                    chemid = chemid_ele.text
                    print(chemkor)
                    b = 1
                    break
            if b == 0:
                chemid = '없음'

        return chemid


    # Open API 호출 (공공데이터포털 MSDS)

    def Call_API(chemicalId):
    
        sentence = translate2kor(chemicalId)
        # print(sentence)
        a=0
        if '눈' in sentence:
            a=1
            
        elif '안구' in sentence:
            a=1
        elif '피부' in sentence:
            a=2
        elif '흡입' in sentence:
            a=3
        elif '먹었' in sentence:
            a=4
        elif '주의사항' in sentence:
            a=5
        # print(a)
        material=chemid_trans(chemicalId)
        if material =='이가을를없음':
            total_text = "다시 한번 말씀해 주세요. (예문: 어떤 화학물질이 어느 부위에 노출되었습니다.)"
            response = {'fulfillmentText': total_text}
        elif material =='없음':
            total_text = "죄송하지만 해당 물질은 지원하지 않습니다."
            response = {'fulfillmentText': total_text}
        
        else:
            
            url = "http://msds.kosha.or.kr/openapi/service/msdschem/chemdetail04?chemId={}&ServiceKey={}".format(material_number(chemicalId), serviceKey)
            # http://msds.kosha.or.kr/openapi/service/msdschem/chemdetail04?chemId=001097&ServiceKey=bomugHU1Hd2U3LSQCXEgQv3FD60qZF83lx8mmzM1%2FzDIxr8ll1xzLG6jctThfCRxmbIPobWEryddgdgpbO%2F4%2Bg%3D%3D
            # print(url)
            response = urllib.request.urlopen(url)
            # print(response)
            response_code = response.getcode()
        
            if response_code == 200:
                response_body = response.read().decode('utf-8') # decode('utf-8') : 바이트열 -> 문자열(복호화)
                soup = BeautifulSoup(response_body, 'html.parser') # xml도 가능
                # print(soup.prettify())
        
                result = soup.find_all('item')
                # print(len(result))
                action_title_list = []
                action_detail_list = []
                for action in result:
                    action_title = action.find('msdsitemnamekor').text
                    if a == 1:
                        if action_title == '눈에 들어갔을 때':
                            action_detail = action.find('itemdetail').text
                            action_detail_list.append(action_detail)
                            action_title_list.append(action_title)
                            # print(action_detail)
                    elif a==2:
                        if action_title == '피부에 접촉했을 때':
                            action_detail = action.find('itemdetail').text
                            action_detail_list.append(action_detail)
                            action_title_list.append(action_title)
                            # print(action_detail)
                    elif a==3:
                        if action_title == '흡입했을 때':
                            action_detail = action.find('itemdetail').text
                            action_detail_list.append(action_detail)
                            action_title_list.append(action_title)
                            # print(action_detail)
                    elif a==4:
                        if action_title == '먹었을 때':
                            action_detail = action.find('itemdetail').text
                            action_detail_list.append(action_detail)
                            action_title_list.append(action_title)
                            # print(action_detail)
                    elif a==5:
                        if action_title == '기타 의사의 주의사항':
                            action_detail = action.find('itemdetail').text
                            action_detail_list.append(action_detail)
                            action_title_list.append(action_title)
                            # print(action_detail)
                total_text = "\n\n".join(action_detail_list)
                # print(total_text)
        
                first_aid = {}
                for title, detail in zip(action_title_list, action_detail_list):
                    first_aid.setdefault(title, []).append(detail)
        
                # print(first_aid.keys())
        
            # 결과 메시지
            
            response = {'fulfillmentText': total_text}
            # print(total_text)
            # translate2foreign
            # trans2 = translator.translate(response['fulfillmentText'], src='ko', dest='zh-CN')
            trans = translate2foreign(chemicalId, response['fulfillmentText'])
            # print(trans)
            # print(trans2.text)
            # trans = trans2.text
            answer = {'fulfillmentText': trans}
        
        return answer
    serviceKey = "EGYpXgaRsbr85%2FEOQFeUMChRV1XSfoGmANilfsEIZMSHWrUh6MNw2WsP8xrwsR7kGfDPoGnaFXPhT0%2B%2B3Mu%2FGw%3D%3D"  # encoding
    jsonObj = request.get_json(force=True) # Parse data as JSON(=dict)


    chemicalId = jsonObj['queryResult']['queryText'] # 001097
    print(chemicalId)
    response = Call_API(chemicalId)
    print(response)
    return response


# ctrl + shift + F10 (or alt shift f10)
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
