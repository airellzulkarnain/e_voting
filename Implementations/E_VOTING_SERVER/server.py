from fastapi import FastAPI, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
import crud


app = FastAPI(redoc_url=None, docs_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)
app.mount("/images", StaticFiles(directory="images"), name="images")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ambil_pasangan")
def ambil_pasangan(db: Session = Depends(get_db)):
    return crud.ambil_pasangan(db)


@app.post("/verifikasi_token")
def verifikasi_token(
    token: str = Form(...), nisn: str = Form(...), db: Session = Depends(get_db)
):
    return crud.verifikasi_token(db, token, nisn)


@app.post("/masukan_suara")
def masukan_suara(
    nomor_urut: int = Form(...), nisn: str = Form(...), db: Session = Depends(get_db)
):
    return crud.masukan_suara(db, nomor_urut, nisn)

@app.get("/ambil_persentase/{nomor_urut}")
def ambil_persentase(nomor_urut: str, db: Session = Depends(get_db)):
    return crud.ambil_persentase(db, nomor_urut)
