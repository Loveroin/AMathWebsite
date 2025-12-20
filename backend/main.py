from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =====================================================
# Routers
# - 只在 main.py 里统一管理 prefix / tags
# - Router 文件里只写 APIRouter() + 相对路径（比如 "/login"、"/me"）
# =====================================================
from app.routers import auth, users, attempts, problems


# =====================================================
# ⚠️ 仅开发阶段用：自动建表（生产请用 Alembic）
# - 你目前用 SQLite + Base.metadata.create_all() 没问题
# - 为了让 SQLAlchemy “发现”所有模型，建议把所有 model import 一次
# =====================================================
from app.core.db import Base, engine
from app.models.user import User
from app.models.problem import Problem
from app.models.attempt import Attempt

Base.metadata.create_all(bind=engine)


# =====================================================
# Lifespan（替代 on_event）
# - FastAPI 推荐用 lifespan 处理启动/关闭逻辑
# - 将来你可以在这里初始化 Redis、加载题库缓存等
# =====================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Backend started")
    yield
    print("🛑 Backend shutdown")


# =====================================================
# FastAPI App
# =====================================================
app = FastAPI(
    title="数学刷题网站 API",
    version="0.1.0",
    lifespan=lifespan,
)

# =====================================================
# CORS
# - 开发阶段 allow_origins=["*"] OK
# - 生产环境必须收紧到你的前端域名（例如 https://xxx.com）
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Routers 注册（统一管理 prefix / tags）
# - 这样 Swagger 分组清晰，路径也不容易写重复
# =====================================================

# Auth：注册/登录
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# Users：当前用户信息等
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# Problems：题目管理/题库接口
app.include_router(
    problems.router,
    prefix="/problems",
    tags=["Problems"],
)

# Attempts：提交答案/查询做题记录
app.include_router(
    attempts.router,
    prefix="/attempts",
    tags=["Attempts"],
)

# =====================================================
# Root
# =====================================================
@app.get("/", tags=["default"])
def root():
    return {"status": "ok"}
