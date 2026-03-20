/**
 * 数维数据管家 - 管理后台通用JavaScript
 */

// API基础配置
const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * API请求封装
 */
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        }
    };

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, mergedOptions);

        if (!response.ok) {
            if (response.status === 401) {
                // Token过期或无效，跳转登录
                localStorage.removeItem('token');
                localStorage.removeItem('userInfo');
                window.location.href = '/login.html';
                throw new Error('登录已过期，请重新登录');
            }
            const errorData = await response.json();
            throw new Error(errorData.detail || '请求失败');
        }

        return await response.json();
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

/**
 * GET请求
 */
async function apiGet(endpoint) {
    return apiRequest(endpoint, { method: 'GET' });
}

/**
 * POST请求
 */
async function apiPost(endpoint, data) {
    return apiRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

/**
 * PUT请求
 */
async function apiPut(endpoint, data) {
    return apiRequest(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
}

/**
 * DELETE请求
 */
async function apiDelete(endpoint) {
    return apiRequest(endpoint, { method: 'DELETE' });
}

/**
 * 检查登录状态
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    const userInfo = localStorage.getItem('userInfo');

    if (!token || !userInfo) {
        window.location.href = '/login.html';
        return null;
    }

    try {
        const user = JSON.parse(userInfo);
        if (user.user_type !== 'admin') {
            window.location.href = '/home.html';
            return null;
        }
        return user;
    } catch (e) {
        window.location.href = '/login.html';
        return null;
    }
}

/**
 * 格式化日期
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * 格式化数字
 */
function formatNumber(num, decimals = 0) {
    if (num === null || num === undefined) return '-';
    return Number(num).toFixed(decimals);
}

/**
 * 显示提示消息
 */
function showMessage(message, type = 'info') {
    const colors = {
        success: '#2ECC71',
        error: '#FF6B6B',
        warning: '#FF9F43',
        info: '#1B3A57'
    };

    document.querySelectorAll('.toast-message').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background: ${colors[type]};
        color: white;
        border-radius: 8px;
        font-size: 14px;
        z-index: 999999;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;

    let styleEl = document.getElementById('toastAnimationStyle');
    if (!styleEl) {
        styleEl = document.createElement('style');
        styleEl.id = 'toastAnimationStyle';
        styleEl.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styleEl);
    }

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

/**
 * 加载显示
 */
function showLoading(element) {
    element.innerHTML = '<div class="loading-spinner"></div>';
    element.style.textAlign = 'center';
}

function hideLoading(element) {
    element.style.textAlign = '';
}

/**
 * 分页数据处理
 */
class Pagination {
    constructor(options) {
        this.currentPage = 1;
        this.pageSize = options.pageSize || 10;
        this.total = 0;
        this.totalPages = 0;
        this.onPageChange = options.onPageChange || (() => {});
        this.containerId = null;
    }

    setTotal(total) {
        this.total = total;
        this.totalPages = Math.ceil(total / this.pageSize);
    }

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.onPageChange(this.currentPage);
            if (this.containerId) this.render(this.containerId);
        }
    }

    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.onPageChange(this.currentPage);
            if (this.containerId) this.render(this.containerId);
        }
    }

    goToPage(page) {
        if (page >= 1 && page <= this.totalPages) {
            this.currentPage = page;
            this.onPageChange(page);
            if (this.containerId) this.render(this.containerId);
        }
    }

    render(containerId) {
        this.containerId = containerId;
        const container = document.getElementById(containerId);
        if (!container) return;

        const start = (this.currentPage - 1) * this.pageSize + 1;
        const end = Math.min(this.currentPage * this.pageSize, this.total);

        container.innerHTML = `
            <div class="pagination">
                <div class="pagination-info">
                    显示 ${start}-${end} 条，共 ${this.total} 条
                </div>
                <div class="pagination-buttons">
                    <button class="page-btn" onclick="paginationObj.prevPage()" ${this.currentPage === 1 ? 'disabled' : ''}>
                        <i class="bi bi-chevron-left"></i>
                    </button>
                    ${this.renderPageNumbers()}
                    <button class="page-btn" onclick="paginationObj.nextPage()" ${this.currentPage === this.totalPages ? 'disabled' : ''}>
                        <i class="bi bi-chevron-right"></i>
                    </button>
                </div>
            </div>
        `;
    }

    renderPageNumbers() {
        let html = '';
        const maxVisible = 5;
        let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
        let end = Math.min(this.totalPages, start + maxVisible - 1);

        if (end - start < maxVisible - 1) {
            start = Math.max(1, end - maxVisible + 1);
        }

        for (let i = start; i <= end; i++) {
            html += `<button class="page-btn ${i === this.currentPage ? 'active' : ''}" onclick="paginationObj.goToPage(${i})">${i}</button>`;
        }
        return html;
    }
}

// 全局分页对象
let paginationObj = null;

/**
 * 风险等级显示
 */
function getRiskBadge(level) {
    const badges = {
        'P0': '<span class="badge badge-danger">P0 高风险</span>',
        'P1': '<span class="badge badge-warning">P1 中风险</span>',
        'P2': '<span class="badge badge-success">P2 低风险</span>'
    };
    return badges[level] || `<span class="badge">${level || '-'}</span>`;
}

/**
 * VIP状态显示
 */
function getVipBadge(isVip) {
    return isVip
        ? '<span class="badge badge-warning">VIP</span>'
        : '<span class="badge badge-secondary">普通</span>';
}

/**
 * 用户类型显示
 */
function getUserTypeBadge(type) {
    return type === 'admin'
        ? '<span class="badge badge-info">管理员</span>'
        : '<span class="badge badge-secondary">普通用户</span>';
}

/**
 * 状态开关
 */
function createToggle(isActive, onChange) {
    return `<div class="toggle-switch ${isActive ? 'active' : ''}" onclick="${onChange}"></div>`;
}

/**
 * 空状态显示
 */
function renderEmptyState(container, message, icon = 'bi-inbox') {
    container.innerHTML = `
        <div class="empty-state">
            <i class="bi ${icon}"></i>
            <p>${message}</p>
        </div>
    `;
}

/**
 * 退出登录
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
    window.location.href = '/login.html';
}

/**
 * 获取URL参数
 */
function getUrlParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}
