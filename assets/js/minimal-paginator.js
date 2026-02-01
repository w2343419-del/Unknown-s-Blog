// 极简换页系统
(() => {
    let currentPage = 1;
    let totalPages = 1;
    
    function init() {
        const main = document.querySelector('.main');
        const container = document.querySelector('.main > .container');
        
        if (!main || !container) return;
        
        setTimeout(() => {
            checkAndPaginate(main, container);
        }, 800);
    }
    
    function checkAndPaginate(main, container) {
        const containerHeight = main.clientHeight;
        const contentHeight = container.offsetHeight;
        
        if (contentHeight <= containerHeight) return;
        
        totalPages = Math.ceil(contentHeight / containerHeight);
        createButtons(main);
    }
    
    function createButtons(main) {
        const btnGroup = document.createElement('div');
        btnGroup.style.cssText = `
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 999;
            background: rgba(0,0,0,0.8);
            padding: 8px 15px;
            border-radius: 20px;
        `;
        
        const prevBtn = document.createElement('button');
        prevBtn.textContent = '◀';
        prevBtn.style.cssText = `
            background: white;
            border: none;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.2s;
        `;
        prevBtn.onclick = () => goToPage(main, -1);
        
        const pageInfo = document.createElement('span');
        pageInfo.style.cssText = `
            color: white;
            font-size: 14px;
            font-weight: bold;
            min-width: 60px;
            text-align: center;
            display: inline-block;
        `;
        pageInfo.textContent = `${currentPage}/${totalPages}`;
        
        const nextBtn = document.createElement('button');
        nextBtn.textContent = '▶';
        nextBtn.style.cssText = `
            background: white;
            border: none;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.2s;
        `;
        nextBtn.onclick = () => goToPage(main, 1);
        
        btnGroup.appendChild(prevBtn);
        btnGroup.appendChild(pageInfo);
        btnGroup.appendChild(nextBtn);
        document.body.appendChild(btnGroup);
        
        // 更新按钮状态
        updateButtons(prevBtn, nextBtn, pageInfo);
        
        // 悬停效果
        prevBtn.onmouseover = () => prevBtn.style.transform = 'scale(1.1)';
        prevBtn.onmouseout = () => prevBtn.style.transform = 'scale(1)';
        nextBtn.onmouseover = () => nextBtn.style.transform = 'scale(1.1)';
        nextBtn.onmouseout = () => nextBtn.style.transform = 'scale(1)';
        
        // 键盘支持
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') goToPage(main, -1);
            if (e.key === 'ArrowRight') goToPage(main, 1);
        });
    }
    
    function goToPage(main, direction) {
        const newPage = currentPage + direction;
        if (newPage < 1 || newPage > totalPages) return;
        
        currentPage = newPage;
        const scrollTop = (currentPage - 1) * (main.clientHeight - 50);
        
        main.scrollTo({
            top: scrollTop,
            behavior: 'smooth'
        });
        
        // 更新显示
        document.querySelector('span').textContent = `${currentPage}/${totalPages}`;
        updateButtons(...document.querySelectorAll('button'));
    }
    
    function updateButtons(prevBtn, nextBtn, pageInfo) {
        if (prevBtn) prevBtn.disabled = currentPage === 1;
        if (nextBtn) nextBtn.disabled = currentPage === totalPages;
        if (prevBtn) prevBtn.style.opacity = currentPage === 1 ? '0.5' : '1';
        if (nextBtn) nextBtn.style.opacity = currentPage === totalPages ? '0.5' : '1';
    }
    
    // 启动
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();