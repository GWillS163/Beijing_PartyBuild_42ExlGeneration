//  Github: GWillS163
//  User: 駿清清
//  Date: 21/11/2022
//  Time: 16:31
// 所有关键词按顺序输入

detailErpData = []
// ex. 有源需求单
let title = document.getElementById("showTitle").innerText
detailErpData.push(title.split("-")[0].trim())

keywordList = [
    // ex. 上市公司
    "misBodyName",
    // ex. 资本类
    "expenditureClassName",
    // ex. 刘霖
    "orderUserName",
    // ex. CMBJ-2018-00024098-CG-00001790
    "contractCode",
    // ex. 中国移动2018年至2019年PTN设备（华为扩容部分）集中采购框架协议（设备）
    "contractName",
    // ex. 30
    "leadTime",
    // ex. 华为技术有限公司
    "vendorName"
]
for (let i = 0; i < keywordList.length; i++) {
    value = document.getElementById(keywordList[i]).value
    detailErpData.push(value)
}


// process the keywordValue in table
matchTable = document.getElementsByTagName("table")[1].children[1]

firstRow = matchTable.children[0].children
// needsPerson  & needsPersonDepartment
detailErpData.push(firstRow[4].innerText ) // ex. 卓明
detailErpData.push(firstRow[2].innerText ) // ex. 大兴分公司.建设中心

// 找到订单员： 最后一个"订单管理员确认"
let orderPerson;
let orderPersonDepart;
let lastConfirmSeqNum;
for (let i = 0; i < matchTable.children.length; i ++ ){
    if (matchTable.children[i].children[1].innerText === "订单管理员确认") {
        lastConfirmSeqNum = i
    }
}
// ex. 订单管理员确认
orderPerson = matchTable.children[lastConfirmSeqNum].children[1].innerText
// ex. 供应链管理部.订单中心
orderPersonDepart = matchTable.children[lastConfirmSeqNum].children[2].innerText
detailErpData.push(orderPerson)
detailErpData.push(orderPersonDepart)

// print the keywordValue iteratively
for (let i = 0; i < detailErpData.length; i++) {
    console.log(detailErpData[i])
}

// export keywordValue
