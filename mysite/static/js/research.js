/**
 * 学术研究成果页 - 终极交互与动画引擎
 * 职责：严格单选路由、手风琴摘要互斥、视差瀑布流显影
 */

document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // 动态注入瀑布流需要的 CSS，保持样式表的纯净
    const styleSheet = document.createElement("style");
    styleSheet.innerText = `
        .research-item-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease, border-color 0.4s ease;
        }
        .research-item-card.is-revealed {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(styleSheet);

    /* ==========================================================================
       1. 瀑布流显影引擎 (Intersection Observer)
       ========================================================================== */
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -30px 0px',
        threshold: 0.05
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const delay = target.getAttribute('data-delay') || 0;
                
                setTimeout(() => {
                    target.classList.add('is-revealed');
                }, delay);

                // 触发后解绑，释放浏览器性能
                observer.unobserve(target);
            }
        });
    }, observerOptions);

    // 为指定面板内的卡片编排错落有致的出现时间
    const initCardsReveal = (container) => {
        const cards = container.querySelectorAll('.research-item-card');
        cards.forEach((card, index) => {
            card.classList.remove('is-revealed'); 
            card.setAttribute('data-delay', index * 80); // 每张卡片延迟 80ms，形成钢琴键般的瀑布流
            // 强制重绘，重置状态
            void card.offsetWidth;
            revealObserver.observe(card);
        });
    };

    /* ==========================================================================
       2. 全局选项卡：绝对排他路由 (Strict Tab Switching)
       ========================================================================== */
    window.switchResearchTab = function(panelId, btn) {
        // A. 全局清场：强制关闭所有面板和导航高亮
        document.querySelectorAll('.research-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.research-nav-item').forEach(b => b.classList.remove('active'));
        
        // B. 精准激活
        const targetPanel = document.getElementById(panelId);
        if (targetPanel) {
            targetPanel.classList.add('active');
            // 为新唤醒的面板重新执行瀑布流动画
            initCardsReveal(targetPanel);
        }
        if (btn) {
            btn.classList.add('active');
        }
        
        // C. 平滑归位
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    /* ==========================================================================
       3. 摘要手风琴：严格互斥展开逻辑 (Strict Accordion)
       ========================================================================== */
    window.toggleAbstract = function(btn, defaultText, activeText) {
        const card = btn.closest('.research-item-card');
        const panel = card.querySelector('.research-abstract-panel');
        const textSpan = btn.querySelector('span');
        const isCurrentlyExpanded = btn.classList.contains('expanded');
        
        // A. 互斥防御：瞬间收起屏幕上所有正在展开的【其他】摘要面板
        document.querySelectorAll('.research-abstract-panel').forEach(p => {
            if (p !== panel) p.classList.remove('visible');
        });
        document.querySelectorAll('.toggle-abstract-btn').forEach(b => {
            if (b !== btn) {
                b.classList.remove('expanded');
                // 恢复其他按钮的文字状态
                const otherSpan = b.querySelector('span');
                if (otherSpan && otherSpan.textContent.includes('收起')) {
                    if(b.closest('#proj-panel')) otherSpan.textContent = '项目详情';
                    else if(b.closest('#patent-panel')) otherSpan.textContent = '专利说明';
                    else otherSpan.textContent = '阅读摘要';
                }
            }
        });
        
        // B. 处理当前点击的操作
        if (!isCurrentlyExpanded) {
            btn.classList.add('expanded');
            panel.classList.add('visible');
            if(textSpan) textSpan.textContent = activeText || '收起内容';
        } else {
            btn.classList.remove('expanded');
            panel.classList.remove('visible');
            if(textSpan) textSpan.textContent = defaultText || '阅读详情';
        }
    };

    // ==========================================================================
    // 4. 初始化引擎
    // ==========================================================================
    const initialPanel = document.querySelector('.research-panel.active');
    if (initialPanel) {
        initCardsReveal(initialPanel);
    }
});