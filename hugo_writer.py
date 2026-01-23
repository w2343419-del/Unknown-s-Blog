import os
import subprocess
import http.server
import socketserver
import json
import webbrowser
import threading
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote
import urllib.request

PORT = 8080
HUGO_PATH = os.getcwd()

# 简单的翻译函数
def translate_text(text, source_lang='zh', target_lang='en'):
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={source_lang}|{target_lang}"
        with urllib.request.urlopen(url) as response:
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
            /* DASHBOARD THEME (Dark) */
            --dash-bg: #0a0a0a;
            --dash-sidebar: #141414;
            --dash-text: #ffffff;
            --dash-text-dim: #888888;
            --dash-accent: #00ffcc; /* Teal accent from screenshot */
            --dash-border: rgba(255,255,255,0.1);

            /* EDITOR THEME (Light/Office) */
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

        /* === VIEW SWITCHING === */
        .view-section {
            display: none;
            width: 100%;
            height: 100%;
        }
        .view-section.active {
            display: flex;
        }

        /* ============================
           VIEW 1: DASHBOARD (Dark) 
           ============================ */
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
            transform: translateY(-1px);
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
        
        .dpi-title { font-size: 16px; font-weight: 600; color: var(--dash-text); margin-bottom: 5px; }
        .dpi-meta { font-size: 12px; color: var(--dash-text-dim); font-family: monospace; }
        .dpi-status { color: var(--dash-accent); font-size: 12px; font-weight: 600; }

        /* ============================
           VIEW 2: EDITOR (Light/Office)
           ============================ */
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
        .word-back-btn:hover { background: rgba(255,255,255,0.3); }

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

        .word-sidebar {
            width: 240px;
            background: white;
            border-right: 1px solid var(--word-border);
            overflow-y: auto;
            border-left: 5px solid #e1dfdd; 
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
        }

        .wp-title { font-family: 'Sitka Small', serif; font-size: 32px; font-weight: 700; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }
        .wp-content { font-family: 'Inter', sans-serif; line-height: 1.8; color: #333; }

        /* Modal & Utils */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
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
        .modal-card button { padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; }
        .btn-confirm { background: var(--dash-accent); color: black; border:none; }
        .btn-cancel { background: transparent; color: #ccc; border: 1px solid #555; margin-right: 10px; }

    </style>
</head>
<body>

    <!-- VIEW 1: DASHBOARD -->
    <div id="dashboard-view" class="view-section active">
        <div class="dash-sidebar">
            <div class="dash-logo">WangScape助手</div>
            
            <button class="dash-btn primary" onclick="openCreateModal()">
                <span>+</span> 新建文章 (双语同步)
            </button>
            <button class="dash-btn" onclick="runCommand('preview')">
                <span>🌍</span> 启动实时预览
            </button>
            <button class="dash-btn" onclick="runCommand('deploy')">
                <span>🚀</span> 一键提交推送
            </button>
            <button class="dash-btn" onclick="location.reload()">
                <span>🔄</span> 刷新列表
            </button>
            
            <div style="margin-top:auto; font-size:12px; color:var(--dash-text-dim);">
                系统状态: <span style="color:#22c55e">在线</span><br>
                v2.5 Hybrid UI
            </div>
        </div>
        
        <div class="dash-main">
            <h1 class="dash-header">最新博文内容</h1>
            <div id="dash-post-list" class="post-list-card">
                <!-- Posts go here -->
            </div>
        </div>
    </div>

    <!-- VIEW 2: EDITOR (OFFICE STYLE) -->
    <div id="editor-view" class="view-section">
        <div class="word-topbar">
            <div style="display:flex; align-items:center; gap:15px;">
                <button class="word-back-btn" onclick="switchView('dashboard')">← Back to Dashboard</button>
                <strong style="font-size:16px;">WangScape Writer</strong>
            </div>
            <div>
                <span id="current-doc-name" style="opacity:0.8; margin-right:20px; font-size:13px;"></span>
                <span id="save-status" style="font-size:12px; margin-right:15px; color:#ddd;"></span>
                <button class="word-back-btn" onclick="toggleLang()" style="display:inline-flex;">EN / 中</button>
            </div>
        </div>
        
        <div class="word-ribbon">
            <button class="word-rib-btn" onclick="saveDocument()">
                <span>💾</span> Save
            </button>
            <button class="word-rib-btn" onclick="runCommand('deploy')">
                <span>🚀</span> Publish
            </button>
            <button class="word-rib-btn" onclick="runCommand('preview')">
                <span>👁</span> Preview Site
            </button>
        </div>

        <div class="word-workspace">
            <div class="word-canvas">
                <div class="word-paper" id="paper-content">
                    <div style="text-align:center; color:#999; margin-top:100px;">
                        Select a document to edit.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ... Create Modal ... -->

    <script>
        let postsData = [];
        let currentDocPath = '';

        function switchView(viewName) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
            document.getElementById(viewName + '-view').classList.add('active');
            if(viewName === 'dashboard') fetchPosts(); // Refresh list on return
        }

        async function init() {
            await fetchPosts();
        }

        async function fetchPosts() {
            const res = await fetch('/api/posts');
            postsData = await res.json();
            renderDashboardList();
        }

        function renderDashboardList() {
            const list = document.getElementById('dash-post-list');
            list.innerHTML = postsData.map(p => `
                <div class="dash-post-item">
                    <div onclick="openEditor('${p.path}', '${p.title}', '${p.date}')" style="flex:1; cursor:pointer;">
                        <div class="dpi-title">${p.title}</div>
                        <div class="dpi-meta">${p.date} · ${p.lang.toUpperCase()} · ${p.path}</div>
                    </div>
                    <div style="display:flex; gap:10px; align-items:center;">
                         <button onclick="deleteDocument('${p.path}')" style="background:transparent; border:1px solid #333; color:#666; width:24px; height:24px; border-radius:4px; cursor:pointer; display:flex; align-items:center; justify-content:center;">🗑</button>
                         <div class="dpi-status">已就绪</div>
                    </div>
                </div>
            `).join('');
        }

        async function openEditor(path, title, date) {
            currentDocPath = path;
            switchView('editor');
            document.getElementById('current-doc-name').textContent = title;
            const paper = document.getElementById('paper-content');
            paper.innerHTML = `<div style="text-align:center; margin-top:50px; color:#888;">Loading...</div>`;
            
            try {
                const res = await fetch('/api/get_content?path=' + encodeURIComponent(path));
                const data = await res.json();
                
                // Use a textarea for editing
                paper.innerHTML = `
                    <div class="wp-title">${title}</div>
                    <div style="font-size:12px; color:#999; margin-bottom:20px;">Date: ${date}</div>
                    <textarea id="editor-textarea" spellcheck="false" 
                        style="width:100%; height:800px; border:none; resize:none; outline:none; font-family:'Inter', monospace; font-size:15px; line-height:1.6; color:#333;">${data.content}</textarea>
                `;
            } catch(e) {
                paper.innerHTML = `<div style="color:red">Error loading content: ${e}</div>`;
            }
        }

        async function saveDocument() {
            if(!currentDocPath) return;
            const content = document.getElementById('editor-textarea').value;
            const statusEl = document.getElementById('save-status');
            statusEl.textContent = "Saving...";
            
            try {
                const res = await fetch('/api/save_content', {
                    method: 'POST',
                    body: JSON.stringify({ path: currentDocPath, content: content })
                });
                const data = await res.json();
                if(data.success) {
                    statusEl.textContent = "Saved " + new Date().toLocaleTimeString();
                    setTimeout(() => statusEl.textContent = "", 3000);
                } else {
                    alert("Save failed: " + data.message);
                }
            } catch(e) { alert("Err: " + e); }
        }

        async function deleteDocument(path) {
            if(!confirm("确定要删除这篇文章吗？操作不可恢复。\\nAre you sure you want to delete this post?")) return;
            
            try {
                const res = await fetch('/api/delete_post', {
                    method: 'POST',
                    body: JSON.stringify({ path: path })
                });
                const data = await res.json();
                if(data.success) {
                    fetchPosts(); // Reload list
                } else {
                    alert("Delete failed: " + data.message);
                }
            } catch(e) { alert("Err: " + e); }
        }

        // --- COMMANDS & CREATION ---
        function openCreateModal() { document.getElementById('create-modal').style.display = 'flex'; }
        function closeCreateModal() { document.getElementById('create-modal').style.display = 'none'; }
        
        async function createPost() {
            const title = document.getElementById('postTitle').value;
            const cat = document.getElementById('postCat').value;
            if(!title) return alert('请输入标题');
            
            try {
                const res = await fetch('/api/create_sync', {
                    method: 'POST',
                    body: JSON.stringify({ title, categories: cat })
                });
                const data = await res.json();
                if(data.success) {
                    closeCreateModal();
                    await fetchPosts();
                    alert('创建成功！请在列表中点击编辑。');
                } else {
                    alert('失败: ' + data.message);
                }
            } catch(e) { alert('Err: ' + e); }
        }

        async function runCommand(cmd) {
            const res = await fetch('/api/command?name=' + cmd);
            const data = await res.json();
            alert('系统: ' + data.message);
        }
        
        function toggleLang() {
            alert("界面语言切换功能将在下一次更新中完善\\nUI Language toggle coming next update");
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

    def get_content(self, rel_path):
        try:
            full_path = os.path.join(HUGO_PATH, rel_path)
            if not os.path.exists(full_path):
                return "File not found."
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode())
        
        if self.path == '/api/create_sync':
            success, result = self.create_sync_post(post_data)
            self.send_json({"success": success, **result})
        elif self.path == '/api/save_content':
            success, msg = self.save_content(post_data)
            self.send_json({"success": success, "message": msg})
        elif self.path == '/api/delete_post':
            success, msg = self.delete_post(post_data)
            self.send_json({"success": success, "message": msg})
        else:
            self.send_error(404)

    def save_content(self, data):
        try:
            rel_path = data.get('path')
            content = data.get('content')
            full_path = os.path.join(HUGO_PATH, rel_path)
            
            # Ensure we are saving to a valid path inside HUGO_PATH
            if not os.path.abspath(full_path).startswith(HUGO_PATH):
                return False, "Invalid path security violation"

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Saved successfully"
        except Exception as e:
            return False, str(e)

    def delete_post(self, data):
        try:
            rel_path = data.get('path')
            full_path = os.path.join(HUGO_PATH, rel_path)
            
            # Security check
            if not os.path.abspath(full_path).startswith(HUGO_PATH):
                return False, "Invalid path security violation"

            # If it's an index.md in a leaf bundle, deleting the folder might be cleaner
            # But for safety, let's just delete the file.
            # Or better, if the parent folder matches the slug and only contains this file, delete the folder.
            parent_dir = os.path.dirname(full_path)
            
            if os.path.exists(full_path):
                os.remove(full_path)
                
            # Check if parent dir is empty now, if so remove it (cleanup leaf bundles)
            if os.listdir(parent_dir) == []:
                 os.rmdir(parent_dir)

            return True, "Deleted successfully"
        except Exception as e:
            return False, str(e)

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def get_posts(self):
        posts = []
        for lang in ['zh-cn', 'en']:
            dir_path = os.path.join(HUGO_PATH, 'content', lang, 'post')
            if not os.path.exists(dir_path): continue
            for root, dirs, files in os.walk(dir_path):
                for f in files:
                    if f.endswith('.md'):
                        rel_path = os.path.relpath(os.path.join(root, f), HUGO_PATH)
                        posts.append({
                            "title": f if f != 'index.md' else os.path.basename(root),
                            "lang": lang,
                            "path": rel_path,
                            "date": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, f))).strftime('%Y-%m-%d')
                        })
        return sorted(posts, key=lambda x: x['date'], reverse=True)[:15]

    def create_sync_post(self, data):
        title_zh = data['title']
        categories = data['categories']
        
        # 自动翻译标题
        title_en = translate_text(title_zh)
        
        # 生成安全的文件名
        filename = "".join(x for x in title_en.lower() if x.isalnum() or x == ' ').replace(' ', '-')
        
        results = {}
        
        try:
            # 创建中文版
            zh_path = f"content/zh-cn/post/{filename}/index.md"
            subprocess.run(["hugo", "new", zh_path], check=True, capture_output=True)
            self.update_frontmatter(zh_path, title_zh, categories)
            results['zh_path'] = zh_path
            
            # 创建英文版
            en_path = f"content/en/post/{filename}/index.md"
            subprocess.run(["hugo", "new", en_path], check=True, capture_output=True)
            self.update_frontmatter(en_path, title_en, categories)
            results['en_path'] = en_path
            
            return True, results
        except Exception as e:
            return False, {"message": str(e)}

    def update_frontmatter(self, path, title, categories):
        try:
            full_path = os.path.join(HUGO_PATH, path)
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                if line.startswith('title:'):
                    new_lines.append(f'title: "{title}"\\n')
                elif line.startswith('categories:'):
                    cats = [c.strip() for c in categories.split(',')]
                    new_lines.append(f'categories: {json.dumps(cats)}\\n')
                else:
                    new_lines.append(line)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"Error updating frontmatter: {e}")

    def handle_command(self, cmd):
        if cmd == 'preview':
            subprocess.Popen(["hugo", "server"], shell=True)
            return "Server start command issued."
        elif cmd == 'deploy':
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Post update via Writer"], check=True)
                subprocess.run(["git", "push"], check=True)
                return "Deployed successfully."
            except Exception as e:
                return f"Deploy failed: {str(e)}"
        return "Unknown command"

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), HugoHandler) as httpd:
        print(f"WangScape Writer Online: http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()

