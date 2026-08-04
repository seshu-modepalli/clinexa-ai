from fastapi import FastAPI

app = FastAPI(
    title="Clinexa AI",
    description="AI Powered Healthcare Assistant",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "application": "Clinexa AI",
        "version": "1.0.0",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }