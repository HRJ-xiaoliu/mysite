

$(function (){

    $(".search_btn").on("click", function() {
        $(".search-dialog-box").toggleClass("on")
    });
    $(".search-dialog-box .pub-close").on("click", function() {
        $(".search-dialog-box").removeClass("on")
    });
    /*site-menu*/

    $('#openBtn').click(function (){
        $('.site-menu').toggleClass('site-menu-is-open')
        $('.header').toggleClass('active')
        $(this).toggleClass("active");
    })
    /*$('.site-menu-close').click(function (){
        $('.site-menu').removeClass('site-menu-is-open')
    })*/


    /*wap*/
    $('.navbtnm').click(function(){
        $('html,body').toggleClass('navShow')
    });
    //移动端导航
    $(".list_box_nav_mobile>li i").click(function(){
        $(this).parents(".list_box_nav_mobile>li").find(".list").slideToggle();
        $(this).parents(".list_box_nav_mobile>li").toggleClass("on1");
        $(this).parents(".list_box_nav_mobile>li").siblings().find(".list").slideUp();
        $(this).parents(".list_box_nav_mobile>li").siblings().removeClass("on1");
    });
    /*$("#m_nav .sub").hide();
    $("#m_nav .void").click(functon(){
        $(this).children(".sub").slideToggle(); //展开
    });*/
    $("#nav_btn_box").click(function(){
        $("#nav_btn_box .point").toggleClass("on");
        $("#nav_btn_box").toggleClass("on");
        $("#m_nav").toggleClass("act");
        $(".nav_mask").fadeToggle();
    });

    $(".nav_mask").click(function(){
        $("#nav_btn_box .point").removeClass("on");
        $("#nav_btn_box").removeClass("on");
        $(this).fadeToggle();
        $(".nav_btn_box").removeClass("act");
        $("#m_nav").removeClass("act");
    })

    $("#m_nav .close").click(function(){
        $("#nav_btn_box .point").removeClass("on");
        $("#nav_btn_box").removeClass("on");
        $(".nav_btn_box").removeClass("act");
        $("#m_nav").removeClass("act");
        $(".nav_mask").fadeOut();
    });



    $(" #bnt_sub_nav").click(function() {
        $(this).toggleClass("on");
        $("#sub_nav_content").stop().slideToggle();
    })


    $("#sub_nav_content dt i").click(function(){
        $(this).next("ul").slideToggle();
        $(this).parents("#sub_nav_content dt").siblings().find("ul").slideUp();
    });

    /// 二级页面 移动端左侧三级导航 展示
    $(".leftNav .box h3 i").click(function() {
        $(this).parents('.box').stop().toggleClass("on").siblings(".box").removeClass("on");
        $(this).parents('.box').children(".s-link").stop().slideToggle(300).parents('.box').siblings().find(".s-link").stop().slideUp();
    })
})