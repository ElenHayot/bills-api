from fastapi import FastAPI

app = FastAPI(title="Bills API")

@app.get("/")
def healthcheck():
    return {"status": "ok"}