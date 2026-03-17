import re

# 读取原始 index.html
with open('d:\\数维创擎\\代码库\\数维数据管家系统\\frontend\\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 添加 head 部分的引入
head_pattern = r'(<head>.*?)(<style>)'
head_replacement = r'''
\1
    <link rel="stylesheet" href="ui-common.css">
    <style>
        .container-main {
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 40px;
            position: relative;
            z-index: 1;
        }

        .header-glass {
            text-align: center;
            margin-bottom: 40px;
        }

        .header-glass h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 20px rgba(0, 210, 255, 0.3);
            color: white;
        }

        .header-glass p {
            font-size: 16px;
            opacity: 0.8;
            color: white;
        }

        .header-info-glass {
            margin-top: 20px;
            padding: 16px;
            background: rgba(0, 210, 255, 0.1);
            border-radius: 12px;
            border-left: 3px solid #00D2FF;
        }

        .nav-bar-glass {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        .nav-item-glass {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: white;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.3s ease;
        }

        .nav-item-glass:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: #00D2FF;
        }

        .nav-item-glass.primary {
            background: rgba(0, 210, 255, 0.2);
            border-color: rgba(0, 210, 255, 0.4);
            color: white;
        }

        .nav-item-glass.primary:hover {
            background: rgba(0, 210, 255, 0.4);
            border-color: #00D2FF;
        }

        .nav-item-glass.danger {
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.3);
            color: #EF4444;
        }

        .step-indicator-glass {
            display: flex;
            justify-content: space-between;
            margin-bottom: 32px;
            position: relative;
            padding: 0 20px;
        }

        .step-indicator-glass::before {
            content: '';
            position: absolute;
            top: 18px;
            left: 40px;
            right: 40px;
            height: 2px;
            background: rgba(255, 255, 255, 0.2);
            z-index: 1;
        }

        .step-indicator-glass .progress-line-glass {
            position: absolute;
            top: 18px;
            left: 40px;
            height: 2px;
            background: linear-gradient(90deg, #00D2FF, #4ECDC4);
            z-index: 2;
            transition: width 0.5s ease;
            width: 0%;
        }

        .step-glass {
            text-align: center;
            position: relative;
            z-index: 3;
            flex: 1;
        }

        .step-circle-glass {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: rgba(255, 255, 255, 0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 8px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .step-glass.active .step-circle-glass {
            background: #00D2FF;
            border-color: #00D2FF;
            color: white;
            box-shadow: 0 0 0 4px rgba(0, 210, 255, 0.15);
        }

        .step-glass.completed .step-circle-glass {
            background: #10B981;
            border-color: #10B981;
            color: white;
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
        }

        .step-label-glass {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.6);
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .step-glass.active .step-label-glass {
            color: white;
            font-weight: 600;
        }

        .step-glass.completed .step-label-glass {
            color: #10B981;
        }

        .progress-section-glass {
            margin-bottom: 32px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .progress-header-glass {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .progress-label-glass {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 500;
        }

        .progress-value-glass {
            font-family: "Roboto Mono", monospace;
            font-size: 14px;
            font-weight: 600;
            color: #00D2FF;
        }

        .progress-segmented-glass {
            display: flex;
            justify-content: space-between;
            gap: 4px;
        }

        .progress-node-glass {
            flex: 1;
            height: 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .progress-node-glass.completed {
            background: #10B981;
            box-shadow: 0 0 6px rgba(16, 185, 129, 0.3);
        }

        .progress-node-glass.active {
            background: #00D2FF;
            animation: node-pulse 1.5s ease-in-out infinite;
        }

        @keyframes node-pulse {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
        }

        .section-title-glass {
            color: white;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
            padding-left: 16px;
            border-left: 4px solid #00D2FF;
            letter-spacing: -0.3px;
        }

        .section-desc-glass {
            color: rgba(255, 255, 255, 0.6);
            font-size: 14px;
            margin-bottom: 24px;
            padding-left: 20px;
        }

        .form-question-glass {
            margin-bottom: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            border-left: 3px solid #00D2FF;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }

        .form-question-glass:hover {
            background: rgba(0, 210, 255, 0.05);
            border-color: rgba(0, 210, 255, 0.2);
        }

        .question-label-glass {
            font-weight: 600;
            color: white;
            margin-bottom: 12px;
            font-size: 14px;
            display: block;
        }

        .required-mark-glass {
            color: #FF6B6B;
            margin-left: 4px;
        }

        .form-control-glass {
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: white;
            background: rgba(255, 255, 255, 0.08);
            transition: all 0.2s ease;
        }

        .form-control-glass:focus {
            border-color: #00D2FF;
            box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.1);
            outline: none;
            background: rgba(255, 255, 255, 0.12);
        }

        .form-control-glass::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }

        .form-check-glass {
            margin-bottom: 8px;
        }

        .form-check-input-glass {
            width: 18px;
            height: 18px;
            margin-top: 0;
            cursor: pointer;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .form-check-input-glass:checked {
            background-color: #00D2FF;
            border-color: #00D2FF;
        }

        .form-check-input-glass:focus {
            box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.15);
        }

        .form-check-label-glass {
            font-size: 14px;
            color: white;
            cursor: pointer;
            margin-left: 4px;
        }

        .other-input-wrapper-glass {
            margin-top: 12px;
            padding: 12px 16px;
            background: rgba(0, 210, 255, 0.05);
            border-radius: 8px;
            border-left: 3px solid #00D2FF;
        }

        .other-input-wrapper-glass input,
        .other-input-wrapper-glass textarea {
            border: 1px dashed #00D2FF;
            background: rgba(255, 255, 255, 0.05);
        }

        .other-input-wrapper-glass input:focus,
        .other-input-wrapper-glass textarea:focus {
            border-style: solid;
            border-color: #00D2FF;
        }

        .other-input-label-glass {
            font-size: 12px;
            color: #00D2FF;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .btn-custom-glass {
            padding: 12px 28px;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.2s ease;
            font-size: 14px;
            border: none;
        }

        .btn-custom-glass:active {
            transform: scale(0.98);
        }

        .btn-primary-glass {
            background: linear-gradient(135deg, #1B3A57 0%, #00D2FF 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(27, 58, 87, 0.25);
        }

        .btn-primary-glass:hover {
            box-shadow: 0 6px 20px rgba(27, 58, 87, 0.35);
            transform: translateY(-2px);
            color: white;
        }

        .btn-secondary-glass {
            background: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .btn-secondary-glass:hover {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border-color: #00D2FF;
        }

        .btn-success-glass {
            background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
        }

        .btn-success-glass:hover {
            box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
            transform: translateY(-2px);
            color: white;
        }

        .btn-success-glass::after {
            content: " ✓";
            display: inline-block;
        }

        .loading-overlay-glass {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(11, 17, 32, 0.95);
            display: none;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            z-index: 9999;
        }

        .loading-overlay-glass.active {
            display: flex;
        }

        .engine-breathing-glass {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: radial-gradient(circle, 
                rgba(0, 210, 255, 0.4) 0%, 
                transparent 70%);
            animation: engine-breathe-glass 2s ease-in-out infinite;
            margin-bottom: 24px;
        }

        @keyframes engine-breathe-glass {
            0%, 100% { transform: scale(0.95); opacity: 0.6; }
            50% { transform: scale(1.1); opacity: 1; }
        }

        .loading-text-glass {
            color: white;
            font-size: 16px;
            font-weight: 500;
        }

        .loading-subtext-glass {
            color: #00D2FF;
            font-size: 13px;
            margin-top: 8px;
        }

        .nav-vip-badge-glass {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: linear-gradient(135deg, #FF9F43 0%, #F7931A 100%);
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
        }

        .nav-vip-badge-glass i {
            font-size: 10px;
        }

        @media (max-width: 768px) {
            .container-main {
                padding: 40px 20px;
            }

            .step-indicator-glass {
                padding: 0;
            }

            .step-indicator-glass::before {
                left: 18px;
                right: 18px;
            }

            .step-indicator-glass .progress-line-glass {
                left: 18px;
            }

            .step-circle-glass {
                width: 32px;
                height: 32px;
                font-size: 12px;
            }

            .step-label-glass {
                font-size: 10px;
            }

            .form-question-glass {
                padding: 16px;
            }

            .glass-section {
                padding: 24px 20px;
            }
        }
'''
content = re.sub(head_pattern, head_replacement, content, flags=re.DOTALL)

# 2. 修改 body 样式
body_pattern = r'(body\s*\{[^}]*\})'
body_replacement = r'''body {
            font-family: var(--font-family-zh);
            background: linear-gradient(135deg, #0a192f 0%, #0f172a 50%, #1e293b 100%);
            min-height: 100vh;
            padding: 0;
            margin: 0;
        }'''
content = re.sub(body_pattern, body_replacement, content)

# 3. 替换类名
replacements = [
    ('class="container" style="max-width: 900px;"', 'class="container-main"'),
    ('class="header-section"', 'class="header-glass"'),
    ('class="header-title"', 'class=""'),
    ('class="header-subtitle"', 'class=""'),
    ('class="header-info"', 'class="header-info-glass"'),
    ('class="form-container"', 'class="glass-section"'),
    ('class="step-indicator"', 'class="step-indicator-glass"'),
    ('class="progress-line"', 'class="progress-line-glass"'),
    ('class="step "', 'class="step-glass '),
    ('class="step active"', 'class="step-glass active"'),
    ('class="step-circle"', 'class="step-circle-glass"'),
    ('class="step-label"', 'class="step-label-glass"'),
    ('class="progress-section"', 'class="progress-section-glass"'),
    ('class="progress-header"', 'class="progress-header-glass"'),
    ('class="progress-label"', 'class="progress-label-glass"'),
    ('class="progress-value"', 'class="progress-value-glass"'),
    ('class="progress-segmented"', 'class="progress-segmented-glass"'),
    ('class="progress-node"', 'class="progress-node-glass"'),
    ('class="section-title"', 'class="section-title-glass"'),
    ('class="section-desc"', 'class="section-desc-glass"'),
    ('class="form-question"', 'class="form-question-glass"'),
    ('class="question-label"', 'class="question-label-glass"'),
    ('class="required-mark"', 'class="required-mark-glass"'),
    ('class="form-control"', 'class="form-control form-control-glass"'),
    ('class="form-select"', 'class="form-select form-control-glass"'),
    ('class="form-check-input"', 'class="form-check-input form-check-input-glass"'),
    ('class="form-check-label"', 'class="form-check-label form-check-label-glass"'),
    ('class="form-check"', 'class="form-check form-check-glass"'),
    ('class="other-input-wrapper"', 'class="other-input-wrapper-glass"'),
    ('class="other-input-label"', 'class="other-input-label-glass"'),
    ('class="loading-overlay"', 'class="loading-overlay-glass"'),
    ('class="engine-breathing"', 'class="engine-breathing-glass"'),
    ('class="loading-text"', 'class="loading-text-glass"'),
    ('class="loading-subtext"', 'class="loading-subtext-glass"'),
    ('class="nav-vip-badge"', 'class="nav-vip-badge-glass"'),
    ('class="btn-primary-custom"', 'class="btn-primary-glass btn-custom-glass"'),
    ('class="btn-secondary-custom"', 'class="btn-secondary-glass btn-custom-glass"'),
    ('class="btn-success-custom"', 'class="btn-success-glass btn-custom-glass"'),
    ('class="btn-custom"', 'class="btn-custom-glass"'),
]

for old, new in replacements:
    content = content.replace(old, new)

# 4. 添加 Canvas 和 body 开始
body_start_pattern = r'(<body>)(.*?)(<div class="container-main">)'
body_start_replacement = r'''\1
    <canvas id="particles-canvas"></canvas>
    \3'''
content = re.sub(body_start_pattern, body_start_replacement, content, flags=re.DOTALL)

# 5. 替换导航栏
nav_pattern = r'<!-- 顶部导航 -->.*?</div>'
nav_replacement = '''<!-- 顶部导航 -->
        <div class="nav-bar-glass">
            <div class="d-flex align-items-center gap-2">
                <span style="font-size: 13px; color: rgba(255, 255, 255, 0.6);">
                    <i class="bi bi-person-circle"></i>
                    <span id="navUserName">游客</span>
                </span>
            </div>
            <div class="d-flex gap-2">
                <a href="/history" class="nav-item-glass primary">
                    <i class="bi bi-clock-history"></i> 历史报告
                </a>
                <button id="navLogoutBtn" onclick="handleLogout()" class="nav-item-glass danger" style="display: none;">
                    <i class="bi bi-box-arrow-right"></i> 退出
                </button>
                <a id="navLoginBtn" href="/login" class="nav-item-glass">
                    <i class="bi bi-box-arrow-in-right"></i> 登录
                </a>
            </div>
        </div>'''
content = re.sub(nav_pattern, nav_replacement, content, flags=re.DOTALL)

# 6. 在 body 结束前添加脚本引用
script_pattern = r'(<script src="https://cdn\.jsdelivr\.net/npm/bootstrap@5\.1\.3/dist/js/bootstrap\.bundle\.min\.js"></script>)'
script_replacement = r'''\1
    <script src="ui-particles.js"></script>
    <script src="form.js"></script>'''
content = re.sub(script_pattern, script_replacement, content)

# 7. 添加粒子初始化和导航状态检查
init_pattern = r'(</script>)(\s*</body>)'
init_replacement = r'''
        // 初始化完整性显示
        document.addEventListener('DOMContentLoaded', function() {
            updateCompletenessValue(50);
            checkNavAuth();
            // 初始化粒子背景
            initParticleBackground('particles-canvas', {
                particleCount: 80,
                particleColor: 'rgba(0, 210, 255, 0.6)',
                lineColor: 'rgba(0, 210, 255, 0.2)'
            });
        });
        
        // 检查导航栏登录状态
        function checkNavAuth() {
            const token = localStorage.getItem('token');
            const userInfo = localStorage.getItem('userInfo');
            
            const navUserName = document.getElementById('navUserName');
            const navLoginBtn = document.getElementById('navLoginBtn');
            const navLogoutBtn = document.getElementById('navLogoutBtn');
            
            if (token && userInfo) {
                try {
                    const user = JSON.parse(userInfo);
                    navUserName.textContent = user.username;
                    navLoginBtn.style.display = 'none';
                    navLogoutBtn.style.display = 'inline-block';
                    
                    // 显示VIP状态
                    showVipStatus(user);
                } catch(e) {
                    navUserName.textContent = '游客';
                }
            } else {
                navUserName.textContent = '游客';
                navLoginBtn.style.display = 'inline-block';
                navLogoutBtn.style.display = 'none';
            }
            
            // 异步刷新用户信息
            refreshUserInfoAsync();
        }
        
        function showVipStatus(user) {
            const navUserName = document.getElementById('navUserName');
            const existingBadge = document.getElementById('navVipBadge');
            if (existingBadge) existingBadge.remove();
            
            if (user.is_vip) {
                const vipBadge = document.createElement('span');
                vipBadge.id = 'navVipBadge';
                vipBadge.className = 'nav-vip-badge-glass';
                vipBadge.innerHTML = '<i class="bi bi-star-fill"></i> VIP';
                navUserName.parentNode.appendChild(vipBadge);
            }
        }
        
        async function refreshUserInfoAsync() {
            const token = localStorage.getItem('token');
            if (!token) return;
            
            try {
                const response = await fetch('/api/v1/auth/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                if (response.ok) {
                    const result = await response.json();
                    const user = result.data;
                    localStorage.setItem('userInfo', JSON.stringify(user));
                    showVipStatus(user);
                }
            } catch(e) {
                console.error('刷新用户信息失败:', e);
            }
        }
        
        // 处理退出登录
        function handleLogout() {
            localStorage.removeItem('token');
            localStorage.removeItem('userInfo');
            localStorage.removeItem('reportData');
            window.location.reload();
        }
        
        // 更新完整性数值显示（带颜色渐变）
        window.updateCompletenessValue = function(value) {
            const valueSpan = document.getElementById('completeness_value');
            const badge = document.getElementById('completeness_badge');
            
            valueSpan.textContent = value + '%';
            
            // 根据值计算颜色（从红色到绿色渐变）
            let color, bgColor;
            if (value < 30) {
                // 红色系 - 低完整性
                color = '#FF6B6B';
                bgColor = 'rgba(255, 107, 107, 0.15)';
            } else if (value < 50) {
                // 橙色系 - 较低完整性
                color = '#FF9F43';
                bgColor = 'rgba(255, 159, 67, 0.15)';
            } else if (value < 70) {
                // 黄色系 - 中等完整性
                color = '#F1C40F';
                bgColor = 'rgba(241, 196, 15, 0.15)';
            } else if (value < 85) {
                // 青色系 - 较高完整性
                color = '#00D2FF';
                bgColor = 'rgba(0, 210, 255, 0.15)';
            } else {
                // 绿色系 - 高完整性
                color = '#2ECC71';
                bgColor = 'rgba(46, 204, 113, 0.15)';
            }
            
            badge.style.background = bgColor;
            badge.style.color = color;
            badge.style.border = `1px solid ${color}`;
        };
    \2'''
content = re.sub(init_pattern, init_replacement, content, flags=re.DOTALL)

# 保存文件
with open('d:\\数维创擎\\代码库\\数维数据管家系统\\frontend\\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('改造完成！')

