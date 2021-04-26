const totalAsset = document.querySelector("#totalAsset");
const check = document.querySelector(".check");

const chckTest = document.querySelector('.chckTest');

function ShowBoolean(){
  console.log(totalAsset.checked);
}

function init(){
  console.log(totalAsset.checked);
  check.addEventListener('click',ShowBoolean)

  check.addEventListener('click', ()=>{
    console.log(chckTest.val);
  });
}

init();
