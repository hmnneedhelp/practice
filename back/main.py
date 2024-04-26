from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
import base64
import io
import numpy
import matplotlib.pyplot as plt
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import File, UploadFile

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Image(BaseModel):
    id: int = Field(gt=-1, lt=101)
    code: str = Field(min_length=1)

IMAGE = []


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return db.query(models.Images).all()

@app.post("/")
def create_image(image: Image, db: Session = Depends(get_db)):
    
    image_model = models.Images()
    image_model.id = image.id
    image_model.code = image.code

    db.add(image_model)
    db.commit()

    return image

@app.get("/{image_id}")
def find_one_img(image_id:int, db: Session = Depends(get_db)):
    image_model = db.query(models.Images).filter(models.Images.id == image_id).first()

    
    if image_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {image_id} : Does not exist"
        )

    return image_model

@app.delete("/{image_id}")
def delete_image(image_id:int, db:Session = Depends(get_db)):
    image_model = db.query(models.Images).filter(models.Images.id == image_id).first()

    if image_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {image_id} : Does not exist"
        )

    db.query(models.Images).filter(models.Images.id == image_id).delete()
    
    db.commit()

    return db.query(models.Images).all()

@app.post('/encodeimage')
async def encode_image(image: UploadFile = File(...), db:Session = Depends(get_db),):
    image_model = models.Images()
    img = await image.read()
    encoded_image = base64.b64encode(img).decode('utf-8')
    image_model.code = encoded_image
    db.add(image_model)
    db.commit()
    return db.query(models.Images).all()