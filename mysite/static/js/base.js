/* 全局基础交互脚本*/
document.addEventListener('DOMContentLoaded', () => {
    /* ------------------------------------------------------------------------
       1. 底层环境光侦听引擎 (Global Environment Light Tracking)
       ------------------------------------------------------------------------ */
    const rootElement = document.documentElement;
    
    window.addEventListener('mousemove', (event) => {
        // 使用 requestAnimationFrame 优化性能，确保动画与屏幕刷新率同步
        requestAnimationFrame(() => {
            rootElement.style.setProperty('--mouse-x', event.clientX + 'px');
            rootElement.style.setProperty('--mouse-y', event.clientY + 'px');
        });
    }, { passive: true });


    /* ------------------------------------------------------------------------
       2. 导航栏动态滚动反馈 (Header Scroll Dynamics)
       ------------------------------------------------------------------------ */
    const headerElement = document.querySelector('.header-academic');
    
    // 安全屏障：只有当当前页面真正存在导航栏时，才挂载滚动监听
    if (headerElement) {
        const handleScrollDynamics = () => {
            // 超过 20px 阈值时触发 CSS 中的光学晕染
            if (window.scrollY > 20) {
                headerElement.classList.add('scrolled-glow');
            } else {
                headerElement.classList.remove('scrolled-glow');
            }
        };

        // 绑定滚动事件，passive: true 大幅提升页面滚动时的丝滑度
        window.addEventListener('scroll', handleScrollDynamics, { passive: true });
        
        // 页面刚加载时立刻执行一次，防止用户在页面半中央刷新时导航栏失去样式
        handleScrollDynamics();
    }

});