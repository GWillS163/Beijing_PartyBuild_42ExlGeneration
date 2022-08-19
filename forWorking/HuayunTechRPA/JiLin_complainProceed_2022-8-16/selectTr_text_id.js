/*

 * # Author : Github: @GWillS163
 * # Time: $(Date)
 */



var lst = document.querySelectorAll(".mini-grid-row")
// define a result array
var rowsResult = []

// select all
for (var i = 0; i < lst.length; i++){
    ele = lst[i].querySelectorAll("td")[5];
    // add id and text to result array
    rowsResult.push({
        id: ele.id,
        text: ele.innerText
    })
}
console.log(rowsResult)


// 87$cell$7 20220812153427X667828837-10312097519-服务类→业务查询→其它

