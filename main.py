import os
import json

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.encoders import jsonable_encoder

from models import Author
from models import Author as ModelAuthor
from models import Book
from models import Book as ModelBook
from schema import Author as SchemaAuthor
from schema import Book as SchemaBook

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/update-book/{book_id}", response_model=SchemaBook)
def update_book(book_id:int, book: SchemaBook):
    db_book = db.session.query(Book).filter(Book.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with code " + str(book_id) + " does not exist")

    update_data = dict()
    print("DATA TO BE UPDATED: ",dict(book))
    for k, v in dict(book).items():
        if v is not None:
            update_data[k] = v

    updated_item_id = db.session.query(Book).filter(Book.id == book_id).update(update_data)
    print("UPDATED DATA: ",updated_item_id)
    updated_book = db.session.query(Book).filter(Book.id == updated_item_id).first()
    db.session.commit()
    return updated_book


@app.put("/update-author/{author_id}", response_model=SchemaAuthor)
def update_author(author_id:int, author: SchemaAuthor):
    db_author = db.session.query(Author).filter(Author.id == author_id).first()
    
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author with code " + str(author_id) + " does not exist")

    update_data = dict()
    print("DATA TO BE UPDATED: ",dict(author))
    for k, v in dict(author).items():
        if v is not None:
            update_data[k] = v

    updated_item_id = db.session.query(Author).filter(Author.id == author_id).update(update_data)
    print("UPDATED DATA: ",updated_item_id)
    updated_author = db.session.query(Author).filter(Author.id == updated_item_id).first()
    db.session.commit()
    return updated_author


@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, price=book.price, unit_of_currency=book.unit_of_currency, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/add-author/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.get("/books/")
def get_books():
    books = db.session.query(Book).all()
    return books


@app.get("/authors/")
def get_books():
    authors = db.session.query(Author).all()
    return authors


@app.get("/get-book/{book_id}", response_model=SchemaBook)
def get_book(book_id:int):
    db_book = db.session.query(Book).filter(Book.id == book_id).first()
    detail_msg = "Book with code " + str(book_id) + " does not exist"
    if db_book is None:
        raise HTTPException(status_code=404, detail=detail_msg)
    
    return db_book


@app.get("/get-author/{author_id}", response_model=SchemaAuthor)
def get_author(author_id:int):
    db_author = db.session.query(Author).filter(Author.id == author_id).first()
    detail_msg = "Author with code " + str(author_id) + " does not exist"
    if db_author is None:
        raise HTTPException(status_code=404, detail=detail_msg)
    
    return db_author


@app.delete("/delete-book/{book_id}")
def delete_book(book_id:int):
    db_book = db.session.query(Book).filter(Book.id == book_id).first()
    db.session.query(Book).filter(Book.id == book_id).delete()
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with code {book_id} does not exist")
    
    db.session.commit()
    return {
        "message": f"Deleted book {book_id}",
        "Deleted Book details" : dict(db_book),
    }


@app.delete("/delete-author/{author_id}")
def delete_author(author_id:int):
    db_author = db.session.query(Author).filter(Author.id == author_id).first()
    print("author to be deleted:",db_author.name)
    db.session.query(Author).filter(Author.id == author_id).delete()
    if db_author is None:
        raise HTTPException(status_code=404, detail=f"Author with code {author_id} does not exist")
    
    db.session.commit()
    return {
        "message": f"Deleted author {author_id}",
        "Deleted Author details" : db_author,
    }

# @app.post("/user/", response_model=SchemaUser)
# def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
