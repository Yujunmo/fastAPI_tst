from fastapi import FastAPI,Body,HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

@app.get("/")
async def home():
    return "HI"


data = {
    1:{
        "id":1,
        "task":"linux bash script",
        "is_done":False
    },
    2:{
        "id":2,
        "task":"fast api",
        "is_done":True
    },
    3:{
        "id":3,
        "task":"sqlp",
        "is_done":False
    },    
}

class createTodoRequest(BaseModel):
    id:int
    contents:str
    is_done:bool


@app.get("/todos",status_code=200)
def get_todos_handler(order:str|None = None):
    ret = list(data.values())
    if order == "DESC":
        return ret[::-1]
    return ret



@app.get("/todos/{id}",status_code=200)
def get_todo_handler(id:int):
    rs = data.get(id)
    if rs:
        return rs
    else:
        raise HTTPException(status_code=404, detail="resource not found")


@app.post("/todos",status_code=201)
def post_todo_handler(request:createTodoRequest):
    data[request.id] = request.dict()
    return json.dumps(data)


@app.patch("/todos/{id}",status_code=200)
def update_todo_handler(
     id:int
    ,is_done : bool = Body(...,embed=True)
      ):
    rs = data.get(id,None)
    if rs:
        rs["is_done"] = is_done
    else:
        raise HTTPException(status_code=404,detail="resource not found")
    

@app.delete("/todos/{id}")
def delete_todo_handler(id:int):
    rs = data.pop(id,None)
    if rs is None:
        raise HTTPException(status_code = 404, detail="resource not found")
    