const menu = document.querySelector(".menu") 
const sideBar = document.querySelector(".side_bar");
const loginBtn = document.querySelector(".login");
const loginShape = document.querySelector(".login_shape");
const closeBtn = document.querySelector(".login_close");
const loginBG = document.querySelector(".login_bg");

// 사이드바 열기
function clickMenu(){
  sideBar.classList.add("showing_menu");
}

// 사이드바 닫기
function clickSideBar(){
  sideBar.classList.remove("showing_menu");
  console.log('ds');
}

// 로그인 창 열기
function clickLoginBtn(){
  loginShape.classList.add("showing_login_shape");
}

//로그인 창 닫기
function closeLoginScreen(){
  loginShape.classList.remove("showing_login_shape");
}

function init(){
  menu.addEventListener("click",clickMenu);
  sideBar.addEventListener("click", clickSideBar);
  loginBtn.addEventListener("click", clickLoginBtn);
  closeBtn.addEventListener("click", closeLoginScreen);
  
  loginBG.addEventListener('click', closeLoginScreen);
}
init();