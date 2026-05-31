/**
 * 导航栏动态滚动效果引擎
 * 职责：侦听视窗滚动，动态挂载光学晕染类名
 */
(function() {
    'use strict';

    const initHeaderScroll = () => {
        const headerElement = document.querySelector('.header-academic');
        
        // 容错处理：确保页面上存在导航栏容器
        if (!headerElement) return;

        const handleScrollDynamics = () => {
            // 设置 20px 的偏移阈值，增加微小的滚动死区防止抖动
            if (window.scrollY > 20) {
                headerElement.classList.add('scrolled-glow');
            } else {
                headerElement.classList.remove('scrolled-glow');
            }
        };

        // 使用 passive 属性优化移动端滚动性能
        window.addEventListener('scroll', handleScrollDynamics, { passive: true });
        
        // 初始检查：防止用户刷新页面后处于滚动位置但导航栏未渲染样式
        handleScrollDynamics();
    };

    // 确保 DOM 完全加载后再执行逻辑
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeaderScroll);
    } else {
        initHeaderScroll();
    }
})();