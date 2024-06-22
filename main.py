from typing import Union

from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd

from mlModelSaver2 import MlModelSaver
mlModelSaverInstance = MlModelSaver({
    "baseRelativePath": ".",
    "modelsFolder": "models"
})


app = FastAPI()

class ModelsBody(BaseModel):
    name: str = Field(..., example="rf")
    inputs:  Optional[List[Dict[str, Any]]] = Field(
        None,
        example=[
            {"amount":2,
"release_year": 2005,
"rental_rate":3,
"length" : 80,
"replacement_cost":18.9,
"NC-17": 1,
"PG" : 0,
"PG-13" : 0,
"R" :0,
"amount_2":4,
"length_2":6400,
"rental_rate_2" : 9,
"special_features":"Deleted Scenes"}
        ]
    )


@app.get("/")
def read_root():
    return "Hello World, this is Marion's ML API"

@app.get("/models/list")
def models():
    return mlModelSaverInstance.listOfModels()

@app.get("/model/info/{modelName}")
def modelInfo(modelName: str = Path(..., example="rf")):
    model = mlModelSaverInstance.getModel(modelName)

    response = model.mlModelSaverConfig
    return response



@app.post("/model/predict")
def modelsInfo(body: ModelsBody):
    model = mlModelSaverInstance.getModel(body.name)
    inputDf = pd.DataFrame(body.inputs)
    return model.mlModelSavePredict(
        inputDf,
        getattr(body, 'typeOfPredict', 'normal')
    )
