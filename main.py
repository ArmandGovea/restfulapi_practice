from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# creates the books.db file and table if they don't exist yet
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Book Tracker API')


@app.get('/')
def root():
    return {'message': 'Book Tracker API - visit /docs for interative docs'}


@app.get('/books', response_model=list[schemas.BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.get('/books/{book_id}', response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail=f'Book "{book}" not found')
    return book
