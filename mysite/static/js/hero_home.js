document.addEventListener('DOMContentLoaded', () => {
    
    /* ==========================================================================
       1. 核心首屏轮播引擎 (Hero Carousel Engine)
       ========================================================================== */
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
    let timer = null;

    const showSlide = (index) => {
        slides.forEach(s => s.classList.remove('active'));
        dots.forEach(d => d.classList.remove('active'));
        slides[index].classList.add('active');
        dots[index].classList.add('active');
        currentIndex = index;
    };

    const nextSlide = () => {
        let next = (currentIndex + 1) % slides.length;
        showSlide(next);
    };

    const startTimer = () => {
        timer = setInterval(nextSlide, 5000);
    };

    dots.forEach((dot, idx) => {
        dot.addEventListener('click', () => {
            clearInterval(timer);
            showSlide(idx);
            startTimer();
        });
    });

    if (slides.length > 0) startTimer();

    /* ==========================================================================
       2. 视区交叉观察器与入场动画 (Intersection Observer for Entrance Animations)
       ========================================================================== */
    // 选中所有需要执行丝滑入场动画的业务容器
    const animatedSections = document.querySelectorAll(
        '.education-section, .events-section, .research-section, .news-section, .media-section'
    );

    // 配置交叉观察器：当容器有 15% 的面积进入浏览器可视区域时，判定为触发
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15 
    };

    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // 如果元素进入了视口
            if (entry.isIntersecting) {
                // 1. 解除动画暂停状态，开始播放从底部上浮的动画
                entry.target.style.animationPlayState = 'running';
                
                // 2. 动画触发后，立即取消对该元素的观察，确保动画只播放一次，不消耗多余性能
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // 初始化引擎：在页面刚加载时，先强制暂停所有容器的 CSS 动画，并将它们交给观察器监控
    animatedSections.forEach(section => {
        // 利用 JS 动态暂停，确保那些被 JS 阻断的用户（极少数）依然能看到通过 CSS 直接渲染的静态画面
        section.style.animationPlayState = 'paused';
        sectionObserver.observe(section);
    });

});