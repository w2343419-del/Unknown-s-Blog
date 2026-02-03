package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

// CommentRequest 评论请求结构
type CommentRequest struct {
	PostPath     string   `json:"post_path"`
	PostTitle    string   `json:"post_title"`
	Author       string   `json:"author"`
	Email        string   `json:"email"`
	Content      string   `json:"content"`
	ParentID     string   `json:"parent_id"`
	UseGithub    bool     `json:"use_github"`
	GithubRepo   string   `json:"github_repo"`
	GithubLabels []string `json:"github_labels"`
}

// GitHubIssue GitHub Issue结构
type GitHubIssue struct {
	Title  string   `json:"title"`
	Body   string   `json:"body"`
	Labels []string `json:"labels"`
}

// APIResponse API响应结构
type APIResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	Data    any    `json:"data,omitempty"`
}

var (
	githubToken = os.Getenv("GITHUB_TOKEN") // GitHub Personal Access Token
	corsOrigin  = os.Getenv("CORS_ORIGIN")  // 允许的CORS源，例如: https://yourdomain.com
)

func main() {
	if githubToken == "" {
		log.Println("警告: 未设置 GITHUB_TOKEN 环境变量")
	}

	http.HandleFunc("/api/submit_comment", corsMiddleware(submitCommentHandler))
	http.HandleFunc("/health", healthHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("评论API服务器启动在端口 %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}

// CORS中间件
func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		origin := r.Header.Get("Origin")
		
		// 设置CORS头
		if corsOrigin != "" {
			w.Header().Set("Access-Control-Allow-Origin", corsOrigin)
		} else if origin != "" {
			// 开发环境允许所有源（生产环境应该设置具体的域名）
			w.Header().Set("Access-Control-Allow-Origin", origin)
		}
		
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Access-Control-Max-Age", "3600")

		// 处理OPTIONS预检请求
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next(w, r)
	}
}

// 健康检查
func healthHandler(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(map[string]string{
		"status": "ok",
		"time":   time.Now().Format(time.RFC3339),
	})
}

// 提交评论处理器
func submitCommentHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")

	if r.Method != http.MethodPost {
		respondError(w, "仅支持POST请求", http.StatusMethodNotAllowed)
		return
	}

	var req CommentRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, "无效的请求数据: "+err.Error(), http.StatusBadRequest)
		return
	}

	// 验证必填字段
	if req.Author == "" || req.Email == "" || req.Content == "" || req.PostPath == "" {
		respondError(w, "缺少必填字段", http.StatusBadRequest)
		return
	}

	// 如果使用GitHub，创建Issue
	if req.UseGithub && req.GithubRepo != "" {
		if err := createGitHubIssue(req); err != nil {
			log.Printf("创建GitHub Issue失败: %v", err)
			respondError(w, "提交到GitHub失败: "+err.Error(), http.StatusInternalServerError)
			return
		}

		respondSuccess(w, "评论已提交到GitHub，等待审核", nil)
		return
	}

	// 如果不使用GitHub，返回错误（你可以在这里添加其他存储方式）
	respondError(w, "当前仅支持GitHub评论", http.StatusNotImplemented)
}

// 创建GitHub Issue
func createGitHubIssue(req CommentRequest) error {
	if githubToken == "" {
		return fmt.Errorf("未配置GitHub Token")
	}

	// 构建Issue标题和内容
	title := fmt.Sprintf("[Comment] %s", req.PostTitle)
	
	bodyParts := []string{
		fmt.Sprintf("Post: %s", req.PostPath),
		fmt.Sprintf("Author: %s", req.Author),
		fmt.Sprintf("Email: %s", req.Email),
	}
	
	if req.ParentID != "" {
		bodyParts = append(bodyParts, fmt.Sprintf("Parent ID: %s", req.ParentID))
	}
	
	bodyParts = append(bodyParts, "", "Content:", req.Content)
	body := strings.Join(bodyParts, "\n")

	// 准备GitHub Issue数据
	issue := GitHubIssue{
		Title:  title,
		Body:   body,
		Labels: req.GithubLabels,
	}

	jsonData, err := json.Marshal(issue)
	if err != nil {
		return fmt.Errorf("序列化Issue数据失败: %w", err)
	}

	// 调用GitHub API
	apiURL := fmt.Sprintf("https://api.github.com/repos/%s/issues", req.GithubRepo)
	httpReq, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("创建请求失败: %w", err)
	}

	httpReq.Header.Set("Authorization", "Bearer "+githubToken)
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Accept", "application/vnd.github.v3+json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(httpReq)
	if err != nil {
		return fmt.Errorf("请求GitHub API失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("GitHub API返回错误 (状态码 %d): %s", resp.StatusCode, string(bodyBytes))
	}

	log.Printf("成功创建GitHub Issue - 作者: %s, 文章: %s", req.Author, req.PostPath)
	return nil
}

// 响应错误
func respondError(w http.ResponseWriter, message string, statusCode int) {
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(APIResponse{
		Success: false,
		Message: message,
	})
}

// 响应成功
func respondSuccess(w http.ResponseWriter, message string, data any) {
	json.NewEncoder(w).Encode(APIResponse{
		Success: true,
		Message: message,
		Data:    data,
	})
}
