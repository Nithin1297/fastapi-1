from fastapi import APIRouter, Query, HTTPException
from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId
from typing import Union

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}  # You can return an actual favicon file if you have one.


@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos

@router.get("/{id}")
async def get_one_todo(id: str):
    one_todo = collection_name.find_one({"_id": ObjectId(id)})
    if one_todo:
        one_todo["_id"] = str(one_todo["_id"])
        return one_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/")
async def post_todo(todo: Todo):
    collection_name.insert_one(dict(todo))
    return {"message": "Todo added successfully"}

@router.put("/{id}")
async def put_todo(id: str, todo: Todo):
    result = collection_name.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(todo)}
    )
    if result:
        return {"message": "Todo updated successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{id}")
async def delete_todo(id: str):
    result = collection_name.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@router.get("/search/")
async def search_todos(query: Union[str, None] = Query(None), complete: Union[bool, None] = Query(None)):

    search_query = {}

    if query:
        search_query["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    if complete is not None:
        search_query["complete"] = complete

    search_results = list_serial(collection_name.find(search_query))
    
    if not search_results:
        return {"message": "No todos found matching the query."}
    
    return search_results

