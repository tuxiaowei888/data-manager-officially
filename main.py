"""
FastAPI 主应用 - 数维数据管家系统
"""
import os
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
from api.datasets import router as datasets_router
from api.org_profiles import router as org_profiles_router
from api.subscription import router as subscription_router

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

# 配置 CORS - 从环境变量读取允许的来源
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080,http://localhost:8000")
allowed_origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()]

# 开发环境允许所有来源，生产环境限制具体域名
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
if DEBUG:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
app.include_router(datasets_router)
app.include_router(org_profiles_router)
app.include_router(subscription_router)


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
