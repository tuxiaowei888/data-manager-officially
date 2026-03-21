"""
FastAPI 主应用 - 数维数据管家系统
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# 配置日志系统
from config.logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

# 导入路由
from api.rules import router as rules_router
from api.evaluation import router as evaluation_router
from api.ai_rules import router as ai_rules_router
from api.knowledge import router as knowledge_router
from api.knowledge_category import router as knowledge_category_router
from api.reports import router as reports_router
from api.auth import router as auth_router
from api.channel import router as channel_router
from api.users import router as users_router
from api.config import router as config_router
from api.customers import router as customers_router
from api.ai_config import router as ai_config_router
from api.prompt_templates import router as prompt_templates_router
from api.permissions import router as permissions_router

# 创建应用
app = FastAPI(
    title="数维数据管家系统",
    description="SaaS 化数据资产评价系统 - V1.0 MVP 版本",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    docs_config={
        "persistAuthorization": True,
    }
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(rules_router)
app.include_router(evaluation_router)
app.include_router(ai_rules_router)
app.include_router(knowledge_router)
app.include_router(knowledge_category_router)
app.include_router(reports_router)
app.include_router(auth_router)
app.include_router(channel_router)
app.include_router(users_router)
app.include_router(config_router)
app.include_router(customers_router)
app.include_router(ai_config_router)
app.include_router(prompt_templates_router)
app.include_router(permissions_router)


@app.get("/")
def root():
    """根路径"""
    return {
        "name": "数维数据管家系统",
        "version": "1.0.0",
        "status": "running",
        "description": "SaaS 化数据资产评价系统"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.get("/api-docs")
def api_docs_redirect():
    """重定向到新版中文 API 文档"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api-docs-cn")


@app.get("/api-docs-cn")
def api_docs_chinese():
    """全新中文 API 文档页面"""
    return FileResponse("api_docs_chinese.html")


@app.get("/report")
def report_page():
    """报告页面"""
    return FileResponse("frontend/report.html")


@app.get("/login")
def login_page():
    """登录页面"""
    return FileResponse("frontend/login.html")


@app.get("/login.html")
def login_html_page():
    """登录页面"""
    return FileResponse("frontend/login.html")


@app.get("/home")
def home_page():
    """用户首页"""
    return FileResponse("frontend/home.html")


@app.get("/register")
def register_page():
    """注册页面"""
    return FileResponse("frontend/register.html")


@app.get("/register.html")
def register_html_page():
    """注册页面"""
    return FileResponse("frontend/register.html")


@app.get("/history")
def history_page():
    """历史报告页面"""
    return FileResponse("frontend/history.html")


@app.get("/admin")
def admin_page():
    """管理员首页"""
    return FileResponse("frontend/admin.html")


@app.get("/admin.html")
def admin_html_page():
    """管理员首页"""
    return FileResponse("frontend/admin.html")


@app.get("/rules")
def rules_page():
    """规则库管理页面"""
    return FileResponse("frontend/rules.html")


@app.get("/rules.html")
def rules_html_page():
    """规则库管理页面"""
    return FileResponse("frontend/rules.html")


@app.get("/knowledge")
def knowledge_page():
    """知识库管理页面"""
    return FileResponse("frontend/knowledge.html")


@app.get("/knowledge.html")
def knowledge_html_page():
    """知识库管理页面"""
    return FileResponse("frontend/knowledge.html")


@app.get("/users")
def users_page():
    """用户管理页面"""
    return FileResponse("frontend/users.html")


@app.get("/users.html")
def users_html_page():
    """用户管理页面"""
    return FileResponse("frontend/users.html")


@app.get("/config")
def config_page():
    """系统配置页面"""
    return FileResponse("frontend/config.html")


@app.get("/config.html")
def config_html_page():
    """系统配置页面"""
    return FileResponse("frontend/config.html")


@app.get("/test-btn.html")
def test_btn_page():
    """测试按钮页面"""
    return FileResponse("frontend/test-btn.html")


@app.get("/customers")
def customers_page():
    """客户管理页面"""
    return FileResponse("frontend/customers.html")


@app.get("/customers.html")
def customers_html_page():
    """客户管理页面"""
    return FileResponse("frontend/customers.html")


@app.get("/reports")
def reports_page():
    """报告管理页面"""
    return FileResponse("frontend/reports.html")


@app.get("/reports.html")
def reports_html_page():
    """报告管理页面"""
    return FileResponse("frontend/reports.html")


@app.get("/ai-config")
def ai_config_page():
    """AI配置管理页面"""
    return FileResponse("frontend/ai_config.html")


@app.get("/ai_config.html")
def ai_config_html_page():
    """AI配置管理页面"""
    return FileResponse("frontend/ai_config.html")


@app.get("/history")
def history_page():
    """历史记录页面"""
    return FileResponse("frontend/history.html")


@app.get("/history.html")
def history_html_page():
    """历史记录页面"""
    return FileResponse("frontend/history.html")


@app.get("/admin-new")
def admin_new_page():
    """新版管理后台首页"""
    return FileResponse("frontend/admin-new/index.html")


@app.get("/admin-new/index.html")
def admin_new_index_html_page():
    """新版管理后台首页"""
    return FileResponse("frontend/admin-new/index.html")


@app.get("/admin-new/pages/{page}")
def admin_new_pages_page(page: str):
    """新版管理后台子页面"""
    return FileResponse(f"frontend/admin-new/pages/{page}")


@app.get("/admin-new/pages/{folder}/{page}")
def admin_new_pages_folder_page(folder: str, page: str):
    """新版管理后台子页面"""
    return FileResponse(f"frontend/admin-new/pages/{folder}/{page}")


@app.get("/admin-new/pages/{page}.html")
def admin_new_pages_html_page(page: str):
    """新版管理后台子页面HTML"""
    return FileResponse(f"frontend/admin-new/pages/{page}.html")


@app.get("/admin-new/css/{file}")
def admin_new_css_page(file: str):
    """新版管理后台CSS文件"""
    return FileResponse(f"frontend/admin-new/css/{file}")


@app.get("/admin-new/js/{file}")
def admin_new_js_page(file: str):
    """新版管理后台JS文件"""
    return FileResponse(f"frontend/admin-new/js/{file}")


from fastapi.staticfiles import StaticFiles
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/favicon.ico")
async def favicon():
    """网站图标"""
    return FileResponse("frontend/favicon.svg", media_type="image/svg+xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
