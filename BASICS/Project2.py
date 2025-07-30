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
    published: int

    def __init__(self, id, title, author, description, rating, published):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published

# Pydantic Model
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not mandatory", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published: int = Field(gt=1500, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "John Doe",
                "description": "Describe the Book", 
                "rating": 5,
                "published": 2000
            }
        }
    }
    

BOOKS = [
    Book(1, "The Silent Patient", "Alex Michaelides", "A thrilling tale of mystery.", 5, 2019),
    Book(2, "The Maidens", "Alex Michaelides", "Dark academia meets murder mystery.", 4, 2021),
    Book(3, "Atomic Habits", "James Clear", "Self-improvement strategies that work.", 5, 2018),
    Book(4, "Deep Work", "Cal Newport", "Maximize focus and productivity.", 4, 2016),
    Book(5, "Digital Minimalism", "Cal Newport", "Tech detox for the modern age.", 4, 2019),
    Book(6, "1984", "George Orwell", "Dystopian future that feels too real.", 5, 1949),
    Book(7, "Animal Farm", "George Orwell", "A clever satire on power and politics.", 5, 1945),
    Book(8, "The Midnight Library", "Matt Haig", "What if you could live other lives?", 4, 2020),
    Book(9, "Outliers", "Malcolm Gladwell", "The story of success beyond talent.", 4, 2008),
    Book(10, "Blink", "Malcolm Gladwell", "Thinking without thinking.", 4, 2005)
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

# ASSIGNMENT
@app.get("/books/publish/")
async def read_by_published(published: int):
    books_to_return  = []
    for book in BOOKS:
        if book.published==published:
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
            if updated_book.id==None:
                updated_book.id = BOOKS[i].id
            BOOKS[i] = Book(**updated_book.model_dump())

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break