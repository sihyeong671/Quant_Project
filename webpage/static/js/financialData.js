const totalAsset = document.querySelector("#totalAsset");
const check = document.querySelector(".check");

function ShowBoolean(){
  console.log(totalAsset.checked);
}

function init(){
  console.log(totalAsset.checked);
  check.addEventListener('click',ShowBoolean)
}

init();
