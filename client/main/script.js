$(document).ready(function(){
    $('.slide_menu').slick({
        slidesToShow: 6,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1500,
        arrows: false,
        dots: false,
        pauseOnHover: false,
        responsive: [{
            breakpoint: 768,
            settings: {
                slidesToShow: 4
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 3
            }
        }]
    });
});

const itm = document.querySelector('.keyword-wrapper');
var i=0;
setInterval(() => {
    if(i > 2){
        i = 0;
        itm.setAttribute('style', `margin-top: -${i*100}px; transition: none;`)
    }else{
        itm.setAttribute('style', `margin-top: -${i*100}px; transition: all .3s;`)
    }
    i++;
}, 2000);