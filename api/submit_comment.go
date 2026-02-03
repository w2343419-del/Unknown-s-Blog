package handler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
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

// Handler 是Vercel Serverless函数的入口点
func Handler(w http.ResponseWriter, r *http.Request) {
	// 设置CORS头
	origin := r.Header.Get("Origin")
	if origin != "" {
		w.Header().Set("Access-Control-Allow-Origin", origin)
	} else {
		w.Header().Set("Access-Control-Allow-Origin", "*")
	}
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	w.Header().Set("Content-Type", "application/json; charset=utf-8")

	// 处理OPTIONS预检请求
	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	// 仅接受POST请求
	if r.Method != http.MethodPost {
		respondError(w, "仅支持POST请求", http.StatusMethodNotAllowed)
		return
	}

	// 解析请求体
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

	// 创建GitHub Issue
	if req.UseGithub && req.GithubRepo != "" {
		if err := createGitHubIssue(req); err != nil {
			respondError(w, "提交到GitHub失败: "+err.Error(), http.StatusInternalServerError)
			return
		}

		respondSuccess(w, "评论已提交到GitHub，等待审核后将显示在页面上", nil)
		return
	}

	respondError(w, "当前仅支持GitHub评论", http.StatusNotImplemented)
}

// 创建GitHub Issue
func createGitHubIssue(req CommentRequest) error {
	githubToken := os.Getenv("GITHUB_TOKEN")
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
