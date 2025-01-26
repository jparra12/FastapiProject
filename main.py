from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

class Post (baseModel):
    title:str
    content:str
    published= False
    rating= Optional[int]=None




app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/posts")
async def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}