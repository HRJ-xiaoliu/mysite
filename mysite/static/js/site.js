// 实用JavaScript - 轻量级交互功能
// ========================================

(function() {
    'use strict';

    // DOM 加载完成后初始化
    document.addEventListener('DOMContentLoaded', function() {
        initSearch();
        initDropdownMenu();
        initSmoothScroll();
        initScrollSpy();
        initAnimations();
    });

    // ========================================
    // 搜索功能
    // ========================================
    function initSearch() {
        const searchBtn = document.querySelector('.search-btn');
        const searchDialog = document.querySelector('.search-dialog-box');
        const searchClose = document.querySelector('.pub-close');
        const searchBg = document.querySelector('.search-bg');

        if (!searchBtn || !searchDialog) return;

        // 打开搜索对话框
        searchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            searchDialog.classList.add('active');
            document.body.style.overflow = 'hidden';

            // 聚焦到搜索输入框（如果存在）
            const searchInput = searchDialog.querySelector('input[type="text"]');
            if (searchInput) {
                setTimeout(() => searchInput.focus(), 300);
            }
        });

        // 关闭搜索对话框
        function closeSearch() {
            searchDialog.classList.remove('active');
            document.body.style.overflow = '';
        }

        if (searchClose) {
            searchClose.addEventListener('click', closeSearch);
        }

        if (searchBg) {
            searchBg.addEventListener('click', closeSearch);
        }

        // ESC 键关闭
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && searchDialog.classList.contains('active')) {
                closeSearch();
            }
        });
    }

    // ========================================
    // 下拉菜单功能（仅移动端）
    // ========================================
    function initDropdownMenu() {
        if (window.innerWidth > 768) return; // 桌面端不需要

        const navItems = document.querySelectorAll('.nav-item.has-submenu');
        
        navItems.forEach(item => {
            const link = item.querySelector('.nav-link');
            
            link.addEventListener('click', function(e) {
                const isActive = item.classList.contains('active');
                
                // 关闭其他的子菜单
                navItems.forEach(other => {
                    if (other !== item) {
                        other.classList.remove('active');
                    }
                });
                
                // 切换当前菜单
                if (isActive) {
                    item.classList.remove('active');
                } else {
                    e.preventDefault();
                    item.classList.add('active');
                }
            });
        });

        // 点击外部关闭菜单
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.nav-item')) {
                navItems.forEach(item => {
                    item.classList.remove('active');
                });
            }
        });
    }

    // ========================================
    // 平滑滚动
    // ========================================
    function initSmoothScroll() {
        // 为所有内部链接添加平滑滚动
        const internalLinks = document.querySelectorAll('a[href^="#"]');

        internalLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ========================================
    // 导航高亮与滚动侦测
    // ========================================
    function initScrollSpy() {
        const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
        const sections = Array.from(navLinks)
            .map(link => document.getElementById(link.getAttribute('href').substring(1)))
            .filter(Boolean);

        if (!navLinks.length || !sections.length) return;

        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    const sectionId = entry.target.id;
                    const link = document.querySelector(`.nav-links a[href="#${sectionId}"]`);

                    if (!link) return;
                    if (entry.isIntersecting) {
                        navLinks.forEach(el => el.classList.remove('active'));
                        link.classList.add('active');
                    }
                });
            },
            { threshold: 0.3, rootMargin: '0px 0px -40% 0px' }
        );

        sections.forEach(section => observer.observe(section));
    }

    // ========================================
    // 基础动画效果
    // ========================================
    function initAnimations() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.classList.add('reduced-motion');
            return;
        }

        const observerOptions = {
            threshold: 0.12,
            rootMargin: '0px 0px -80px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        const animateElements = document.querySelectorAll('.feature-card, .blog-post-item, .portfolio-item, .research-item-card');
        animateElements.forEach(el => {
            el.classList.add('animate-ready');
            observer.observe(el);
        });
    }

    // ========================================
    // 工具函数
    // ========================================

    // 防抖函数
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // 节流函数
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // 添加到全局作用域（可选）
    window.SiteUtils = {
        debounce: debounce,
        throttle: throttle
    };

})();