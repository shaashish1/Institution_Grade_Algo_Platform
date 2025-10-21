from fastapi import FastAPI
import uvicorn

app = FastAPI(title="AlgoProject API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("basic_api:app", host="0.0.0.0", port=3001, reload=True)