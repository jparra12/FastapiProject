from typing import Optional
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class Post (BaseModel):
    id: int = 0
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None



json_posts = [{"title":"title of post 1","content": "content of post 1","id":1},
              {"title":"title of post 3","content": "content of post 3","id":3},
              {"title":"title of post 7","content": "content of post 7","id":7},
              {"title":"title of post 11","content": "content of post 11","id":11},
              {"title":"title of post 151","content": "content of post 151","id":151}]



def find_post(id : int):
    for p in json_posts:
        if p['id'] == id:
            return p
        #return None

def find_post_index(id : int):
    for i, p in enumerate(json_posts):
        if p['id'] == id:
            return i
        #return None


app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": json_posts} 

@app.get("/posts/{id}")
async def get_post(id : int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id {id} was not found"}

    return {"detail_post": post} 




@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    postReceived = post.dict()
    postReceived['id'] = randrange(1, 10000)
    json_posts.append(postReceived)
    
    return {"data": postReceived}



@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id: {id} wasn't found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    json_posts[index]  = post_dict 
    
    return {"data": post_dict} 




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):
    
    index = find_post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id: {id} wasn't found")
    
    json_posts.pop(index)   
    return Response(status_code=status.HTTP_204_NO_CONTENT)