# the script is for work

keywordDict = {
    '王秋实': ['小号&&v网', '物联网', '企业宽带', 'IMS', '铁通固话', '集团客户'],
    '肖 敏': ['开户', '销户', '报停', '一证五号', '过户', '动感地带', '全球通', '激活', '全网一证多号', '断卡'],
    '付大为': ['能力开放', '能开', 'BIP&&报错', 'BIP&&返回'],
    '杨春雨': ['资费&&变更', '套餐', '互斥&&报错'],
    '姜 欣': ['携号转网', '携转', '垃圾短信', '骚扰电话', '加解黑'],
    '郭 洋': ['企业视频彩铃', '专线', '云mas', 'BBOSS', '全网客户关怀'],
    '张圣春': ['一号多终端', '和多号', '手机报', '咪咕', '飞信', '139邮箱', '漫游移动气象'],
    '温娟娟': ['补换卡', '远程写卡', '5785', '网上售卡&&订单&&状态'],
    '杨靖源': ['电子工单', '受理凭证', '8965', '空中充值&&注销', '不承认办理&&电子单', '渠道&&账户&&合同编号&&不匹配', '组织树&&账户&&合同编号&&不匹配'],
    '姜 洋': ['固定费收取', '星级', '有余额被停机', '缴费未开机', '集团信控', '集团账单', '欠费黑名单', '催缴短信'],
    '赵 娜': ['融合&&宽带', '流量共享', '亲情网', '幸福家庭'],
    '范子龙': ['宽带&&卡单', '宽带&&改单', '宽带&&IPTV', '智能组网', '和家固话', '家庭安防', 'CPE', '宽带&&预接入', '宽带&&变更', '宽带&&短信'],
    '吕泽江': ['赠费', '积分', '5G金币', '话费卷', '营销活动', '流量赠送', '语音赠送'],
    '李佳慧': ['购机', '购终端', '终端营销', '退机', '信用购', '后台查询&&串号'],
    '姜桂华': ['通话费', '语音共享', '短信共享', '优惠分区', '内容计费类'],
    '周冠岑': ['发票', '普票', '专票', '缴费', '统付', '转账', '退费', '托收', '资质', '未到账'],
    '赵松琦': [], '康馨匀': ['权益', '权益&&领取', '领取', '权益&&发放'],
    '刘 昕': ['短信延迟', '提醒延迟', '上网费', '小区流量', '封顶', '日租卡', '定向流量', '流量共享', '结转'],
    '张 希': ['彩铃', '来电显示', '来电提醒', '短信炸弹防护', '高频防骚扰拦截', '城市名片', 'Volte', '呼叫转移',
            '开机', '停复机', '国际漫游', '呼转呼叫', '主叫隐藏', '限速', '来显', '呼转',
            '关机', '手机上网', '上网功能', '转移', '漫游直拨', '停机', '4G上网', '集团小号', '主被叫', '2/3G', '23G', '短信应急防护',
            'ENUMDNS', 'SIFC']}


# the Core of the program
def get_str_lst(row_text):
    forStuff = None
    break_flag = False
    row_text = row_text.lower()
    for stuff, kw in keywordDict.items():
        for keyW in kw:
            # compatible with upper and lower case
            keyW = keyW.lower()
            if "&&" in keyW:
                keyWs = keyW.split("&&")
                # demonstrate the keyW all in the title
                if all(keyW in row_text for keyW in keyWs):
                    forStuff = stuff
                    break_flag = True
                    break
            elif keyW in row_text:
                forStuff = stuff
                break_flag = True
                break

        if break_flag:
            break
        return forStuff


if __name__ == '__main__':
    # test the function by use the above stuff_with_keyword dict, the result is key, value is the person who is the key
    # print(get_str_lst("企业视频彩铃"))
    for person, keywords in keywordDict.items():
        for keyword in keywords:
            get_stuff = get_str_lst(keyword)
            if not get_stuff == person:
                print(get_stuff == person, end=" ")
                print(get_stuff, keyword, person)


