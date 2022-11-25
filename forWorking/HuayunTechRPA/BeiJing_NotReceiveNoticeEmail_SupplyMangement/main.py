# Github: GWillS163
# User: 駿清清 
# Date: 21/11/2022 
# Time: 14:17
import os
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
import csv

import openpyxl


def colLtrParamsConvert(supplyCompany, mailContents,
                        contactCom, contactMail, contPartner, staffPartner,
                        staffName, staffMailAcc, staffMailPsd, staffMailServer, staffMailPort):
    """
    将传入的字母列参数转换为数字
    :return:
    """
    return [getColNum(supplyCompany),
            [getColNum(i) for i in mailContents],

            getColNum(contactCom),
            getColNum(contPartner),
            getColNum(contactMail),
            getColNum(staffPartner),

            getColNum(staffName),
            getColNum(staffMailAcc),
            getColNum(staffMailPsd),
            getColNum(staffMailServer),
            getColNum(staffMailPort),
            ]


def getColLtr(colNum: int) -> str:
    """0 -> A, 1 -> B, 2 -> C, ..., 26->AA, ..., 311 -> KZ
    :param colNum: the Column number of the Column Letter of Excel mappings
    :return the letter of Excel column
    """
    if colNum < 26:
        return chr(colNum + 65)
    else:
        return getColLtr(colNum // 26 - 1) + getColLtr(colNum % 26)


def getColNum(colLtr: str) -> int:
    """A -> 0, B -> 1, C -> 2, ..., AA->26, ..., KZ -> 311
    :param colLtr: the Column Letter of Excel
    :return the sequence number of Excel column
    """
    # turn to upper case
    colLtr = colLtr.upper()
    if len(colLtr) == 1:
        return ord(colLtr) - 65
    else:
        return (ord(colLtr[0]) - 64) * 26 + getColNum(colLtr[1:])


def paramsCheck(contactPath: str, notReceivePath: str, staffPath: str, savePath: str):
    """
    参数检查, 传入的参数是否符合要求
    :param contactPath:
    :param notReceivePath:
    :param staffPath:
    :param savePath:
    :return:
    """
    if not os.path.exists(contactPath):
        raise Exception(f"联系人:{contactPath} not exist!")
    if not os.path.exists(notReceivePath):
        raise Exception(f"notReceiveXls:{notReceivePath} not exist!")
    if not os.path.exists(staffPath):
        raise Exception(f"staffXls:{staffPath} not exist!")
    if not os.path.exists(savePath):
        os.makedirs(savePath)


def saveOutputFileCsv(path: str, fileName: str, data: list):
    """
    保存输出文件
    :param data:
    :param path:
    :param fileName:
    :return:
    """
    # resolve the encoding problem

    timeStr = time.strftime("_%Y%m%d_%H%M%S", time.localtime())
    savePath = os.path.join(path, fileName + timeStr + ".csv")
    with open(savePath, "w",
              encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return savePath


def readXls(xlsPath, startRow=1):
    """
    读取xls文件 返回数据
    :param xlsPath:
    :param startRow:
    :return: [[], [], []]
    """
    # read the xls file and return the data with list type by openpyxl
    wb = openpyxl.load_workbook(xlsPath)
    sheet = wb.active
    # data = []
    # for row in sheet.rows:
    #     data.append([cell.value for cell in row])
    # use simple way to get the data
    wb.close()
    # return [list(i) for i in sheet.iter_rows(min_row=startRow, values_only=True)]
    startRow = startRow - 1 if startRow > 1 else 0
    return list(sheet.values)[startRow:]


def readContact(contactXlsPath: str) -> dict:
    """
    读取供应商联系人数据
    :param contactXlsPath:
    :return: {
        "供应商1": {contactMail, contPartner, staffPartner: "王某"},
    "供应商2": {信息, partner: "李某"},
        }
    """
    contactRawData = readXls(contactXlsPath, startRow=2)
    contactData = {}
    for row in contactRawData:
        contactData.update({
            row[contactComCol]: {
                "contactMail": row[contactMailCol],
                "contPartner": row[contPartnerCol],
                "staffPartner": row[staffPartnerCol],
            }
        })
    return contactData


def readNotReceive(notReceiveXlsPath) -> dict:
    """
    读取未接收数据
    :param notReceiveXlsPath:
    :return: {供应商: {项目: 内容, 项目: 内容...},
             供应商: {项目: 内容, 项目: 内容...}}
    """
    notReceiveRawData = readXls(notReceiveXlsPath, startRow=0)
    header = notReceiveRawData[0]
    content = notReceiveRawData[1:]
    notReceiveData = {}
    for row in content:  # 对每一行数据进行处理
        supplyCom = row[supplyCompanyCol]
        if row[supplyCompanyCol] not in notReceiveData:
            notReceiveData.update({supplyCom: []})
        eachData = {}
        for eachDataCol in mailContentCols:
            # 添加每行的每一个相关数据
            eachData.update({
                header[eachDataCol]: row[eachDataCol]
            })
        notReceiveData[supplyCom].append(eachData)
    return notReceiveData


def readStaff(staffXlsPath) -> dict:
    """
    读取员工数据 及其邮箱
    :param staffXlsPath:
    :return: {"张三": {"mail": ""},
                "李四": {}, ]
    """
    data = readXls(staffXlsPath, startRow=2)
    staffData = {}
    for row in data:
        staffData.update({
            row[staffNameCol]: {
                "mail": row[staffMailAccCol],
                "psd": row[staffMailPsdCol],
                "server": row[staffMailServerCol],
                "port": row[staffMailPortCol],
            }
        })
    return staffData


def updateFailedRecords(failedRecords: list, data: dict, reason: str, comKey: str, comValue: str):
    for detailItem in data[comKey]:
        failedRecords.append([comValue] + list(detailItem.values()) + [reason])


def mergeContact(contactData, notReceiveData, staffsData) -> list:
    """

    :param staffsData:
    :param contactData: 联系人数据
    :param notReceiveData: 未接收数据原文(可能删减)
    :return: [
    { "name": "张三", "mail": "g@..com", "psd": "123456",
        "data": [ {}, {}, {} ] },
    }
    ]
    """
    trySendData = []
    # 添加表头
    headers = notReceiveData[list(notReceiveData.keys())[0]][0].keys()
    failedRecords = [["供应商"] + list(headers) + ["运行结果"]]

    def isExcludeData():
        # 1. 联系人表
        if com not in contactData:
            updateFailedRecords(failedRecords, notReceiveData,
                                "联系人表中没有该供应商",
                                comKey=com, comValue=com)
            return True
        if not contactData[com]["staffPartner"]:
            updateFailedRecords(failedRecords, notReceiveData,
                                "联系人表中对接人为空",
                                comKey=com, comValue=com)
            return True

        # 2. 员工表
        staffPartner = contactData[com]["staffPartner"]
        staffMail = staffsData[contactData[com]["staffPartner"]]["mail"]
        staffPsd = staffsData[contactData[com]["staffPartner"]]["psd"]
        staffServer = staffsData[contactData[com]["staffPartner"]]["server"]
        staffPort = staffsData[contactData[com]["staffPartner"]]["port"]
        if staffPartner not in staffsData:
            # failedRecords.append(formatXlsData(com, notReceiveData, "联系人表中的对接人不在员工邮件表中"))
            updateFailedRecords(failedRecords, notReceiveData,
                                f"联系人表中的对接人({staffPartner})不在员工邮件表中",
                                comKey=com, comValue=com)
            return True
        if not staffMail:
            # failedRecords.append(formatXlsData(com, notReceiveData, "联系人表中的对接人的邮箱为空"))
            updateFailedRecords(failedRecords, notReceiveData,
                                f"联系人表中的对接人({staffPartner})的邮箱为空",
                                comKey=com, comValue=com)
            return True
        if not staffPsd:
            # failedRecords.append(formatXlsData(com, notReceiveData, "联系人表中的对接人的邮箱密码为空"))
            updateFailedRecords(failedRecords, notReceiveData,
                                f"联系人表中的对接人({staffPartner})的邮箱密码为空",
                                comKey=com, comValue=com)
            return True
        if not staffServer:
            # failedRecords.append(formatXlsData(com, notReceiveData, "联系人表中的对接人的邮箱服务器为空"))
            updateFailedRecords(failedRecords, notReceiveData,
                                f"联系人表中的对接人({staffPartner})的邮箱服务器为空",
                                comKey=com, comValue=com)
            return True
        if not staffPort:
            # failedRecords.append(formatXlsData(com, notReceiveData, "联系人表中的对接人的邮箱端口为空"))
            updateFailedRecords(failedRecords, notReceiveData,
                                f"联系人表中的对接人({staffPartner})的邮箱端口为空",
                                comKey=com, comValue=com)
            return True
        return False

    for com in notReceiveData:
        if isExcludeData():
            continue
        # 以上都满足则添加到待发送数据中
        partner = contactData[com]["staffPartner"]
        mail = staffsData[partner]["mail"]
        psd = staffsData[partner]["psd"]
        trySendData.append(
            {
                "staffName": partner,
                "staffMail": mail,
                "staffPsd": str(psd),
                "staffMailServer": staffsData[partner]["server"],
                "staffMailPort": staffsData[partner]["port"],
                "contactCom": com,
                "contPartner": contactData[com]["contPartner"],
                "contactMail": contactData[com]["contactMail"],
                "data": notReceiveData[com],  # 里面是一个列表，看做一个整体
            }
        )

    return [failedRecords, trySendData]


def getContentAtMail(eachStaff):
    """
    生成邮件内容
    可选参数: "selfName", "mail", "psd", "contactCom", "contactMail", "data"
    :param eachStaff:
    :return:
    """
    data = eachStaff["data"]
    staffName = eachStaff["staffName"]
    contactCom = eachStaff["contactCom"]
    contactPartner = eachStaff["contPartner"]

    tableCodeHeader = f'<tr style="' \
                      f'background-color:#3592c4; ' \
                      f'font-weight:bold; ' \
                      f'color: #ffffff">'
    for eachKey in data[0].keys():
        tableCodeHeader += f"<th>{eachKey}</th>"
    tableCodeHeader += f"</tr>"

    tableCodeDetail = f""
    for each in data:
        tableCodeDetail += "<tr>"
        for eachKey in each.keys():
            tableCodeDetail += f"<td>{each[eachKey]}</td>"
        tableCodeDetail += "</tr>"
    tableCodeDetail += "</table>"

    content = f"""
    <p>尊敬的{contactPartner}，您好！</p>
    <p>您在公司({contactCom})负责的以下{(len(data))}个订单仍未接收，请您核实并处理，谢谢！</p>
    <table border="1" cellspacing="0" cellpadding="0" width="100%">
        {tableCodeHeader}
        {tableCodeDetail}
        
    </table>
    <br>
    <p>如有疑问，请联系对接人:{staffName}。</p>
    
    </table>
    """
    return content
    # return f"您好，我是{name}的IPA数智员工," \
    #        f"经检查发现由我负责跟进的单位:{contactCom}中，" \
    #        f"有以下{len(data)}条未接收的数据，而您是负责人，请及时推进处理，谢谢：<br>" + \
    #        detail


def sendMail(sendMailAdd, sendMailPsd,
             toMailAdd, content, subject="未接收数据通知",
             smtpServer="smtp.163.com", port=465):
    if not sendMailAdd:
        return "发送邮箱为空"
    if not sendMailPsd:
        return "发送邮箱密码为空"
    try:
        # 发送html邮件
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = Header(subject, 'utf-8')
        msg['To'] = Header(toMailAdd, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        server = smtplib.SMTP_SSL(smtpServer, port)
        server.login(sendMailAdd, sendMailPsd)
        server.sendmail(sendMailAdd, toMailAdd, msg.as_string())
        server.quit()
        res = f"发送成功, {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
    except Exception as e:
        res = f"发送失败，原因：{e}"
    return res


def sendMailBatch(mergedContactData):
    """
    通过读取联系人及联系人数据, 使用对应员工的邮件发送
    :param mergedContactData: 供应商联系人及未接收数据
    :return:
    """
    sendResult = []
    for eachStaff in mergedContactData:
        content = getContentAtMail(eachStaff)
        res = sendMail(eachStaff["staffMail"], eachStaff["staffPsd"],
                       eachStaff["contactMail"], content,
                       subject="未接收数据通知",
                       smtpServer=eachStaff["staffMailServer"],
                       port=eachStaff["staffMailPort"])
        # sendResult.append([
        #     formatXlsData(eachStaff["toCom"], eachStaff["data"], res)
        # ])
        updateFailedRecords(sendResult, eachStaff, res,
                            comKey="data", comValue=eachStaff["contactCom"])
        # colorful res， if res is success, then green, else red \33[32m
        res = f"\33[32m{res}\33[0m" if "成功" in res else f"\33[31m{res}\33[0m"
        print(f"{eachStaff['staffName']}({eachStaff['staffMail']})"
              f"\n\t发送给{eachStaff['contactCom']:10}的邮件结果"
              f"\n\t{res}")
    return sendResult


def main(contactXlsPath: str, notReceiveXlsPath: str,
         staffXlsPath: str, outputFolderPath: str):
    # 参数检查
    paramsCheck(contactXlsPath, notReceiveXlsPath, staffXlsPath, outputFolderPath)
    notReceiveData = readNotReceive(notReceiveXlsPath)
    contactData = readContact(contactXlsPath)
    staffData = readStaff(staffXlsPath)
    [noSendRecords, trySendData] = mergeContact(contactData, notReceiveData, staffData)
    sendResult = sendMailBatch(trySendData)

    # 生成输出文件
    outputCSVPath = saveOutputFileCsv(outputFolderPath, "contactData", noSendRecords + sendResult)
    print("\n输出文件已生成", outputFolderPath, outputCSVPath)


[supplyCompanyCol, mailContentCols,
 contactComCol, contPartnerCol, contactMailCol, staffPartnerCol,
 staffNameCol, staffMailAccCol, staffMailPsdCol, staffMailServerCol, staffMailPortCol] = \
  colLtrParamsConvert(
    # 未接收数据表
    supplyCompany="F",  # 供应商名
    mailContents=["A", "B", "C",
                  "D", "E", "F",
                  ],  # 未接收数据表中的邮件内容

    # 供应商联系人表
    contactCom="A",  # 供应商公司名列
    contPartner="C",  # 负责跟进人列
    contactMail="E",  # 供应商联系人邮箱列
    staffPartner="G",  # 负责跟进人列

    # 员工邮箱数据
    staffName="A",
    staffMailAcc="B",
    staffMailPsd="C",
    staffMailServer="D",
    staffMailPort="E",
)

# contactXls = ".\input\供应商信息测试.xlsx"
# notReceiveXls = ".\input\未开单测试.xlsx"
# staffXls = ".\input\员工邮箱数据.xlsx"
# outputPath = ".\output"

# from pprint import pprint
# pprint(readContact(contactXls))
# pprint(readStaff(staffXls))
# pprint(readNotReceive(notReceiveXls))
# saveOutputFileCsv(outputPath, "contactData.csv", [[1, 2, 3], [4, 5, 6]])
main(contactXls, notReceiveXls, staffXls, outputPath)
