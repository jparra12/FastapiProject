from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/posts")
async def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": f"Title: {payLoad['Title']}, Content: {payLoad['Content']}"}