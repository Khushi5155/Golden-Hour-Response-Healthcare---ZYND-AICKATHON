from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import routes
import uvicorn

# Import websocket only if it exists
try:
    from src.api import websocket
    HAS_WEBSOCKET = True
except ImportError:
    HAS_WEBSOCKET = False
    print("⚠️  WebSocket module not found, skipping...")

app = FastAPI(
    title="Golden Hour Response System",
    description="AI-powered emergency response backend",
    version="1.0.0"
)

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routes
app.include_router(routes.router, prefix="/api/v1")

# Include WebSocket routes (if available)
if HAS_WEBSOCKET:
    app.include_router(websocket.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Golden Hour System Active 🚑",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    print("🚀 Starting Golden Hour Response System...")
    print("📍 API Docs: http://localhost:8000/docs")
    print("🏥 Health: http://localhost:8000/")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
