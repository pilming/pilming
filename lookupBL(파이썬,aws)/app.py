from flask import Flask, render_template, request
import requests
from xml.etree import ElementTree

app = Flask(__name__)

@app.route('/')
def index():
       # render your html template
       status1=['-', '-', '-', '-', '-', '-', '-', '-']
       status2=['-', '-', '-', '-', '-', '-', '-', '-']
       status3=['-', '-', '-', '-', '-', '-', '-', '-']
       status4=['-', '-', '-', '-', '-', '-', '-', '-']
       status5=['-', '-', '-', '-', '-', '-', '-', '-']
       status1Detail=[]
       status2Detail=[]
       status3Detail=[]
       status4Detail=[]
       status5Detail=[]
       i = 0
       while i < 15:
              status1Detail.append(['-','-','-','-','-','-'])
              status2Detail.append(['-','-','-','-','-','-'])
              status3Detail.append(['-','-','-','-','-','-'])
              status4Detail.append(['-','-','-','-','-','-'])
              status5Detail.append(['-','-','-','-','-','-'])
              i += 1

       defaltBlNumber= ['','','','','']
       defaltYear = ["2020","2020","2020","2020","2020"]

       return render_template('index.html',status1 = status1 ,status2 = status2 ,status3 = status3
       ,status4 = status4 ,status5 = status5, blNumber = defaltBlNumber, blYear = defaltYear, status1Detail=status1Detail, status2Detail=status2Detail
       , status3Detail=status3Detail, status4Detail=status4Detail, status5Detail=status5Detail)

@app.route('/search', methods=['POST','GET'])
def search():
       if request.method == 'POST':
              blInformation = request.form      #["blInfo"]    #대괄호로 해줘야됨    이걸 받아서 다시 비엘번호로 전달
              blInformation = blInformation.getlist("blInfo")
              blNumber = []
              blYear = []
              i=0
              while i < len(blInformation):
                     if i % 2 == 0:
                            blYear.append(blInformation[i])
                     else:
                            blNumber.append(blInformation[i].upper().strip())
                     i += 1

              status1=['-','-','-','-','-','-','-','-']
              status2=['-','-','-','-','-','-','-','-']
              status3=['-','-','-','-','-','-','-','-']
              status4=['-','-','-','-','-','-','-','-']
              status5=['-','-','-','-','-','-','-','-']
              status1Detail=[]
              status2Detail=[]
              status3Detail=[]
              status4Detail=[]
              status5Detail=[]
              i = 0
              while i < 15:
                     status1Detail.append(['-','-','-','-','-','-'])
                     status2Detail.append(['-','-','-','-','-','-'])
                     status3Detail.append(['-','-','-','-','-','-'])
                     status4Detail.append(['-','-','-','-','-','-'])
                     status5Detail.append(['-','-','-','-','-','-'])
                     i += 1
              i = 0
              while i < len(blNumber):
                     if(blNumber[i] != ''):
                            apiUrl = "https://unipass.customs.go.kr:38010/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo?crkyCn=r200z280o057z221p040r040c0&hblNo="+blNumber[i]+"&blYy="+blYear[i]
                            url = requests.get(apiUrl)
                            urlText = url.text
                            tree = ElementTree.fromstring(urlText)
                            result = tree.iter(tag='cargCsclPrgsInfoQryRtnVo')
                            for element in result:
                                   if element.find('tCnt').text != '0':
                                          locals()['status{}'.format(i+1)][0] = element.find('cargCsclPrgsInfoQryVo').find("prgsStts").text
                                          locals()['status{}'.format(i+1)][1] = element.find('cargCsclPrgsInfoQryVo').find("prnm").text
                                          tempTime = element.find('cargCsclPrgsInfoQryVo').find("prcsDttm").text
                                          tempTime = tempTime[0:4]+'년'+tempTime[4:6]+'월'+tempTime[6:8]+'일  '+tempTime[8:10]+':'+tempTime[10:12]+':'+tempTime[12:]
                                          locals()['status{}'.format(i+1)][2] = tempTime
                                          locals()['status{}'.format(i+1)][3] = element.find('cargCsclPrgsInfoQryVo').find("pckGcnt").text + element.find('cargCsclPrgsInfoQryVo').find("pckUt").text
                                          locals()['status{}'.format(i+1)][4] = element.find('cargCsclPrgsInfoQryVo').find("csclPrgsStts").text
                                          locals()['status{}'.format(i+1)][5] = element.find('cargCsclPrgsInfoQryVo').find("ttwg").text + element.find('cargCsclPrgsInfoQryVo').find("wghtUt").text                                         
                                          locals()['status{}'.format(i+1)][6] = element.find('cargCsclPrgsInfoQryVo').find("shipNm").text
                                          tempArrivalTime = element.find('cargCsclPrgsInfoQryVo').find("etprDt").text
                                          tempArrivalTime = tempArrivalTime[0:4]+'-'+tempArrivalTime[4:6]+'-'+tempArrivalTime[6:]
                                          locals()['status{}'.format(i+1)][7] = tempArrivalTime

                                          subResult = tree.iter(tag='cargCsclPrgsInfoDtlQryVo')
                                          lenCheck=[]
                                          for temp in subResult:
                                                 lenCheck.append(element.find('cargCsclPrgsInfoQryVo').find("prcsDttm").text)
                                          if len(lenCheck) <= 15:
                                                 k=0
                                                 while k < len(lenCheck):
                                                        locals()['status{}Detail'.format(i+1)][k][0] = len(lenCheck)-k
                                                        k += 1
                                                 l=0
                                                 subResult = tree.iter(tag='cargCsclPrgsInfoDtlQryVo')
                                                 for part in subResult:                                                       
                                                        if part.find('cargTrcnRelaBsopTpcd').text != None:
                                                               locals()['status{}Detail'.format(i+1)][l][1] = part.find('cargTrcnRelaBsopTpcd').text
                                                        if part.find("prcsDttm").text !=None:
                                                               tempTime = part.find("prcsDttm").text
                                                               tempTime = tempTime[0:4]+'년'+tempTime[4:6]+'월'+tempTime[6:8]+'일  '+tempTime[8:10]+':'+tempTime[10:12]+':'+tempTime[12:]
                                                               locals()['status{}Detail'.format(i+1)][l][2] = tempTime
                                                        if part.find("shedNm").text !=None:
                                                               locals()['status{}Detail'.format(i+1)][l][3] = part.find("shedNm").text
                                                        if part.find("pckGcnt").text !=None and part.find("pckUt").text !=None:
                                                               locals()['status{}Detail'.format(i+1)][l][4] = part.find("pckGcnt").text + part.find("pckUt").text
                                                        if part.find("wght").text != None and part.find("wghtUt").text != None:
                                                               locals()['status{}Detail'.format(i+1)][l][5] = part.find("wght").text + part.find("wghtUt").text        
                                                        l += 1
                                                        
                                          else:
                                                 k=0
                                                 while k < 15:
                                                        locals()['status{}Detail'.format(i+1)][k][0] = 15-k
                                                        k += 1

                                                 m = 0
                                                 subResult = tree.iter(tag='cargCsclPrgsInfoDtlQryVo')
                                                 for part in subResult:
                                                        if m < 15:
                                                               if part.find('cargTrcnRelaBsopTpcd').text != None:
                                                                      locals()['status{}Detail'.format(i+1)][m][1] = part.find('cargTrcnRelaBsopTpcd').text
                                                               if part.find("prcsDttm").text !=None:
                                                                      tempTime = part.find("prcsDttm").text
                                                                      tempTime = tempTime[0:4]+'년'+tempTime[4:6]+'월'+tempTime[6:8]+'일  '+tempTime[8:10]+':'+tempTime[10:12]+':'+tempTime[12:]
                                                                      locals()['status{}Detail'.format(i+1)][m][2] = tempTime
                                                               if part.find("shedNm").text !=None:
                                                                      locals()['status{}Detail'.format(i+1)][m][3] = part.find("shedNm").text
                                                               if part.find("pckGcnt").text !=None and part.find("pckUt").text !=None:
                                                                      locals()['status{}Detail'.format(i+1)][m][4] = part.find("pckGcnt").text + part.find("pckUt").text
                                                               if part.find("wght").text != None and part.find("wghtUt").text != None:
                                                                      locals()['status{}Detail'.format(i+1)][m][5] = part.find("wght").text + part.find("wghtUt").text                         
                                                        m += 1                                                                                  
                                   else:
                                          j=0
                                          while j < len(locals()['status{}'.format(i+1)]):
                                                 locals()['status{}'.format(i+1)][j] = '조회불가능'
                                                 j += 1                                                                                  
                     i += 1
              return render_template('index.html',status1 = status1 ,status2 = status2 ,status3 = status3
       ,status4 = status4 ,status5 = status5, blNumber = blNumber, blYear = blYear, status1Detail=status1Detail, status2Detail=status2Detail
       , status3Detail=status3Detail, status4Detail=status4Detail, status5Detail=status5Detail)

       elif request.method == 'GET':
              blNumber = request.args.get("blNum")
              apiUrl = "https://unipass.customs.go.kr:38010/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo?crkyCn=r200z280o057z221p040r040c0&hblNo="+str(blNumber)+"&blYy=2020"
              url = requests.get(apiUrl)
              urlText = url.text
              xmlValue = []
              tree = ElementTree.fromstring(urlText)
              result = tree.iter(tag='cargCsclPrgsInfoQryVo')
              testData = None
              for element in result:
                     xmlValue.append(element.find("prgsStts").text)
                     xmlValue.append(element.find("prnm").text)
                     tempTime = element.find("prcsDttm").text
                     tempTime = tempTime[0:4]+'년'+tempTime[4:6]+'월'+tempTime[6:8]+'일  '+tempTime[8:10]+':'+tempTime[10:12]+':'+tempTime[12]
                     xmlValue.append(tempTime)
                     xmlValue.append(element.find("pckGcnt").text + element.find("pckUt").text)
                     xmlValue.append(element.find("csclPrgsStts").text)
                     xmlValue.append(element.find("ttwg").text + element.find("wghtUt").text)                   
                     testData = xmlValue

              return render_template('index.html', testDataHtml = testData)

if __name__ == '__main__':
       app.run()