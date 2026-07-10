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
        raise HTTPException(status_code=404, detail=f'Book with book id "{book_id}" not found')
    return book

@app.post('/books', response_model=schemas.BookResponse, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put('/books/{book_id}', response_model=schemas.BookResponse)
def update_book(book_id: int, updates: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail=f'Book with book id "{book_id}" not found')

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(book, field, value)


    db.commit()
    db.refresh(book)
    return book


@app.delete('/books/{book_id}', status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f'Book with book id "{book_id}" not found')

    db.delete(book)
    db.commit()
    return None