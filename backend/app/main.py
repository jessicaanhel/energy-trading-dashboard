from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.power import router as power_router

app = FastAPI(title="Power Trading API (Local CSV)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(power_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=3001, reload=True)