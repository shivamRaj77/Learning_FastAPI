from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Book_One", "author": "author one", "category": "science"},
    {"title": "Book_Two", "author": "author two", "category": "history"},
    {"title": "Book_Three", "author": "author three", "category": "science"},
    {"title": "Book_Four", "author": "author four", "category": "mathematics"},
    {"title": "Book_Five", "author": "author five", "category": "economics"}
]

# GET HTTP Method
@app.get("/books")
async def read_api():
    return BOOKS
    
#Path Parameter
@app.get("/books/{title}")
async def read_book(title: str):
    for book in BOOKS:
        if book.get('title', '').casefold()==title.casefold():
            return book

# Query Parameter
@app.get("/books/")
async def read_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category', '').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Simultaneous use of Query and Path Parameters
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author', '').casefold()==book_author.casefold() and \
                book.get('category', '').casefold()==category.casefold():
            books_to_return.append(book)
    return books_to_return

# POST HTTP Method
@app.post("/books/create_book")
async def create_book(new_Book = Body()):
    BOOKS.append(new_Book)
    
# PUT HTTP Method
@app.put("/books/update_book")
async def update_book(updated_Book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title', '').casefold()==updated_Book.get('title').casefold():
            BOOKS[i] = updated_Book

# DELETE HTTP Method
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title', '').casefold()==book_title.casefold():
            BOOKS.pop()
            break;

# Assignment: Create a new API Endpoint that can fetch all books 
# from a specific author using either Path Parameters or Query Parameters.

# Solution (using Path Parameters) 
@app.get("/books/byauthor/{author_name}")
def fetch_book_from_author(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author', '').casefold()==author_name.casefold():
            books_to_return.append(book)
    return books_to_return

# Solution (using Query Parameters) 
# -- this will not work unless you put this above "@app.get("/books/{book_author}/")"
@app.get("/books/byauthor/")
async def fetch_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author', '').casefold()==author.casefold():
            books_to_return.append(book)
    return books_to_return
