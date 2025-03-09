import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ CORS 올바른 임포트
from pydantic import BaseModel
from analyzer import get_numerical_data


app = FastAPI()

# ✅ CORS 설정 추가 (프론트엔드에서 백엔드 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # 프론트엔드 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("main")

class Data(BaseModel):
    data: list

@app.post("/analyze")
async def analyze(data: Data):
    numerical_data_info = get_numerical_data(data)

    return numerical_data_info

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
