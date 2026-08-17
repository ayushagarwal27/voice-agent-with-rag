from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import equipment

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Industrial MVP backend...")
    await connect_to_mongo()
    yield

    # Shutdown
    logger.info("🛑 Shutting down...")
    await close_mongo_connection()


app = FastAPI(
    title="Industrial MVP API",
    description="MVP version of Industrial voice bot with RAG",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(equipment.router, prefix="/api/v1/equipment", tags=["Equipment"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    def fix_binary(node):
        if isinstance(node, dict):
            if node.get("contentMediaType") == "application/octet-stream":
                del node["contentMediaType"]
                node["format"] = "binary"
            for value in node.values():
                fix_binary(value)
        elif isinstance(node, list):
            for item in node:
                fix_binary(item)

    fix_binary(schema)
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def read_root():
    return {"message": "Industrial MVP API is running", "version": "0.1.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)