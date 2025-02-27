from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.dispatch.db.session import Base, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan 시작")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(Base.metadata.tables, "@" * 100)
        print("테이블 생성 완료!")
    yield
    print("lifespan 종료")

app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*"
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하려면 "*"
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}