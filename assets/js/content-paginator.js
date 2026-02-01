// 内容换页系统 - 自动检测内容溢出并提供换页功能
class ContentPaginator {
    constructor() {
        this.currentPage = 1;
        this.pages = [];
        this.containerHeight = 0;
        this.contentHeight = 0;
        this.pageHeight = 0;
        this.maxPages = 50; // 最大页数限制
        this.init();
    }

    init() {
        // 等待DOM完全加载
        if (document.readyState !== 'complete') {
            document.addEventListener('readystatechange', () => {
                if (document.readyState === 'complete') {
                    this.setupPaginator();
                }
            });
            return;
        }
        
        this.setupPaginator();
    }

    setupPaginator() {
        this.container = document.querySelector('.main > .container');
        if (!this.container) {
            console.log('内容换页系统：未找到容器元素');
            return;
        }

        this.main = document.querySelector('.main');
        if (!this.main) {
            console.log('内容换页系统：未找到主容器');
            return;
        }

        console.log('内容换页系统：初始化开始');
        
        // 延迟执行确保所有内容都已渲染
        setTimeout(() => {
            this.setupPagination();
            this.checkContentOverflow();
            this.createPaginationControls();
            
            // 监听窗口大小变化
            window.addEventListener('resize', () => {
                clearTimeout(this.resizeTimeout);
                this.resizeTimeout = setTimeout(() => {
                    this.checkContentOverflow();
                }, 300);
            });

            // 监听内容变化
            const observer = new MutationObserver(() => {
                clearTimeout(this.mutationTimeout);
                this.mutationTimeout = setTimeout(() => {
                    this.checkContentOverflow();
                }, 200);
            });
            
            observer.observe(this.container, { 
                childList: true, 
                subtree: true,
                attributes: false
            });
            
            console.log('内容换页系统：初始化完成');
        }, 500);
    }

    setupPagination() {
        // 获取可用高度（排除padding和其他元素）
        this.containerHeight = this.main.clientHeight - 40; // 减去padding
        this.pageHeight = this.containerHeight - 150; // 留出足够的换页按钮空间
        
        // 确保页面高度合理
        if (this.pageHeight < 300) {
            this.pageHeight = 300;
        }
        
        console.log(`容器高度设置: 总高度=${this.containerHeight}px, 页面高度=${this.pageHeight}px`);
    }

    checkContentOverflow() {
        try {
            // 检查容器是否还存在
            if (!this.container || !this.container.children) {
                console.warn('容器不存在或没有子元素');
                return;
            }

            this.setupPagination();
            
            // 如果页面高度太小，不启用换页
            if (this.pageHeight < 200) {
                console.warn('页面高度太小，跳过换页检测');
                return;
            }
            
            // 重置页面分割
            this.pages = [];
            this.currentPage = 1;

            // 排除换页控件和不可见的元素
            const elements = Array.from(this.container.children).filter(child => {
                if (child.classList && child.classList.contains('content-paginator')) {
                    return false;
                }
                // 检查元素是否可见
                const style = window.getComputedStyle(child);
                return style.display !== 'none' && style.visibility !== 'hidden';
            });
            
            let currentPageContent = [];
            let currentHeight = 0;

            console.log(`内容换页系统：总容器高度=${this.containerHeight}px, 页面高度=${this.pageHeight}px, 内容元素数=${elements.length}`);

            for (const element of elements) {
                if (!element) continue;
                
                const elementHeight = this.getElementHeight(element);
                console.log(`元素高度: ${elementHeight}px, 当前页面累计高度: ${currentHeight}px`);
                
                if (elementHeight === 0) continue; // 跳过高度为0的元素
                
                if (currentHeight + elementHeight <= this.pageHeight) {
                    currentPageContent.push(element);
                    currentHeight += elementHeight;
                } else {
                    // 如果单个元素太高，强制分割
                    if (elementHeight > this.pageHeight && currentPageContent.length === 0) {
                        currentPageContent.push(element);
                        this.pages.push([...currentPageContent]);
                        currentPageContent = [];
                        currentHeight = 0;
                    } else {
                        // 保存当前页
                        if (currentPageContent.length > 0) {
                            this.pages.push([...currentPageContent]);
                        }
                        currentPageContent = [element];
                        currentHeight = elementHeight;
                    }
                }
            }

            // 保存最后一页
            if (currentPageContent.length > 0) {
                this.pages.push([...currentPageContent]);
            }

            console.log(`内容换页系统：分割为 ${this.pages.length} 页`);

            // 如果只有一页且没有溢出，隐藏换页控件
            if (this.pages.length <= 1) {
                console.log('内容换页系统：只有一页，隐藏换页控件');
                this.hidePaginationControls();
                this.showAllContent();
            } else {
                console.log('内容换页系统：多页内容，显示换页控件');
                this.showPage(1);
                this.updatePaginationControls();
            }
        } catch (error) {
            console.error('检查内容溢出时出错:', error);
        }
    }

    getElementHeight(element) {
        // 检查元素是否存在
        if (!element || !element.parentNode) {
            console.warn('元素不存在或未在DOM中');
            return 0;
        }
        
        try {
            // 使用getBoundingClientRect获取更准确的高度
            const rect = element.getBoundingClientRect();
            let height = 0;
            
            // 如果元素当前不可见，临时显示它来测量高度
            const originalDisplay = element.style.display;
            const originalVisibility = element.style.visibility;
            const originalPosition = element.style.position;
            
            if (rect.height === 0) {
                element.style.display = '';
                element.style.visibility = 'hidden';
                element.style.position = 'absolute';
                height = element.offsetHeight;
            } else {
                height = rect.height;
            }
            
            // 恢复原始样式
            element.style.display = originalDisplay;
            element.style.visibility = originalVisibility;
            element.style.position = originalPosition;
            
            return Math.max(0, height);
        } catch (error) {
            console.error('获取元素高度时出错:', error);
            return 0;
        }
    }

    showPage(pageNumber) {
        try {
            if (pageNumber < 1 || pageNumber > this.pages.length) {
                console.warn('无效的页码:', pageNumber);
                return;
            }
            
            if (!this.container) {
                console.warn('容器不存在');
                return;
            }
            
            this.currentPage = pageNumber;
            
            // 隐藏所有元素（排除换页控件）
            Array.from(this.container.children).forEach(element => {
                if (element && element.classList && !element.classList.contains('content-paginator')) {
                    element.style.display = 'none';
                }
            });
            
            // 显示当前页元素
            if (this.pages[pageNumber - 1] && Array.isArray(this.pages[pageNumber - 1])) {
                this.pages[pageNumber - 1].forEach(element => {
                    if (element && element.style) {
                        element.style.display = '';
                        element.style.animation = 'fadeInUp 0.5s var(--ease-responsive) forwards';
                    }
                });
            }

            this.updatePaginationControls();
            this.scrollToTop();
        } catch (error) {
            console.error('显示页面时出错:', error);
        }
    }

    showAllContent() {
        // 显示所有元素
        Array.from(this.container.children).forEach(element => {
            element.style.display = '';
        });
    }

    createPaginationControls() {
        // 创建换页控件容器
        if (document.getElementById('content-paginator')) return;

        const controlsContainer = document.createElement('div');
        controlsContainer.id = 'content-paginator';
        controlsContainer.className = 'content-paginator';
        
        controlsContainer.innerHTML = `
            <div class="pagination-content">
                <button class="paginator-btn prev-btn" title="上一页">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
                    </svg>
                    <span>上一页</span>
                </button>
                
                <div class="page-info">
                    <span class="current-page">${this.currentPage}</span>
                    <span class="page-separator">/</span>
                    <span class="total-pages">${this.pages.length}</span>
                </div>
                
                <button class="paginator-btn next-btn" title="下一页">
                    <span>下一页</span>
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
                    </svg>
                </button>
            </div>
        `;

        // 添加事件监听器
        const prevBtn = controlsContainer.querySelector('.prev-btn');
        const nextBtn = controlsContainer.querySelector('.next-btn');
        
        prevBtn.addEventListener('click', () => this.previousPage());
        nextBtn.addEventListener('click', () => this.nextPage());

        // 插入到容器底部
        this.container.appendChild(controlsContainer);

        // 初始隐藏
        this.hidePaginationControls();
    }

    updatePaginationControls() {
        const controls = document.getElementById('content-paginator');
        if (!controls) return;

        const prevBtn = controls.querySelector('.prev-btn');
        const nextBtn = controls.querySelector('.next-btn');
        const currentPageSpan = controls.querySelector('.current-page');
        const totalPagesSpan = controls.querySelector('.total-pages');

        // 更新页码显示
        if (currentPageSpan) currentPageSpan.textContent = this.currentPage;
        if (totalPagesSpan) totalPagesSpan.textContent = this.pages.length;

        // 更新按钮状态
        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
            prevBtn.classList.toggle('disabled', this.currentPage === 1);
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.pages.length;
            nextBtn.classList.toggle('disabled', this.currentPage === this.pages.length);
        }

        // 显示控件
        controls.classList.add('show');
    }

    hidePaginationControls() {
        const controls = document.getElementById('content-paginator');
        if (controls) {
            controls.classList.remove('show');
        }
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.showPage(this.currentPage - 1);
        }
    }

    nextPage() {
        if (this.currentPage < this.pages.length) {
            this.showPage(this.currentPage + 1);
        }
    }

    scrollToTop() {
        this.main.scrollTop = 0;
        // 平滑滚动到顶部
        this.main.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// 初始化内容换页系统
document.addEventListener('DOMContentLoaded', () => {
    // 等待内容加载完成
    setTimeout(() => {
        new ContentPaginator();
    }, 500);
});

// 添加CSS样式到页面
const paginatorStyles = `
<style>
.content-paginator {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s var(--ease-responsive);
    margin-bottom: 0;
}

.content-paginator.show {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
}

.pagination-content {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 25px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 50px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    animation: slideUpFade 0.5s var(--ease-responsive);
}

.paginator-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 25px;
    color: white;
    font-weight: 500;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s var(--ease-responsive);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.paginator-btn:hover:not(.disabled) {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.paginator-btn:active:not(.disabled) {
    transform: translateY(-1px) scale(1.02);
}

.paginator-btn.disabled {
    background: rgba(200, 200, 200, 0.3);
    color: rgba(150, 150, 150, 0.8);
    cursor: not-allowed;
    box-shadow: none;
}

.paginator-btn svg {
    width: 18px;
    height: 18px;
}

.page-info {
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: 600;
    color: #333;
    font-size: 16px;
    padding: 8px 16px;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 20px;
    min-width: 60px;
    justify-content: center;
}

.current-page {
    color: var(--accent-color, #667eea);
    font-size: 18px;
}

.page-separator {
    opacity: 0.6;
}

.total-pages {
    opacity: 0.8;
}

@keyframes slideUpFade {
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
[data-scheme="dark"] .pagination-content {
    background: rgba(30, 30, 30, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

[data-scheme="dark"] .page-info {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
}

[data-scheme="dark"] .current-page {
    color: var(--accent-color, #8b5cf6);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
    .content-paginator {
        bottom: 20px;
        left: 50%;
        right: 20px;
        transform: translateX(-50%);
    }
    
    .pagination-content {
        padding: 12px 20px;
        gap: 12px;
    }
    
    .paginator-btn span:not(:first-child),
    .paginator-btn span:not(:last-child) {
        display: none;
    }
    
    .page-info {
        font-size: 14px;
        min-width: 50px;
        padding: 6px 12px;
    }
    
    .current-page {
        font-size: 16px;
    }
    
    .paginator-btn svg {
        width: 16px;
        height: 16px;
    }
}
</style>
`;

// 注入样式到页面
document.head.insertAdjacentHTML('beforeend', paginatorStyles);