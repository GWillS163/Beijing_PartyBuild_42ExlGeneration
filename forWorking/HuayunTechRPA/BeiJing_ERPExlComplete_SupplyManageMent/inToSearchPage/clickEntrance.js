// find all a tag
let allATag = document.getElementsByTagName("a")

for (i=0; i< allATag.length; i++){
    if (allATag[i].innerText == "订单全流程跟踪"){
        allATag[i].click();
        console.log("found");
        console.log(allATag[i].innerText)
    }
}