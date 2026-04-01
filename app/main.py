from fastapi import FastAPI, Request
import logging

from app.api.routes import transaction
from app.db.session import engine
from app.db.base import Base
from app.core.logging import setup_logging

from prometheus_fastapi_instrumentator import Instrumentator


# ✅ Setup logging FIRST
setup_logging()
logger = logging.getLogger(__name__)

# ✅ Create FastAPI app
app = FastAPI(title="Transaction Risk Service")

# ✅ Middleware (after app creation)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response

# ✅ Include routes
app.include_router(transaction.router)

# ✅ Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Metrics (AFTER app creation)
Instrumentator().instrument(app).expose(app)

# ✅ DB table creation (last step)
Base.metadata.create_all(bind=engine)