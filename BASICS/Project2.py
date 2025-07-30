from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# Pydantic Model
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not mandatory", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "John Doe",
                "description": "Describe the Book", 
                "rating": 5
            }
        }
    }
    

BOOKS = [
    Book(1, "1984", "George Orwell", "Dystopian novel about totalitarianism", 5),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Classic novel on racial injustice", 5),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", "Jazz Age story of love and loss", 4),
    Book(4, "Pride and Prejudice", "Jane Austen", "Romantic drama in the British countryside", 5),
    Book(5, "The Catcher in the Rye", "J.D. Salinger", "Rebellious teen's journey in NYC", 4),
    Book(6, "The Hobbit", "J.R.R. Tolkien", "Fantasy adventure of Bilbo Baggins", 5),
    Book(7, "Frankenstein", "Mary Shelley", "Gothic novel about creation and responsibility", 4),
    Book(8, "The Alchemist", "Paulo Coelho", "Spiritual journey to follow one's dreams", 4),
    Book(9, "Jane Eyre", "Charlotte Brontë", "Orphaned girl's rise through adversity", 5),
    Book(10, "The Book Thief", "Markus Zusak", "Story of a girl in Nazi Germany narrated by Death", 5)
]

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id + 1
    return book

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")    # path parameter
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id==book_id:
            return book
        
@app.get("/books/")     # query parameter
async def read_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

# post request before validation
@app.post("/create_book")
# Body doesn't allow any kind of validation on the data
# async def create_book(book_request=Body()):
#     BOOKS.append(book_request)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.put("/books/update_book")
async def update_book(updated_book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].title.casefold()==updated_book.title.casefold():
            BOOKS[i] = Book(**updated_book.model_dump())

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break