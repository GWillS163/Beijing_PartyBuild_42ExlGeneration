// input  输入参数
erpCode = "2019040170"

// Fill condition 填写查询条件
erp = document.getElementById("erpSegment")
erp.value = erpCode

// Clear the Date filter  清空日期过滤条件
clearNeeds = [5,6]
for (i = 0; i < clearNeeds.length; i++) {
    document.getElementsByClassName("input-group-addon")
        [clearNeeds[i]]
        .click()
    // Click the "Clear" button
    // Method 1
    document.getElementsByClassName("clear")[0].click()
    // Method 2
    // allClear = document.getElementsByClassName("clear")
    // for (i=0; i< allClear .length; i++){
    //     allClear[i].click()
    // }
}

// Click the "Search" button  点击查询按钮
document.getElementsByClassName("btn btn-warning btn-sm")[0].click()

// wait for the page to load  等待页面加载

