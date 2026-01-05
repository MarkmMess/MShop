import uvicorn
from fastapi import FastAPI
from api.endpoints import users, product

app = FastAPI()
app.include_router(product.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
