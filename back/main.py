from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
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
    id: int 
    code: str

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

@app.put("/{image_id}")
def update_book(image_id: int, image: Image, db: Session = Depends(get_db)):

    image_model = db.query(models.Images).filter(models.Images.id == image_id).first()

    if image_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {image_id} : Does not exist"
        )
    image_model.id = image_id
    image_model.code=image.code

    db.add(image_model)
    db.commit()

    return db.query(models.Images).all()

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

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}