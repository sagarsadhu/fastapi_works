from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'}

}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.post("/")
async def create_book(book_title: str, book_author: str):
    current_book_id = len(BOOKS)

    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']


@app.put("/{book_name}")
async def update_book(book_name: str, book_author: str, book_title: str):
    book_info = {'title': book_title, 'book_author': book_author}
    BOOKS[book_name] = book_info
    return book_info


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f'{book_name} deleted.'


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS.get(book_name)


@app.get("/book/read/")
async def read_book(book_name: str):
    return BOOKS.get(book_name)


@app.delete("/book/delete/")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f'{book_name} is deleted.'


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "Left"}
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "sub": "Right"}


@app.get("/book/mybook")
async def read_favorite_book():
    return {"book_title": "Immortals of Meluha"}


@app.get("/book/{book_id}")
async def read_book(book_id: int):
    return {"book_title": book_id}
