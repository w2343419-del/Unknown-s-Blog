// 简化的内容换页系统
class SimplePaginator {
    constructor() {
        this.currentPage = 1;
        this.totalPages = 1;
        this.containerHeight = 0;
        this.contentElements = [];
        this.init();
    }

    init() {
        // 确保DOM完全加载
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        const mainContainer = document.querySelector('.main');
        const contentContainer = document.querySelector('.main > .container');
        
        if (!mainContainer || !contentContainer) {
            console.log('未找到必要容器');
            return;
        }

        console.log('开始设置简化换页系统');

        // 延迟执行确保内容完全渲染
        setTimeout(() => {
            this.analyzeContent(mainContainer, contentContainer);
            this.createControls();
            this.setupEventListeners();
        }, 1000);
    }

    analyzeContent(mainContainer, contentContainer) {
        // 获取可用高度
        this.containerHeight = mainContainer.clientHeight - 100; // 预留空间
        
        if (this.containerHeight < 300) {
            console.log('容器高度太小，跳过换页');
            return;
        }

        console.log('容器高度:', this.containerHeight);

        // 获取所有内容元素
        this.contentElements = Array.from(contentContainer.children)
            .filter(child => !child.classList.contains('simple-paginator-controls'));

        // 计算总高度
        let totalHeight = 0;
        this.contentElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            totalHeight += rect.height;
            console.log(`元素 ${element.tagName} 高度:`, rect.height);
        });

        console.log('总内容高度:', totalHeight);

        // 计算需要的页数
        this.totalPages = Math.ceil(totalHeight / this.containerHeight);
        console.log('计算出的页数:', this.totalPages);

        // 只有当内容确实需要换页时才显示控件
        if (this.totalPages > 1) {
            this.showControls();
            this.goToPage(1);
        }
    }

    createControls() {
        // 创建控制面板
        const controls = document.createElement('div');
        controls.className = 'simple-paginator-controls';
        controls.innerHTML = `
            <div class="paginator-wrapper">
                <button id="prev-page" class="paginator-btn" disabled>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
                    </svg>
                    <span>上一页</span>
                </button>
                
                <div class="page-info">
                    <span class="current-page">1</span>
                    <span class="separator">/</span>
                    <span class="total-pages">${this.totalPages}</span>
                </div>
                
                <button id="next-page" class="paginator-btn">
                    <span>下一页</span>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
                    </svg>
                </button>
            </div>
        `;

        document.body.appendChild(controls);
        this.controls = controls;

        // 添加样式
        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .simple-paginator-controls {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 1000;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                pointer-events: none;
            }
            
            .simple-paginator-controls.show {
                opacity: 1;
                visibility: visible;
                pointer-events: auto;
            }
            
            .paginator-wrapper {
                display: flex;
                align-items: center;
                gap: 15px;
                padding: 12px 20px;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 25px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .paginator-btn {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .paginator-btn:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .paginator-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                background: #ccc;
                box-shadow: none;
            }
            
            .page-info {
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 6px 12px;
                background: rgba(0, 0, 0, 0.05);
                border-radius: 15px;
                font-size: 14px;
                font-weight: 600;
            }
            
            .current-page {
                color: #667eea;
                font-size: 16px;
            }
            
            .separator {
                opacity: 0.6;
            }
            
            .total-pages {
                opacity: 0.8;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* 暗色模式 */
            [data-scheme="dark"] .paginator-wrapper {
                background: rgba(30, 30, 30, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            [data-scheme="dark"] .page-info {
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.9);
            }
            
            [data-scheme="dark"] .current-page {
                color: #8b5cf6;
            }
            
            /* 响应式 */
            @media (max-width: 768px) {
                .paginator-wrapper {
                    padding: 10px 16px;
                    gap: 12px;
                }
                
                .paginator-btn span:not(:first-child),
                .paginator-btn span:not(:last-child) {
                    display: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    showControls() {
        if (this.controls) {
            this.controls.classList.add('show');
        }
    }

    hideControls() {
        if (this.controls) {
            this.controls.classList.remove('show');
        }
    }

    setupEventListeners() {
        if (!this.controls) return;

        const prevBtn = this.controls.querySelector('#prev-page');
        const nextBtn = this.controls.querySelector('#next-page');

        prevBtn.addEventListener('click', () => this.goToPage(this.currentPage - 1));
        nextBtn.addEventListener('click', () => this.goToPage(this.currentPage + 1));

        // 键盘支持
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.goToPage(this.currentPage - 1);
            if (e.key === 'ArrowRight') this.goToPage(this.currentPage + 1);
        });

        // 窗口大小变化
        window.addEventListener('resize', () => {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                location.reload(); // 简单重载重新计算
            }, 500);
        });
    }

    goToPage(pageNumber) {
        if (pageNumber < 1 || pageNumber > this.totalPages) return;

        this.currentPage = pageNumber;
        
        // 计算滚动位置
        const scrollPosition = (pageNumber - 1) * this.containerHeight;
        
        // 滚动主容器
        const mainContainer = document.querySelector('.main');
        if (mainContainer) {
            mainContainer.scrollTo({
                top: scrollPosition,
                behavior: 'smooth'
            });
        }

        // 更新按钮状态
        this.updateControls();
    }

    updateControls() {
        if (!this.controls) return;

        const prevBtn = this.controls.querySelector('#prev-page');
        const nextBtn = this.controls.querySelector('#next-page');
        const currentPageSpan = this.controls.querySelector('.current-page');

        if (prevBtn) prevBtn.disabled = this.currentPage === 1;
        if (nextBtn) nextBtn.disabled = this.currentPage === this.totalPages;
        if (currentPageSpan) currentPageSpan.textContent = this.currentPage;

        // 显示或隐藏控件
        if (this.totalPages <= 1) {
            this.hideControls();
        } else {
            this.showControls();
        }
    }
}

// 初始化换页系统
new SimplePaginator();