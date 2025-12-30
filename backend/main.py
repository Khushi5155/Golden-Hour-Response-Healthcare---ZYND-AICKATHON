from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import routes, websocket
import uvicorn

app = FastAPI(
    title="Golden Hour Response System",
    description="AI-powered emergency response backend",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routes
app.include_router(routes.router, prefix="/api/v1")

# Include WebSocket routes
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"status": "online", "message": "Golden Hour System Active 🚑"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
