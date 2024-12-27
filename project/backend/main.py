from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.user_routes import router as user_router
import uvicorn

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 允許所有來源（開發環境下），在生產環境中應設置為具體域名
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有標頭
)

# 提供靜態檔案
#app.mount("/", StaticFiles(directory="/path/to/your/frontend/dist", html=True), name="static")

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
