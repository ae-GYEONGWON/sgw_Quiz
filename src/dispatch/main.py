from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.dispatch.db.session import Base, engine
from contextlib import asynccontextmanager
from uuid import uuid1
from contextvars import ContextVar
from typing_extensions import Final, Optional
from dispatch.db.session import AsyncSessionLocal

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

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


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

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """각 요청마다 독립적인 비동기 DB 세션을 생성하는 미들웨어"""
    response = None
    request_id = str(uuid1())
    ctx_token = _request_id_ctx_var.set(request_id)

    try:
        request.state.db = AsyncSessionLocal()  # 비동기 세션 생성
        response = await call_next(request)  # 요청 처리
    except Exception as e:
        raise e from None
    finally:
        await request.state.db.close()  # 요청 종료 후 세션 닫기
        
    _request_id_ctx_var.reset(ctx_token)
    return response

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}