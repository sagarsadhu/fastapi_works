from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(
        title="Description of book", max_length=100, min_length=1
    )
    rating: int = Field(gt=-1, lt=11)

    class Config:
        schema_extra = {
            "example": {
                "id": "e0661d81-05dd-46b2-9b64-a23069810a5b",
                "title": "The immortals of Meluha",
                "author": "Amish Tripathi",
                "description": "Shiva Trilogy part-1",
                "rating": 10
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        new_books = BOOKS[:books_to_return]
        return new_books

    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    return {}


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return book
    return "Id didn't match, nothing to update"


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID {book_id} is deleted.'

    return "Id didn't match, nothing to delete"


def create_books_no_api():
    book_1 = Book(
        id="e0661d81-05dd-46b2-9b64-a23069810a5b",
        title="Pymongo",
        author="Mongoose",
        description="Mongo DB",
        rating=9,
    )
    book_2 = Book(
        id="506b7560-b52b-4c58-b53d-76b58dc20389",
        title="React",
        author="Leela",
        description="React JS " "with " "Leela",
        rating=9,
    )
    book_3 = Book(
        id="4692e915-36a9-4b1a-a8ec-b6cc9f04d462",
        title="Nodejs",
        author="Banni",
        description="Node JS " "with " "Bhavani",
        rating=9,
    )
    book_4 = Book(
        id="705a8417-4fc9-40af-99d5-bfeb12bceeae",
        title="FastAPI",
        author="Balu",
        description="FastAPI in " "python",
        rating=9,
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
