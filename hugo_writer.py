import os
import subprocess
import http.server
import socketserver
import json
import webbrowser
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import urllib.request

PORT = 8080
HUGO_PATH = os.getcwd()

def translate_text(text, source_lang='zh', target_lang='en'):
    """简单的翻译功能"""
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={source_lang}|{target_lang}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data['responseData']['translatedText']
    except:
        return text

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WangScape Writer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sitka+Small&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --dash-bg: #0a0a0a;
            --dash-sidebar: #141414;
            --dash-text: #ffffff;
            --dash-text-dim: #888888;
            --dash-accent: #00ffcc; 
            --dash-border: rgba(255,255,255,0.1);
            --word-bg: #f3f2f1;
            --word-blue: #2b579a;
            --word-paper: #ffffff;
            --word-text: #201f1e;
            --word-border: #e1dfdd;
            --font-main: 'Inter', 'Noto Sans SC', sans-serif;
        }

        body {
            margin: 0;
            font-family: var(--font-main);
            overflow: hidden;
            height: 100vh;
        }

        .view-section {
            display: none;
            width: 100%;
            height: 100%;
        }
        
        .view-section.active {
            display: flex;
        }

        /* Dashboard */
        #dashboard-view {
            background: var(--dash-bg);
            color: var(--dash-text);
        }

        .dash-sidebar {
            width: 280px;
            background: var(--dash-sidebar);
            border-right: 1px solid var(--dash-border);
            padding: 30px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .dash-logo {
            font-size: 24px;
            font-weight: 700;
            color: var(--dash-accent);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .dash-btn {
            background: transparent;
            border: 1px solid var(--dash-border);
            color: var(--dash-text);
            padding: 12px 20px;
            border-radius: 12px;
            cursor: pointer;
            text-align: left;
            font-size: 14px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .dash-btn:hover {
            border-color: var(--dash-accent);
            background: rgba(0, 255, 204, 0.05);
        }
        .dash-btn.primary {
            background: var(--dash-accent);
            color: #000;
            border: none;
            font-weight: 600;
        }
        
        .dash-btn.primary:hover {
            opacity: 0.9;
        }

        .dash-main {
            flex: 1;
            padding: 50px;
            overflow-y: auto;
        }

        .dash-header {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 30px;
            letter-spacing: -0.5px;
        }

        .post-list-card {
            background: var(--dash-sidebar);
            border-radius: 16px;
            border: 1px solid var(--dash-border);
            overflow: hidden;
        }

        .dash-post-item {
            padding: 20px 25px;
            border-bottom: 1px solid var(--dash-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: background 0.2s;
        }
        .dash-post-item:hover {
            background: rgba(255,255,255,0.03);
        }
        .dash-post-item:last-child { border-bottom: none; }
        
        .dpi-title { 
            font-size: 16px; 
            font-weight: 600; 
            color: var(--dash-text); 
            margin-bottom: 5px; 
        }
        
        .dpi-meta { 
            font-size: 12px; 
            color: var(--dash-text-dim); 
            font-family: monospace; 
        }
        
        /* Editor View */
        #editor-view {
            background: var(--word-bg);
            color: var(--word-text);
            flex-direction: column;
        }

        .word-topbar {
            background: var(--word-blue);
            color: white;
            height: 48px;
            display: flex;
            align-items: center;
            padding: 0 16px;
            justify-content: space-between;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .word-back-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .word-back-btn:hover { 
            background: rgba(255,255,255,0.3); 
        }

        .word-ribbon {
            background: white;
            border-bottom: 1px solid var(--word-border);
            padding: 8px 20px;
            display: flex;
            gap: 10px;
        }

        .word-rib-btn {
            border: 1px solid transparent;
            background: transparent;
            padding: 6px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 13px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: #333;
        }
        .word-rib-btn:hover {
            background: #f0f0f0;
            border-color: #d0d0d0;
        }

        .word-workspace {
            flex: 1;
            display: flex;
            overflow: hidden;
        }

        .word-canvas {
            flex: 1;
            background: #f3f3f3;
            padding: 40px;
            overflow-y: auto;
            display: flex;
            justify-content: center;
        }

        .word-paper {
            width: 800px;
            min-height: 1000px;
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 60px 80px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }

        .wp-title { 
            font-family: 'Sitka Small', serif; 
            font-size: 32px; 
            font-weight: 700; 
            border-bottom: 2px solid #eee; 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
        }
        
        /* Modal */
        .modal-overlay {
            position: fixed;
            top: 0; 
            left: 0; 
            right: 0; 
            bottom: 0;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }
        
        .modal-card {
            background: #1a1a1a;
            color: white;
            width: 500px;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        
        .modal-card input {
            width: 100%;
            padding: 12px;
            background: #000;
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            border-radius: 8px;
            margin-top: 8px;
            margin-bottom: 20px;
        }
        
        .modal-card button { 
            padding: 10px 20px; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: 600; 
        }
        
        .btn-confirm { 
            background: var(--dash-accent); 
            color: black; 
            border: none; 
        }
        
        .btn-cancel { 
            background: transparent; 
            color: #ccc; 
            border: 1px solid #555; 
            margin-right: 10px; 
        }

    </style>
</head>
<body>

    <!-- VIEW 1: DASHBOARD -->
    <div id="dashboard-view" class="view-section active">
        <div class="dash-sidebar">
            <div class="dash-logo" data-i18n="app-title">WangScape助手</div>
            
            <button class="dash-btn primary" onclick="openCreateModal()">
                <span data-i18n="btn-new">+ N新建文章</span>
            </button>
            <button class="dash-btn" onclick="runCommand('preview')">
                <span data-i18n="btn-preview">🌍 启动实时预览</span>
            </button>
            <button class="dash-btn" onclick="runCommand('deploy')">
                <span data-i18n="btn-deploy">🚀 一键提交推送</span>
            </button>
            <button class="dash-btn" onclick="location.reload()">
                <span data-i18n="btn-refresh">🔄 刷新列表</span>
            </button>
            
            <div style="margin-top:auto; font-size:12px; color:var(--dash-text-dim);">
                <span data-i18n="status-online">系统状态: 在线</span><br>
                v2.8 Live Sync
            </div>
        </div>
        
        <div class="dash-main">
            <h1 class="dash-header" data-i18n="header-latest">最新博文内容</h1>
            <div id="dash-post-list" class="post-list-card">
                <!-- Posts... -->
            </div>
        </div>
    </div>

    <!-- VIEW 2: EDITOR (OFFICE STYLE) -->
    <div id="editor-view" class="view-section">
        <div class="word-topbar">
            <div style="display:flex; align-items:center; gap:15px;">
                <button class="word-back-btn" onclick="switchView('dashboard')" data-i18n="back-dash">← Back to Dashboard</button>
                <strong style="font-size:16px;" data-i18n="app-title">WangScape Writer</strong>
            </div>
            <div>
                <span id="current-doc-name" style="opacity:0.8; margin-right:20px; font-size:13px;"></span>
                <span id="save-status" style="font-size:12px; margin-right:15px; color:#ddd;"></span>
                <button class="word-back-btn" onclick="toggleLang()" style="display:inline-flex;">EN / 中</button>
            </div>
        </div>
        
        <div class="word-ribbon">
            <button class="word-rib-btn" onclick="saveDocument()">
                <span data-i18n="save-publish">💾 Save</span>
            </button>
            <button class="word-rib-btn" onclick="runCommand('deploy')">
                <span data-i18n="publish-site">🚀 Publish</span>
            </button>
            <button class="word-rib-btn" onclick="runCommand('preview')">
                <span data-i18n="preview-site">👁 Preview Site</span>
            </button>
        </div>

        <div class="word-workspace">
            <div class="word-canvas">
                <div class="word-paper" id="paper-content">
                    <div style="text-align:center; color:#999; margin-top:100px;" data-i18n="select-tip">
                        Select a document to edit.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- CREATE MODAL -->
    <div class="modal-overlay" id="create-modal">
        <div class="modal-card">
            <h2 style="margin-top:0" data-i18n="modal-title">创作新篇章</h2>
            <label data-i18n="modal-label-title">文章标题 (中文)</label>
            <input type="text" id="postTitle" placeholder="例如：冬日随笔">
            <label data-i18n="modal-label-cat">分类 (Categories)</label>
            <input type="text" id="postCat" placeholder="Life, Code">
            <p style="font-size:12px; color:var(--dash-text-dim)" data-i18n="modal-tip">* 系统将自动生成双语版本 (zh-cn/en)。</p>
            <div style="text-align:right">
                <button class="btn-cancel" onclick="closeCreateModal()" data-i18n="btn-cancel">取消</button>
                <button class="btn-confirm" onclick="createPost()" data-i18n="btn-create">立即创建</button>
            </div>
        </div>
    </div>

    <script>
        const translations = {
            'zh': {
                'app-title': 'WangScape 写作助手',
                'btn-new': '+ 新建文章 (双语同步)',
                'btn-preview': '🌍 启动实时预览',
                'btn-deploy': '🚀 一键提交推送',
                'btn-refresh': '🔄 刷新列表',
                'header-latest': '最新博文内容',
                'status-online': '在线',
                'back-dash': '← 返回仪表盘',
                'save-publish': '💾 保存',
                'publish-site': '🚀 发布',
                'preview-site': '👁 预览',
                'loading': '正在加载...',
                'select-tip': '请选择左侧文章进行编辑',
                'modal-title': '创作新篇章',
                'modal-label-title': '文章标题 (中文)',
                'modal-label-cat': '分类 (Categories)',
                'modal-tip': '* 系统将自动生成双语版本 (zh-cn/en)。',
                'btn-cancel': '取消',
                'btn-create': '立即创建',
                'del-confirm': '确定要删除这篇文章吗？操作不可恢复。',
                'create-success': '创建成功！请在列表中点击编辑。',
                'save-success': '已保存 ',
                'status-ready': '已就绪',
                'empty-list': '暂无文章，点击左上角新建',
                'status-draft': '草稿',
                'status-mod': '已修改',
                'status-new': '未跟踪',
                'status-pub': '已发布'
            },
            'en': {
                'app-title': 'WangScape Writer',
                'btn-new': '+ New Post (Bilingual)',
                'btn-preview': '🌍 Start Preview',
                'btn-deploy': '🚀 Deploy & Push',
                'btn-refresh': '🔄 Refresh',
                'header-latest': 'Latest Posts',
                'status-online': 'Online',
                'back-dash': '← Dashboard',
                'save-publish': '💾 Save',
                'publish-site': '🚀 Publish',
                'preview-site': '👁 Preview',
                'loading': 'Loading...',
                'select-tip': 'Select a post to edit',
                'modal-title': 'Create New Post',
                'modal-label-title': 'Post Title (Chinese)',
                'modal-label-cat': 'Categories',
                'modal-tip': '* Auto-generates bilingual versions (zh-cn/en).',
                'btn-cancel': 'Cancel',
                'btn-create': 'Create',
                'del-confirm': 'Are you sure you want to delete this post?',
                'create-success': 'Created! Click to edit.',
                'save-success': 'Saved ',
                'status-ready': 'Ready',
                'empty-list': 'No posts found.',
                'status-draft': 'DRAFT',
                'status-mod': 'MODIFIED',
                'status-new': 'UNTRACKED',
                'status-pub': 'PUBLISHED'
            }
        };

        let postsData = [];
        let currentDocPath = '';
        let currentLang = 'zh';

        function switchView(viewName) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
            document.getElementById(viewName + '-view').classList.add('active');
            if(viewName === 'dashboard') fetchPosts();
        }

        async function init() {
            await fetchPosts();
            updateLanguage();
        }

        function toggleLang() {
            currentLang = currentLang === 'zh' ? 'en' : 'zh';
            updateLanguage();
            renderDashboardList(); 
        }

        function updateLanguage() {
            const t = translations[currentLang];
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if(t[key]) {
                    const firstChild = el.firstChild;
                    if(firstChild && firstChild.nodeType === 3) {
                         el.innerText = t[key];
                    } else {
                         el.innerText = t[key];
                    }
                }
            });
            document.getElementById('postTitle').placeholder = currentLang === 'zh' ? '例如：冬日随笔' : 'e.g. Winter Thoughts';
        }

        async function fetchPosts() {
            const res = await fetch('/api/posts');
            postsData = await res.json();
            renderDashboardList();
        }

        function renderDashboardList() {
            const t = translations[currentLang];
            const list = document.getElementById('dash-post-list');
            if (postsData.length === 0) {
                list.innerHTML = `<div style="padding:40px; text-align:center; color:#555;">${t['empty-list']}</div>`;
                return;
            }
            list.innerHTML = postsData.map(p => {
                let sLabel = p.status || 'PUBLISHED';
                if(sLabel === 'DRAFT') sLabel = t['status-draft'];
                if(sLabel === 'MODIFIED') sLabel = t['status-mod'];
                if(sLabel === 'UNTRACKED') sLabel = t['status-new'];
                if(sLabel === 'PUBLISHED') sLabel = t['status-pub'];

                return `
                <div class="dash-post-item">
                    <div onclick="openEditor('${p.path}', '${p.title}', '${p.date}')" style="flex:1; cursor:pointer; display:flex; flex-direction:column; gap:4px;">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="dpi-title">${p.title}</div>
                            <span style="font-size:10px; padding:2px 6px; border-radius:4px; background:${p.status_color}20; color:${p.status_color}; font-weight:600; border:1px solid ${p.status_color}40;">
                                ${sLabel}
                            </span>
                        </div>
                        <div class="dpi-meta">${p.date} · ${p.lang.toUpperCase()} · ${p.path}</div>
                    </div>
                    <div style="display:flex; gap:15px; align-items:center;">
                         <button onclick="deleteDocument('${p.path}')" title="${t['btn-cancel']}" style="
                            background:rgba(255,50,50,0.1); border:1px solid rgba(255,50,50,0.2); 
                            color:#ff5555; width:32px; height:32px; border-radius:8px; 
                            cursor:pointer; display:flex; align-items:center; justify-content:center;
                            transition:all 0.2s;">
                            🗑
                         </button>
                         <button onclick="openEditor('${p.path}', '${p.title}', '${p.date}')" title="Edit" style="
                            background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); 
                            color:#fff; width:32px; height:32px; border-radius:8px; 
                            cursor:pointer; display:flex; align-items:center; justify-content:center;
                            transition:all 0.2s;">
                            ✎
                         </button>
                    </div>
                </div>
            `}).join('');
        }

        async function openEditor(path, title, date) {
            currentDocPath = path;
            switchView('editor');
            document.getElementById('current-doc-name').textContent = title;
            const paper = document.getElementById('paper-content');
            paper.innerHTML = `<div style="text-align:center; margin-top:50px; color:#888;">${translations[currentLang]['loading']}</div>`;
            
            try {
                const res = await fetch('/api/get_content?path=' + encodeURIComponent(path));
                const data = await res.json();
                
                paper.innerHTML = `
                    <div class="wp-title">${title}</div>
                    <div style="font-size:12px; color:#999; margin-bottom:20px;">Date: ${date}</div>
                    <textarea id="editor-textarea" spellcheck="false" 
                        style="width:100%; height:800px; border:none; resize:none; outline:none; font-family:'Inter', monospace; font-size:15px; line-height:1.6; color:#333;">${data.content}</textarea>
                `;
            } catch(e) {
                paper.innerHTML = `<div style="color:red">Error: ${e}</div>`;
            }
        }

        async function saveDocument() {
            if(!currentDocPath) return;
            const content = document.getElementById('editor-textarea').value;
            const statusEl = document.getElementById('save-status');
            const t = translations[currentLang];
            statusEl.textContent = t['save-success'] + "...";
            
            try {
                const res = await fetch('/api/save_content', {
                    method: 'POST',
                    body: JSON.stringify({ path: currentDocPath, content: content })
                });
                const data = await res.json();
                if(data.success) {
                    statusEl.textContent = t['save-success'] + new Date().toLocaleTimeString();
                    setTimeout(() => statusEl.textContent = "", 3000);
                    fetchPosts(); 
                } else {
                    alert("Save failed: " + data.message);
                }
            } catch(e) { alert("Err: " + e); }
        }

        async function deleteDocument(path) {
            if(!confirm(translations[currentLang]['del-confirm'])) return;
            try {
                const res = await fetch('/api/delete_post', {
                    method: 'POST',
                    body: JSON.stringify({ path: path })
                });
                const data = await res.json();
                if(data.success) {
                    fetchPosts(); 
                } else {
                    alert("Delete failed: " + data.message);
                }
            } catch(e) { alert("Err: " + e); }
        }

        function openCreateModal() { document.getElementById('create-modal').style.display = 'flex'; }
        function closeCreateModal() { document.getElementById('create-modal').style.display = 'none'; }
        
        async function createPost() {
            const title = document.getElementById('postTitle').value;
            const cat = document.getElementById('postCat').value;
            if(!title) return alert('Title required');
            
            try {
                const res = await fetch('/api/create_sync', {
                    method: 'POST',
                    body: JSON.stringify({ title, categories: cat })
                });
                const data = await res.json();
                if(data.success) {
                    closeCreateModal();
                    await fetchPosts();
                    alert(translations[currentLang]['create-success']);
                } else {
                    alert('Err: ' + data.message);
                }
            } catch(e) { alert('Err: ' + e); }
        }

        async function runCommand(cmd) {
            const res = await fetch('/api/command?name=' + cmd);
            const data = await res.json();
            if(data.message.url) {
                window.open(data.message.url, '_blank');
            } else if(data.url) {
                 if(data.message.url) {
                     window.open(data.message.url, '_blank');
                 }
                 alert('System: ' + (data.message.message || data.message));
            } else {
                 alert('System: ' + data.message);
            }
        }

        init();
    </script>
</body>
</html>
"""

class HugoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        elif self.path == '/api/posts':
            posts = self.get_posts()
            self.send_json(posts)
        elif self.path.startswith('/api/get_content'):
            query = parse_qs(urlparse(self.path).query)
            path = query.get('path', [None])[0]
            if path:
                content = self.get_content(path)
                self.send_json({"content": content})
            else:
                self.send_error(400)
        elif self.path.startswith('/api/command'):
            query = parse_qs(urlparse(self.path).query)
            cmd = query.get('name', [None])[0]
            msg = self.handle_command(cmd)
            self.send_json({"success": True, "message": msg})
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode())
        
        if self.path == '/api/create_sync':
            success, result = self.create_sync_post(data)
            self.send_json({"success": success, **result})
        elif self.path == '/api/save_content':
            success, msg = self.save_content(data)
            self.send_json({"success": success, "message": msg})
        elif self.path == '/api/delete_post':
            success, msg = self.delete_post(data)
            self.send_json({"success": success, "message": msg})
        else:
            self.send_error(404)

    def save_content(self, data):
        """保存文件内容"""
        try:
            rel_path = data.get('path', '')
            content = data.get('content', '')
            
            # 安全检查
            if '..' in rel_path or not rel_path.lower().endswith('.md'):
                return False, "Invalid path"
                
            full_path = os.path.join(HUGO_PATH, rel_path)
            
            if not os.path.abspath(full_path).startswith(HUGO_PATH):
                return False, "Path security violation"

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Success"
        except Exception as e:
            return False, str(e)

    def delete_post(self, data):
        """删除文章"""
        try:
            rel_path = data.get('path', '')
            full_path = os.path.join(HUGO_PATH, rel_path)
            
            if not os.path.abspath(full_path).startswith(HUGO_PATH) or not full_path.lower().endswith('.md'):
                return False, "Invalid path"
                
            if os.path.exists(full_path):
                os.remove(full_path)
                parent_dir = os.path.dirname(full_path)
                if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                    os.rmdir(parent_dir)
            return True, "Deleted"
        except Exception as e:
            return False, str(e)

    def get_content(self, rel_path):
        """读取文件内容"""
        try:
            full_path = os.path.join(HUGO_PATH, rel_path)
            if not os.path.exists(full_path) or not full_path.lower().endswith('.md'):
                return "File not found or invalid."
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error: {str(e)}"

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def get_git_status(self):
        """获取Git状态"""
        status_map = {}
        try:
            res = subprocess.run(["git", "status", "--porcelain"], 
                               capture_output=True, text=True, cwd=HUGO_PATH, timeout=5)
            for line in res.stdout.splitlines():
                if len(line) > 3:
                    stat = line[:2].strip()
                    path = line[3:].strip().replace('"', '').replace('/', os.sep)
                    status_map[path] = stat
        except:
            pass
        return status_map

    def get_posts(self):
        """获取文章列表"""
        posts = []
        git_map = self.get_git_status()
        content_root = os.path.join(HUGO_PATH, 'content')
        
        if not os.path.exists(content_root):
            return []

        for root, dirs, files in os.walk(content_root):
            for f in files:
                if not f.endswith('.md') or f.startswith('_'):
                    continue
                    
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, HUGO_PATH)
                
                # 只过滤包含post的路径
                path_parts = rel_path.lower().split(os.sep)
                if 'post' not in path_parts and 'posts' not in path_parts:
                    continue

                # 推断语言
                lang = 'en'
                if len(path_parts) > 1 and path_parts[1] in ['zh-cn', 'zh', 'en']:
                    lang = path_parts[1]
                
                # 获取Git状态
                g_stat = "clean"
                norm = rel_path.replace('/', os.sep)
                if norm in git_map:
                    g_stat = git_map[norm]

                # 解析frontmatter
                title = f
                is_draft = False
                date_str = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d')
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f_obj:
                        content = f_obj.read()
                        if content.startswith('---'):
                            parts = content.split('---', 2)
                            if len(parts) >= 3:
                                for line in parts[1].splitlines():
                                    line = line.strip()
                                    if line.startswith('title:'): 
                                        title = line.split(':', 1)[1].strip().strip('"')
                                    if line.startswith('draft:') and 'true' in line.lower(): 
                                        is_draft = True
                                    if line.startswith('date:'):
                                        date_raw = line.split(':', 1)[1].strip().strip('"')
                                        try:
                                            date_str = date_raw[:10]
                                        except:
                                            pass
                except:
                    pass

                # 确定状态
                status = "PUBLISHED"
                color = "#22c55e"
                if is_draft:
                    status = "DRAFT"
                    color = "#eab308"
                elif g_stat in ['M', 'A', '??']:
                    status = "UNSAVED"
                    color = "#f97316"

                posts.append({
                    "title": title,
                    "lang": lang,
                    "path": rel_path,
                    "date": date_str,
                    "status": status,
                    "status_color": color
                })
                
        return sorted(posts, key=lambda x: x['date'], reverse=True)[:50]

    def create_sync_post(self, data):
        """创建双语文章"""
        title_zh = data['title']
        categories = data.get('categories', '')
        title_en = translate_text(title_zh)
        filename = "".join(x for x in title_en.lower() if x.isalnum() or x == ' ').replace(' ', '-')
        
        results = {}
        try:
            zh_path = f"content/zh-cn/post/{filename}/index.md"
            subprocess.run(["hugo", "new", zh_path], check=True, capture_output=True, timeout=10)
            self.update_frontmatter(zh_path, title_zh, categories)
            results['zh_path'] = zh_path
            
            en_path = f"content/en/post/{filename}/index.md"
            subprocess.run(["hugo", "new", en_path], check=True, capture_output=True, timeout=10)
            self.update_frontmatter(en_path, title_en, categories)
            results['en_path'] = en_path
            return True, results
        except Exception as e:
            return False, {"message": str(e)}

    def update_frontmatter(self, path, title, categories):
        """更新文章frontmatter"""
        try:
            full_path = os.path.join(HUGO_PATH, path)
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                if line.startswith('title:'):
                    new_lines.append(f'title: "{title}"\n')
                elif line.startswith('categories:'):
                    cats = [c.strip() for c in categories.split(',')] if categories else []
                    new_lines.append(f'categories: {json.dumps(cats)}\n')
                else:
                    new_lines.append(line)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        except:
            pass

    def handle_command(self, cmd):
        """处理命令"""
        if cmd == 'preview':
            try:
                subprocess.Popen(["hugo", "server", "--disableFastRender", "--bind", "127.0.0.1"], 
                               shell=True, cwd=HUGO_PATH)
            except:
                pass
            return {"message": "Server launching...", "url": "http://localhost:1313/WangScape/"}
        elif cmd == 'deploy':
            try:
                subprocess.run(["git", "add", "."], check=True, timeout=10)
                subprocess.run(["git", "commit", "-m", "Web Update"], check=True, timeout=10)
                subprocess.run(["git", "push"], check=True, timeout=30)
                return {"message": "Deployed successfully"}
            except Exception as e:
                return {"message": f"Deploy failed: {e}"}
        return {"message": "Unknown command"}

def start_server():
    """启动服务器"""
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), HugoHandler) as httpd:
        print(f"WangScape Writer Online: http://127.0.0.1:{PORT}")
        webbrowser.open(f"http://127.0.0.1:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
