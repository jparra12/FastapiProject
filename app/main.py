from typing import Optional
from fastapi import FastAPI, Response, HTTPException, status, Depends 
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind = engine)


app = FastAPI()







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





@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts} 

@app.get("/posts/{id}")
async def get_post(id : int, response: Response, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM  posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"detail_post": post} 




@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #            (post.title, post.content, post.published))
    #result = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}



@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id=%s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    #updated_post =cursor.fetchone()

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id: {id} wasn't found")

    #conn.commit()
    updated_post.update(post.dict(), synchronize_session = False)
    db.commit()
    return {"data": updated_post} 




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int, db: Session = Depends(get_db)):

    #cursor.execute("""DELETE FROM posts WHERE id=%s returning * """,(str(id)))
    #deleted_post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"id: {id} wasn't found") 
    #conn.commit()  
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)