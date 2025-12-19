from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import auth  # 注意这里是 users，不是 user

# =========================
# ⚠️ 仅开发阶段用：自动建表
# =========================
from app.core.db import Base, engine
from app.models.user import User
from backend.app.routers import users

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    print("🚀 Backend started")
    yield
    print("🛑 Backend shutdown")


app = FastAPI(
    title="数学刷题网站 API",
    version="0.1.0",
    lifespan=lifespan,
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 开发阶段 OK，生产要收紧
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers（⚠️ 不再重复写 prefix）
# =========================
app.include_router(auth.router)
app.include_router(users.router)
# app.include_router(problem.router)

# =========================
# Root
# =========================
@app.get("/")
def root():
    return {"status": "ok"}
