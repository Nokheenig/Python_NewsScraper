from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List


from .models.article import Article as objectModel
from .models.article import ArticleUpdate as objectUpdateModel
objectName = "article"
routerName = f"{objectName}_router"
#exec(routerName = APIRouter())
router = APIRouter()

#
@router.post("/", response_description=f"Creates a new {objectName} in database", status_code=status.HTTP_201_CREATED, response_model=objectModel)
def create_object(request: Request, obj: objectModel = Body(...)):
    obj = jsonable_encoder(obj)
    new_obj = request.app.database[f"{objectName}s"].insert_one(obj)
    created_obj = request.app.database[f"{objectName}s"].find_one(
        {"_id": new_obj.inserted_id}
    )

    return created_obj

#
@router.get("/", response_description=f"Returns all (first 100) {objectName}s in the database", response_model=List[objectModel])
def list_objects(request: Request):
    objects = list(request.app.database[f"{objectName}s"].find(limit=100))
    return objects

#panels = [panel for panel in request.app.database[f"{objectName}s"].find({},projection)]

@router.get("/list", response_description=f"Returns a summary list of all {objectName}s in database")
def sumlist_objects(request: Request):
    query = {
        "manufacturer": "1Soltech"
    }
    projection = {
        "date": 1,
        "title": 1,
        "link": 1,
    }

    objects = [obj for obj in request.app.database[f"{objectName}s"].find({},projection)]
    #objDict = {f"{panel['manufacturer']}_{panel['model']}": panel for panel in panels}
    return objects

@router.get("/{id}", response_description=f"Returns {objectName} with provided id", response_model=objectModel)
def find_object(id: str, request: Request):
    if (obj := request.app.database[f"{objectName}s"].find_one({"_id": id})) is not None:
        return obj
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{objectname.capitalize()} with ID {id} not found")

"""
#
@router.put("/{id}", response_description=f"Updates {objectName} in database with provided id with provided dictionnary object", response_model=objectModel)
def update_object(id: str, request: Request, obj: objectUpdateModel = Body(...)):
    obj = {k: v for k, v in obj.dict().items() if v is not None}
    if len(obj) >= 1:
        update_result = request.app.database[f"{objectName}s"].update_one(
            {"_id": id}, {"$set": obj}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{objectname.capitalize()} with ID {id} not found")

    if (
        existing_obj := request.app.database[f"{objectName}s"].find_one({"_id": id})
    ) is not None:
        return existing_obj

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{objectname.capitalize()} with ID {id} not found")
"""
#
@router.delete("/{id}", response_description=f"Deletes {objectName} in database with provided id")
def delete_object(id: str, request: Request, response: Response):
    delete_result = request.app.database[f"{objectName}s"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{objectname.capitalize()} with ID {id} not found")