$(function () {
    var ww,wh;
    var we = window, wa = 'inner';
    if (!('innerWidth' in window )) {
        wa = 'client';
        we = document.documentElement || document.body;
    }
    ww = we[ wa+'Width' ], wh = we[ wa+'Height' ];
    // return { width : we[ wa+'Width' ] , height : we[ wa+'Height' ] };
    var PC = ww > 1025,
        mobile = ww <= 1024,
        mobile_s = ww <= 768,
        winWidth = ww,
        winHeight = wh;

    $(".banner").addClass("on");

    var banner = new Swiper('.banner', {
        loop: true,
        speed: 1e3,
        spaceBetween: 0,
        slidesPerView: 1,
        autoplay: {
            delay: 5000,
            stopOnLastSlide: false,
            disableOnInteraction: false,
        },

        pagination:{
            el:'.banner .page',
            clickable :true,
            bulletActiveClass:'active',
        },
        on: {
            slideChangeTransitionStart : function(swiper){
                var swiper = this;

                // 判断swiper-slide-active是否有视频
                if($(".banner .swiper-slide-active video").length>0){
                    console.log(1)
                    // 停止自动切换
                    swiper.autoplay.stop();
                    // 动态增加id
                    setTimeout(function(){
                        swiper.autoplay.stop();
                        $(".banner .swiper-slide-active video").attr("id","video_01");

                        var _video=document.getElementById("video_01");

                        // 播放视频
                        _video.play();
                        // 切换后重新播放视频
                        _video.currentTime = 0;
                        // 静音
                        _video.volume = 0;
                        // 监听视频播放结束
                        _video.addEventListener('ended', function () {
                            swiper.slideNext();
                            //重新开始轮播banner
                            swiper.autoplay.start();
                        });
                    }, 10);
                }
            },
            slideChangeTransitionEnd: function(swiper){
                //动态移除id
                setTimeout(function(){
                    $(".banner .swiper-slide-active video").attr("id","");
                }, 10);
            },
        }
    })


    var swiper1 = new Swiper('.list1w', {
        loop: true,
        speed: 1e3,
        spaceBetween: 10,
        slidesPerView: 1,
        autoplay: {
            delay: 5000,
            stopOnLastSlide: false,
            disableOnInteraction: false,
        },
        navigation: {
            prevEl: '.index-s2 .prev',
            nextEl: '.index-s2 .next',
        },
        breakpoints:{
            1025:{
                spaceBetween: 42,
                slidesPerView: 4,
            },
            769:{
                spaceBetween: 20,
                slidesPerView: 2,
            }
            ,481:{
                spaceBetween: 10,
                slidesPerView: 2,
            }
        }

    })


    var swiper2 = new Swiper('.list2w', {
        //loop: true,
        speed: 1e3,
        spaceBetween: 10,
        slidesPerView: 1,
        autoplay: {
            delay: 5000,
            stopOnLastSlide: false,
            disableOnInteraction: false,
        },

        on:{
            slideChangeTransitionStart: function(){
                $('.list_box5 li').eq(this.activeIndex).addClass('active').siblings().removeClass('active')
            },
        }

    })

    $('.list_box5 li').on("mouseenter",function (){
        var i = $(this).index()
        $(this).addClass('active').siblings().removeClass('active')
        swiper2.slideTo(i)
    })

    var swiper3 = new Swiper('.list3w', {
        loop: true,
        speed: 1e3,
        spaceBetween: 10,
        slidesPerView: 2,
        autoplay: {
            delay: 5000,
            stopOnLastSlide: false,
            disableOnInteraction: false,
        },
        breakpoints:{
            1025:{
                spaceBetween: 50,
                slidesPerView: 5,
            },
            769:{
                spaceBetween: 20,
                slidesPerView: 4,
            }
            ,481:{
                spaceBetween: 10,
                slidesPerView: 2,
            }
        },
        setTransition: function(c) {
            for (var e = 0; e < this.slides.length; e++)
                this.slides.eq(e).transition(c)
        }

    })

})