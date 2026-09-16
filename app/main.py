"""
FastAPI应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings

# 创建FastAPI应用
app = FastAPI(
    title="跨境电商AI全链路助手",
    description="用AI打通选品→图文→视频→运营全流程",
    version="0.1.0",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径，返回应用信息"""
    return {
        "name": "跨境电商AI全链路助手",
        "version": "0.1.0",
        "status": "开发中",
        "modules": ["选品", "图文", "视频", "运营"],
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("应用启动成功")
    logger.info(f"监听地址: {settings.app_host}:{settings.app_port}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
