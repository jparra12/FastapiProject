from typing import Optional
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


class Post (BaseModel):
    id: int = 0
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='Dell', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(4)

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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts} 

@app.get("/posts/{id}")
async def get_post(id : int, response: Response):
    cursor.execute("""SELECT * FROM  posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"detail_post": post} 




@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                (post.title, post.content, post.published))
    result = cursor.fetchone()
    conn.commit()
    return {"data": result}



@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id=%s returning *""",
                    (post.title, post.content, post.published, str(id)))
    updated_post =cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id: {id} wasn't found")
    conn.commit()
    return {"data": updated_post} 




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):

    cursor.execute("""DELETE FROM posts WHERE id=%s returning * """,(str(id)))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id: {id} wasn't found") 
    conn.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)