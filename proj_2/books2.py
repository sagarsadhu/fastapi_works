from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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
                "rating": 10,
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None, title="Description of the book", max_length=100, min_length=1
    )


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
        request: Request, exception: NegativeNumberException
):
    return JSONResponse(
        status_code=418,
        content={"message": "Cannot return negative number of books, Bazzinga"},
    )


# @app.post("/books/login")
# async def book_login(username: str = Form(), password: str = Form()):
#     return {"username": username, "password": password}

@app.post("/books/login")
async def book_login(book_id: UUID, username: str = Header(), password: str = Header()):
    if username == "FastAPIUser" and password == "test1234!":
        for x in BOOKS:
            if x.id == book_id:
                return x

    return "Invalid User"


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random_header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)

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
    raise raise_item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
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
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID {book_id} is deleted."

    raise raise_item_cannot_be_found_exception()


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


def raise_item_cannot_be_found_exception():
    return HTTPException(
        status_code=404,
        detail="Book not found",
        headers={"X-Header-Error": "Nothing to be seen at UUID"},
    )
