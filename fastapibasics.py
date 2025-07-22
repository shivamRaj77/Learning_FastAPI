# 1. Library Imports
# pip install fastapi uvicorn
from fastapi import FastAPI
from typing import Optional
import uvicorn  ## ASGI(Asynchronous Server Gateway Interface)

# 2. Create the app object
app = FastAPI()

# HTTP Methods - GET, POST, PUT, DELETE

# 3. Index route, opens automatically on http://127.0.0.1:8000
# setting up an endpoint
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
# Located at: http://127.0.0.1:8000/AnyNameHere
@app.get("/NewPage")
async def hello(name: str):
    return f"Welcome {name} to fastAPI tutorial."

# https://app.example.com/users?age=25&country=US
# / ---> Path/Endpoint Parameters
# ? ---> Query Parameters


# Run the API with uvicorn
# Will run on http://127.0.0.1:8000
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
# uvicorn filename:FastAPIobjectname --reload