/**
 * 增强分页体验的JavaScript
 * 提供平滑的页面切换、加载状态和键盘导航
 */
document.addEventListener('DOMContentLoaded', function() {
    // 分页增强功能
    const paginationEnhancement = {
        init: function() {
            this.setupPaginationTransitions();
            this.setupKeyboardNavigation();
            this.setupLoadingStates();
            this.setupScrollPosition();
        },

        // 设置分页切换时的平滑过渡
        setupPaginationTransitions: function() {
            const paginationLinks = document.querySelectorAll('.pagination .page-link:not(.disabled):not(.current)');
            
            paginationLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const href = this.getAttribute('href');
                    
                    if (href && href !== '#') {
                        this.classList.add('loading');
                        this.style.opacity = '0.6';
                        
                        // 添加页面切换动画
                        document.body.classList.add('page-transitioning');
                        
                        // 延迟跳转以显示加载状态
                        setTimeout(() => {
                            window.location.href = href;
                        }, 150);
                    }
                });
            });
        },

        // 设置键盘导航
        setupKeyboardNavigation: function() {
            document.addEventListener('keydown', function(e) {
                // 左箭头 - 上一页
                if (e.key === 'ArrowLeft') {
                    const prevLink = document.querySelector('.pagination .page-link[href*="prev"], .pagination .page-link:not(.disabled):first-child');
                    if (prevLink && !prevLink.classList.contains('current')) {
                        prevLink.click();
                    }
                }
                // 右箭头 - 下一页
                else if (e.key === 'ArrowRight') {
                    const nextLink = document.querySelector('.pagination .page-link[href*="next"], .pagination .page-link:not(.disabled):last-child');
                    if (nextLink && !nextLink.classList.contains('current')) {
                        nextLink.click();
                    }
                }
            });
        },

        // 设置加载状态
        setupLoadingStates: function() {
            // 为分页按钮添加微交互
            const paginationButtons = document.querySelectorAll('.pagination .page-link');
            
            paginationButtons.forEach(button => {
                // 鼠标进入效果
                button.addEventListener('mouseenter', function() {
                    if (!this.classList.contains('disabled') && !this.classList.contains('current')) {
                        this.style.transform = 'translateY(-2px) scale(1.05)';
                    }
                });
                
                // 鼠标离开效果
                button.addEventListener('mouseleave', function() {
                    if (!this.classList.contains('loading')) {
                        this.style.transform = '';
                    }
                });
                
                // 按下效果
                button.addEventListener('mousedown', function() {
                    if (!this.classList.contains('disabled')) {
                        this.style.transform = 'translateY(0px) scale(0.98)';
                    }
                });
                
                // 释放效果
                button.addEventListener('mouseup', function() {
                    if (!this.classList.contains('disabled')) {
                        this.style.transform = 'translateY(-2px) scale(1.05)';
                    }
                });
            });
        },

        // 设置滚动位置管理
        setupScrollPosition: function() {
            // 如果是从分页页面过来的，滚动到文章列表顶部
            if (window.location.search.includes('page') || window.location.pathname.includes('/page/')) {
                const articleList = document.querySelector('.article-list');
                if (articleList) {
                    setTimeout(() => {
                        articleList.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'start' 
                        });
                    }, 100);
                }
            }

            // 保存滚动位置
            const saveScrollPosition = () => {
                sessionStorage.setItem('scrollPosition', window.pageYOffset);
            };

            // 恢复滚动位置
            const restoreScrollPosition = () => {
                const scrollPosition = sessionStorage.getItem('scrollPosition');
                if (scrollPosition) {
                    window.scrollTo(0, parseInt(scrollPosition));
                    sessionStorage.removeItem('scrollPosition');
                }
            };

            // 在页面离开时保存位置
            window.addEventListener('beforeunload', saveScrollPosition);
            
            // 在页面加载后恢复位置
            setTimeout(restoreScrollPosition, 100);
        },

        // 显示分页提示
        showPaginationHint: function() {
            const pagination = document.querySelector('.pagination');
            if (pagination) {
                // 添加键盘导航提示
                const hint = document.createElement('div');
                hint.className = 'pagination-hint';
                hint.innerHTML = `
                    <div class="hint-content">
                        <span class="hint-text">使用 ← → 键快速导航</span>
                    </div>
                `;
                
                pagination.appendChild(hint);
                
                // 3秒后隐藏提示
                setTimeout(() => {
                    hint.style.opacity = '0';
                    setTimeout(() => {
                        if (hint.parentNode) {
                            hint.parentNode.removeChild(hint);
                        }
                    }, 300);
                }, 3000);
            }
        }
    };

    // 初始化分页增强功能
    paginationEnhancement.init();
    
    // 显示键盘导航提示
    setTimeout(() => {
        paginationEnhancement.showPaginationHint();
    }, 1000);

    // 页面切换动画样式
    const style = document.createElement('style');
    style.textContent = `
        .page-transitioning {
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }
        
        .pagination .page-link.loading {
            pointer-events: none;
            position: relative;
        }
        
        .pagination .page-link.loading::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 16px;
            height: 16px;
            border: 2px solid var(--accent-color, #007bff);
            border-radius: 50%;
            border-top-color: transparent;
            animation: paginationSpin 0.8s linear infinite;
        }
        
        @keyframes paginationSpin {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .pagination-hint {
            position: absolute;
            top: -40px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1000;
            opacity: 1;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .hint-content {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .pagination-hint .hint-text {
            font-weight: 500;
        }
        
        @media screen and (max-width: 768px) {
            .pagination-hint {
                display: none; /* 移动端不显示键盘提示 */
            }
        }
    `;
    document.head.appendChild(style);
});