// Click the exactly one record  点击唯一一条记录
let searchData = document.getElementsByTagName("tr")
// find the SeqNumber of ERPCode in the table  找到表格中ERPCode的序号
let erpCol = -1 ; // 24
let header = searchData[0].children
for (let i = 0; i < header.length; i++) {
    if (header[i].innerText === "ERP订单号") {
        erpCol = i
        console.log("erpCol: " + erpCol)
        break;
    }
}

// recognize the exactly one record  识别唯一一条记录
let isExactlyMatched = false;
// 0 直接遍历:
for (i = 1; i < searchData.length; i++) {
    let erpColText = searchData[i].children[erpCol].innerText;
    console.log(erpColText, erpCode);
    if (erpColText === erpCode) {
        searchData[i].children[1].children[0].click()
        isExactlyMatched = true
        console.log("found exactly record row:", i)
        break;
    }
}

// 1 switch 设计器内会语法报错
// switch (searchData.length) {
//     case 1:
//         console.log("No exactly record found");
//         break;
//     case 2:
//         console.log("Exactly one record found");
//         searchData[1].children[erpCol].click()
//         isExactlyMatched = true;
//         break;
//     case 3:
//     default:// 多条记录， 但是只有一条是完全匹配的
//         for (i = 1; i < searchData.length; i++) {
//             let erpColText = searchData[i].children[erpCol].innerText;
//             console.log(erpColText, erpCode);
//             if (erpColText === erpCode) {
//                 searchData[i].children[1].children[0].click()
//                 isExactlyMatched = true
//                 console.log("found exactly record row:", i)
//                 break;
//             }
//         }
//         break;
// }

// 2 改用if语句
// if (searchData.length === 2) {
//     console.log("Exactly one record found");
//     searchData[1].children[erpCol].click()
//     isExactlyMatched = true;
// } else {
//     if (searchData.length === 1) {
//         console.log("No exactly record found");
//     } else {
//         // 多条记录， 但是只有一条是完全匹配的
//         for (i = 1; i < searchData.length; i++) {
//             let erpColText = searchData[i].children[erpCol].innerText;
//             console.log(erpColText, erpCode);
//             if (erpColText === erpCode) {
//                 searchData[i].children[1].children[0].click()
//                 isExactlyMatched = true
//                 console.log("found exactly record row:", i)
//                 break;
//             }
//         }
//     }
// }

// export the result : isExactlyMatched