from flask import Flask, request
from googletrans import Translator
from langdetect import detect
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"

@app.route('/webhook', methods=['POST'])
def webhook():
    def get_DataBase():
        certificate = {"type": "service_account", "project_id": "smart-msds-ntoq", "private_key_id": "53295a6b6be80c11c0452b5dceca7aa017d99924", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCeOlvy0Nd4BPhu\nVHH6BOL3dzfifcg9MVE1UG1PVkVebJXE0yUfDSl1+QGG/AOqoUNZOqw8waZCAZEz\n53C3vgeAbAKPVZQ1GBb8SudQpSQN4S2n1K8wsass82y298DLMRi8Ulc35gz6j+0e\njbAyeZag9WtlBk3u+0vr2wol5OMaUoLQO0KIlPUwjZ0VytAwbxD/1SMnTOwCUc6+\noqbR2uScEl5vc+ObbaflIycyR39Ez2ozhKOpFPSf26z+lEoDEgVOiPcClS2LIJw0\nORGqIAMCq/GFdv2TuwPJxA0GSf47k/VPHsrCcgQPXkQOAYxGHHBd6tAs7zXy1Dml\nZ4xnDsFPAgMBAAECggEAKcsTZ2cXSrnRXt8KPfZVdvTz+2yq29LvdswYG1kXuJGo\n25TD3NhOp70OVLezRjoTPnnbba7eudeNIW8T3Eyi0Z517KM3ovCKfbhRMgF0rP/Z\n3dc1MQD0zEo94HQ/ZcxBktiS9g5bRkGG6ceWDzcDfN9mLwiDxEh3LMSuAQVcoSJY\nrrlavtwxaCpOfmga0AysnHn+aRrsh7w6OL9SY6GQV68k0TxXserKDcpyx/IfTqnt\nNrZxskOQdwsiMks7oQxjfFWlB9lAz5tl8jUoTOK8cBuvxOxSUlpsjLtWtow5zUtz\n4CjWaALhl1xgXn3unVUNIpPOjO5cVhWJbwsaPypUoQKBgQDVdLkAY30U1HpT1UzQ\nXP6QmF1G+m2emecqlEahkg0+4dNwheyGgUNpRG95xNjycmL+VBiH6jigBXeBnjqK\nrqqdZ8ASzEjiyTFVMNp+WVBsEjf0x3ENcZVRcciehbLMyjKB1jfj7P5J2BtMIhDH\ncZmmR2yEX7dH9ruorfPpP/xjLwKBgQC9w7WkZ8L+Hd0L0ugH+OReZxbr9fTzd8zn\nzzVl095b5++NCHyPwdFGs4F0NECxpiZp1lURpEvZSSuTrqaESBeRiSuV/qTWSocL\nt1x/XXRnryqdaaFMFkaSyicU00Kpv67h2oL+3iD337K3SDmaCPqSMSiDJRZAdG7/\npsslLax74QKBgQC3pp9taCu7+jvtWP2n3/rd6VmHsfsSlBPCHKTQalqfGajTjUY9\nS4X2Uf0fZW/K2QO3Eh+xAKILe+igSsTPgQwmNZeaFM044iVhyJCUWL/K27ntDpOE\nH4967UzQpvN5IxZlgyu/HK6EVjzWOhD5qBGscJM7KScF8ZDvxgqvSnAZ3QKBgFKH\nSPoFPmJx7m5z/QFqlzcPMoLQZwVztqOiFCEC8ZOa3S3C4RlMO426B7TX/MLF9bLV\nyg1wHKSVE+SYckbZa5aZx2DmbB3eL7lCt3GU3UkyfyASjlme3nZ8gF6oOjfE63PC\nKnJZfJEQspLPUG3TNdZalrniaTkC6js4+ORkZr1BAoGAaCxiYVmzSFBDakdN1WV0\nqs4/aqG7RakLdvrJ0kIVa2c9EriUBP1x0CQDnn5MPj7OLn+yTU78HZe2WCg/5Yrk\n/6NeOMFOfN2CwhUXs8oe7edqbQUt5EEz+uxYRHGiqC7OyRXmgoxifj1X1ffBapm7\nGLYPfk3TRHIgn27L2heG42Y=\n-----END PRIVATE KEY-----\n", "client_email": "firebase-adminsdk-ajpld@smart-msds-ntoq.iam.gserviceaccount.com", "client_id": "103913831689164165809", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ajpld%40smart-msds-ntoq.iam.gserviceaccount.com"}
        cred = credentials.Certificate(certificate)
        firebase_admin.initialize_app(cred, {'databaseURL' : 'https://smart-msds-ntoq-default-rtdb.asia-southeast1.firebasedatabase.app'})
        ref = db.reference()
        row = ref.get()
        print(row[0])
        return row
    server = get_DataBase()

    def languagedetect(sentence):
        detected = detect(sentence)
        return detected
        
    def translate2kor(chemicalId):
        translator = Translator()
        detected = languagedetect(chemicalId)
        trans2 = translator.translate(chemicalId, src=detected, dest='ko')
        trans = trans2.text
        
        return trans

    def translate2foreign(chemicalId, kor_sentence):
        translator = Translator()
        detected = languagedetect(chemicalId)
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
                # print(i)
            if '가' in i:
                i = i.replace('가', '')
                searchword = i
                c = 1
                break
                # print(i)
            if '을' in i:
                i = i.replace('을', '')
                searchword = i
                c = 1
                break
                # print(i)
            if '를' in i:
                i = i.replace('를', '')
                searchword = i
                c = 1
                break
                # print(i)
            if '는' in i:
                i = i.replace('는', '')
                searchword = i
                c = 1
                break
            if '은' in i:
                i = i.replace('는', '')
                searchword = i
                c = 1
                break
                # print(i)
        
        if c == 0:
            chemid = chemid_trans_handiling_saving(chemicalId)
            searchword = chemid
        
        return searchword

    def chemid_trans_handiling_saving(chemicalId):
        searchword_kor = translate2kor(chemicalId)
        searchword_kor = str(searchword_kor)
        print(searchword_kor)
        return searchword_kor

    def material_number(chemicalId):  
   
        searchword = chemid_trans(chemicalId)
        print(searchword)
        b = 0
        
        chemkor = server.index
   
        for item in chemkor:
            if item == searchword:
                # print(item)
                b = 1
                chemid = item
                break
           
            else: 
                if searchword in item:
                    print(searchword)
                    index = item.index(searchword)
                    print(item.index(searchword))
                    
                    if index == 0:
                        chemid = item
                    if item[index-1] == searchword[0]:
                        chemid = item
                    if searchword + ' ' in item:
                        pass
                    if ' ' + searchword  in item:
                        pass
                    if ' ' + searchword  in item:
                        pass
                    if searchword + '의' in item:
                        pass
                    else:
                        # print(item)
                        chemid = item
                        b = 1
                        break

            if b == 0:
                chemid = '없음'
            # print(chemid)
        return chemid


    def Return_handiling(chemicalId):
        sentence = translate2kor(chemicalId)
        print(sentence)
        print(server.index)
        material = chemid_trans_handiling_saving(chemicalId)
        full_material = material_number(material)
        print(full_material)
        total_text = server.loc[full_material]['취급주의사항']
        print(total_text)
        trans = translate2foreign(chemicalId, total_text)
        answer = {'fulfillmentText': trans}

        return answer

    def Return_saving(chemicalId):
        sentence = translate2kor(chemicalId)
        print(sentence)
        print(server.index)
        material = chemid_trans_handiling_saving(chemicalId)
        full_material = material_number(material)
        print(full_material)
        total_text = server.loc[full_material]['저장방법']
        print(total_text)
        trans = translate2foreign(chemicalId, total_text)
        answer = {'fulfillmentText': trans}

        return answer

    def Return_response(chemicalId):
        sentence = translate2kor(chemicalId)

        print(server[0])
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
        print(a)
        material=chemid_trans(chemicalId)
        full_material = material_number(chemicalId)
        print(material)
        if material =='이가을를없음':
            total_text = "다시 한번 말씀해 주세요. (예문: 어떤 화학물질이 어느 부위에 노출되었습니다.)"
            # response = {'fulfillmentText': total_text}
        elif material =='없음':
            total_text = "죄송하지만 해당 물질은 지원하지 않습니다."
            # response = {'fulfillmentText': total_text}
            
        else:
            if a == 1:
                
                total_text = server.loc[full_material]['eye']
                        
            if a == 2:
               total_text = server.loc[full_material]['skin']
                        
            if a == 3:
                total_text = server.loc[full_material]['inhale']
                        
            if a == 4:
                total_text = server.loc[full_material]['eat']
                        
            if a == 5:
                total_text = server.loc[full_material]['doctor']
                    
                    
        # print(total_text)
        # print(total_text)
        response = {'fulfillmentText': total_text}

        trans = translate2foreign(chemicalId, total_text)
        
        answer = {'fulfillmentText': trans}
    
        return answer
        
                    
    jsonObj = request.get_json(force=True) # Parse data as JSON(=
    print(jsonObj)
    chemicalId = jsonObj['queryResult']['queryText'] # 001097
    intent = jsonObj['queryResult']['intent']['displayName']
    print(intent)
    if intent == '화학물질 초기대응 알려줘 - custom':
        response = Return_response(chemicalId)
    if intent == '화학물질 초기대응 알려줘 - fallback':
        response = Return_response(chemicalId)
    if intent == '화학물질 취급방법 알려줘 - custom':
        response = Return_handiling(chemicalId)
    elif intent == '화학물질 취급방법 알려줘 - fallback':
        response = Return_handiling(chemicalId)
    if intent == '화학물질 저장방법 알려줘 - custom':
        response = Return_saving(chemicalId)
    elif intent == '화학물질 저장방법 알려줘 - fallback':
        response = Return_saving(chemicalId)

    # print(response)
    return response

# ctrl + shift + F10 (or alt shift f10)
if __name__ == '__main__':

    app.run(host='127.0.0.1', debug=True, port=5000)
