from sqlalchemy import select, update, and_, delete
from sqlalchemy.orm import Session
from pandas import DataFrame
import models
import random
import string
import win32api


def masukan_pasangan(db: Session, nama_ketua: str, 
                        nama_wakil: str, gambar_ketua: str, 
                        gambar_wakil: str, nomor_urut: int):
    pasangan = models.Pasangan(nama_ketua=nama_ketua, nama_wakil=nama_wakil, gambar_ketua=gambar_ketua, gambar_wakil=gambar_wakil, nomor_urut=nomor_urut)
    db.add(pasangan)
    db.commit()
    db.refresh(pasangan)
    return pasangan

def ubah_pasangan(db: Session, nomor_urut, **kwargs):
    db.execute(update(models.Pasangan).where(models.Pasangan.nomor_urut == nomor_urut).values(**kwargs))
    db.commit()
    return 1


def hapus_pasangan(db: Session, nomor_urut):
    db.execute(delete(models.Pasangan).where(models.Pasangan.nomor_urut == nomor_urut))
    db.commit()
    return 1


def cetak_token(db: Session):
    tokens = db.execute(select(models.Token).where(models.Token.terpakai == False)).scalars().all()
    df = DataFrame({'tokens': [x.keyword for x in tokens]})
    df.to_excel(r'temp\temp.xlsx', index=False)
    win32api.ShellExecute(0, 'print', r'temp\temp.xlsx', None, '.', 0)
    return 1

def lihat_token(db: Session):
    return db.execute(select(models.Token)).scalars().all()

def buat_token(db: Session, jumlah: int):
    characters = string.ascii_letters + string.digits
    tokens = []
    for i in range(jumlah):
        tokens.append(models.Token(keyword=''.join(random.choices(characters, k=5))))
    db.add_all(tokens)
    db.commit()
    return 1


def verifikasi_token(db: Session, token: str):
        token = db.scalar(select(models.Token).where(and_(models.Token.keyword == token, models.Token.terpakai == False)))
        if token is not None:
            token.terpakai = True
            db.commit()
            return 1

def cek_passcode(db: Session, passcode: str):
    if db.scalar(select(models.Passcode.keyword)) == passcode:
        return True

def ubah_passcode(db: Session, new_passcode: str):
    db.execute(update(models.Passcode).where(models.Passcode.id == 1).values(keyword=new_passcode))
    db.commit()
    return 1

def ambil_pasangan(db: Session):
    return db.execute(select(models.Pasangan)).scalars().all()

def masukan_suara(db: Session, nomor_urut: int):
    pasangan = db.scalar(select(models.Pasangan).where(models.Pasangan.nomor_urut == nomor_urut))
    pasangan.jumlah_suara += 1
    db.commit()
    db.refresh(pasangan)
    return pasangan
