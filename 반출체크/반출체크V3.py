import pyautogui
import time
import datetime
import sys
import requests
from xml.etree import ElementTree

def find_bl():

    i=0
    while i < len(checkList):

        apiUrl = f"https://unipass.customs.go.kr:38010/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo?crkyCn=r200z280o057z221p040r040c0&hblNo={checkList[i]}&blYy=2020"
        Data = requests.get(apiUrl)
        TextXmlData = Data.text
        text2Xml = ElementTree.fromstring(TextXmlData)
        result = text2Xml.iter(tag='cargCsclPrgsInfoQryRtnVo')
        for element in result:
            if element.find("tCnt").text =='0':
                진행상태.append('조회불가')
                처리일시.append('조회불가')
                통관진행상태.append('조회불가')
            else:
                진행상태.append(element.find("cargCsclPrgsInfoQryVo").find("prgsStts").text)  
                tempTime = element.find("cargCsclPrgsInfoQryVo").find("prcsDttm").text
                tempTime = f'{tempTime[0:4]}년{tempTime[4:6]}월{tempTime[6:8]}일  {tempTime[8:10]}:{tempTime[10:12]}:{tempTime[12:]}'
                처리일시.append(tempTime)  
                통관진행상태.append(element.find("cargCsclPrgsInfoQryVo").find("csclPrgsStts").text)
                

            
        i += 1
def create_msg(msg):
    i = 0
    while i < len(진행상태):
        if 진행상태[i] == "조회불가":
            msg = msg + f'{i + 1}.{checkList[i]}\n{진행상태[i]}\n\n'
        else:
            msg = msg + f'{i + 1}.{checkList[i]}\n{진행상태[i]}\n{처리일시[i]}\n{통관진행상태[i]}\n\n'
        i += 1
    return msg
checkList = []
진행상태 = [] #진행상태 prgsStts 
처리일시 = [] #처리일시 prcsDttm
통관진행상태 = [] #통관진행상태 csclPrgsStts
added_bl = []

MSG_1 = pyautogui.prompt('비엘번호 입력', '반출체크','여기 입력하세요',)
if MSG_1 == None:
    sys.exit()
if MSG_1 != None:
    checkList.append(MSG_1.upper())  
    MSG_2 = pyautogui.confirm('비엘을 추가하시겠습니까?', buttons=['예','아니오(조회하기)'])
    if MSG_2 == None:
        sys.exit()

    if MSG_2 == '예':
        while True:
            MSG_1 = pyautogui.prompt('비엘번호 입력', '반출체크(Cancel = 조회하기)', '여기 입력하세요', )
            if MSG_1 == None:
                break
            if MSG_1 != None:
                checkList.append(MSG_1.upper())
                MSG_2 = pyautogui.confirm('비엘을 추가하시겠습니까?', buttons=['예', '아니오(조회하기)'])
                if MSG_2 == '아니오(조회하기)':
                    break

    while True:
        진행상태.clear()
        처리일시.clear()
        통관진행상태.clear()
        added_bl.clear()

        find_bl()

        msg = create_msg(msg='')

        now = datetime.datetime.now()

        whileBreaker = False

        result = pyautogui.confirm(f'{msg}\n 조회 시간 : {now.hour}시 {now.minute}분 {now.second}초', '유니패스 조회결과', buttons=['다시 조회', '비엘 추가 or 제외','종료'])
        if result == '다시 조회':
            continue
        if result == '종료' or result == None:
            sys.exit()
        if result == '비엘 추가 or 제외':
            org_msg = create_msg(msg='')
            while True:
                reviseBL = pyautogui.prompt(org_msg, '비엘 추가 or 제외', '추가 할 비엘번호 or 제외 할 색인 한 개 입력 ex)1,2,3...')
                if reviseBL == None: 
                    sys.exit()
                if reviseBL == '':
                    whileBreaker = False
                    break
                if len(reviseBL) <= 2: # 숫자가 범위를 초과했을 경우에
                    try:
                        if checkList[int(reviseBL) - 1] in added_bl:
                            del added_bl[added_bl.index(checkList[int(reviseBL) - 1])]
                            del checkList[int(reviseBL) - 1]
                        else:
                            del checkList[int(reviseBL)-1]
                            del 진행상태[int(reviseBL)-1]
                            del 처리일시[int(reviseBL)-1]
                            del 통관진행상태[int(reviseBL)-1]

                        revise_msg = ''
                        if len(added_bl) > 0:
                            i = 0
                            while i < len(added_bl):
                                revise_msg = revise_msg + f'{len(checkList)-len(added_bl)+i+1}. {added_bl[i]}\n\n'
                                i += 1
                        org_msg = create_msg(msg='') + revise_msg
                        result = pyautogui.confirm(org_msg, '유니패스 조회결과', buttons=['다시 조회', '비엘 추가 or 제외', '종료'])
                        if result == '다시 조회':
                            whileBreaker = False
                            break
                        if result == '비엘 추가 or 제외':
                            continue
                        if result == '종료':
                            sys.exit()
                    except ValueError:
                        pyautogui.alert(text='제외 할 색인의 숫자를 입력하셔야 됩니다.', title='Type error', button='OK')
                        continue
                    except IndexError:
                        pyautogui.alert(text='숫자 범위를 벗어났습니다. 색인 범위 안에서 입력해주세요', title='Index error', button='OK')
                        continue


                    
                if len(reviseBL) > 2:
                    if reviseBL.upper() in checkList:
                        result = pyautogui.confirm(f'{org_msg}', '유니패스 조회결과', buttons=['다시 조회', '비엘 추가 or 제외', '종료']) 
                    else:
                        checkList.append(reviseBL.upper())
                        added_bl.append(reviseBL.upper())
                        org_msg = org_msg + f'{len(checkList)}. ' + added_bl[len(added_bl)-1] + '\n' + '\n'
                        result = pyautogui.confirm(f'{org_msg}', '유니패스 조회결과', buttons=['다시 조회', '비엘 추가 or 제외', '종료'])
                    if result == '다시 조회':
                        whileBreaker = False
                        break
                    if result == '비엘 추가 or 제외':
                        continue
                    if result == '종료':
                        sys.exit()

        if whileBreaker == False:
            continue
