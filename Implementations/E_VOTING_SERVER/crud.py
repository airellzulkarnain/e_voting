from sqlalchemy import select, update, and_, delete, or_, func
from sqlalchemy.orm import Session
import pandas as pd
import models
import random
import string
import win32api


def masukan_pasangan(
    db: Session,
    nama_ketua: str,
    nama_wakil: str,
    gambar_ketua: str,
    gambar_wakil: str,
    nomor_urut: int,
):
    pasangan = models.Pasangan(
        nama_ketua=nama_ketua,
        nama_wakil=nama_wakil,
        gambar_ketua=gambar_ketua,
        gambar_wakil=gambar_wakil,
        nomor_urut=nomor_urut,
    )
    db.add(pasangan)
    db.commit()
    db.refresh(pasangan)
    return pasangan


def hapus_pasangan(db: Session, nomor_urut):
    db.execute(delete(models.Pasangan).where(models.Pasangan.nomor_urut == nomor_urut))
    db.commit()
    return 1


def masukan_peserta(db: Session, xlsx_name: str):
    data_peserta = pd.read_excel(xlsx_name)
    data_peserta.drop_duplicates(inplace=True)
    list_peserta = []
    for index, peserta in data_peserta.iterrows():
        if not db.scalar(select(models.PesertaPemilu.nisn).where(models.PesertaPemilu.nisn == peserta["NISN"])):
            list_peserta.append(
                models.PesertaPemilu(nisn=peserta["NISN"], nama=peserta["NAMA"])
            )
    db.add_all(list_peserta)
    db.commit()


def cetak_token(db: Session, dir_: str):
    tokens = (
        db.execute(select(models.Token).where(models.Token.terpakai == False))
        .scalars()
        .all()
    )
    peserta = lihat_peserta(db)
    

    df = pd.DataFrame({
        "NAMA": [x.nama for x in peserta], 
        "NISN": [x.nisn for x in peserta], 
        "TOKEN": [x.keyword for x in tokens][:len(peserta)], 
        })
    df.to_excel(dir_+r'\data_peserta_pemilu.xlsx', index=False)
    # win32api.ShellExecute(0, "print", r"temp\temp.xlsx", None, ".", 0)
    return 1


def lihat_token(db: Session, belum_terpakai: bool = False):
    if belum_terpakai:
        return db.execute(select(models.Token).where(models.Token.terpakai == False)).scalars().all()
    return db.execute(select(models.Token)).scalars().all()


def lihat_peserta(db: Session, keyword: str | None = None):
    if bool(keyword):
        return db.execute(select(models.PesertaPemilu)
        .where(or_(
            models.PesertaPemilu.nama.like(f'%{keyword}%'), 
            models.PesertaPemilu.nisn.like(f'%{keyword}%'), 
            models.PesertaPemilu.nomor_urut_yang_dipilih.like(f'%{keyword}%')
            ))
        ).scalars().all()
    return db.execute(select(models.PesertaPemilu)).scalars().all()


def buat_token(db: Session, jumlah: int):
    characters = string.ascii_letters + string.digits
    tokens = []
    for i in range(jumlah):
        tokens.append(models.Token(keyword="".join(random.choices(characters, k=5)).lower()))
    db.add_all(tokens)
    db.commit()
    return 1


def verifikasi_token(db: Session, token: str, nisn: str):
    token = db.scalar(
        select(models.Token).where(
            and_(models.Token.keyword == token, models.Token.terpakai == False)
        )
    )
    nisn = db.scalar(
        select(models.PesertaPemilu.nisn).where(and_(models.PesertaPemilu.nisn == nisn, models.PesertaPemilu.nomor_urut_yang_dipilih == None))
    )
    if (token and nisn) or (nisn == 'demo' and token == 'demo'):
        token.terpakai = True
        db.commit()
        return nisn


def cek_passcode(db: Session, passcode: str):
    if db.scalar(select(models.Passcode.keyword)) == passcode:
        return True


def ubah_passcode(db: Session, new_passcode: str):
    db.execute(
        update(models.Passcode)
        .where(models.Passcode.id == 1)
        .values(keyword=new_passcode)
    )
    db.commit()
    return 1


def ambil_pasangan(db: Session):
    return db.execute(select(models.Pasangan)).scalars().all()


def ambil_persentase(db: Session, nomor_urut: str):
    try: 
        return (db.scalar(select(models.Pasangan.jumlah_suara).where(models.Pasangan.nomor_urut == nomor_urut))/db.scalar(select(func.sum(models.Pasangan.jumlah_suara))))*100.0
    except ZeroDivisionError:
        return 0


def masukan_suara(db: Session, nomor_urut: int, nisn: str):
    pasangan = db.scalar(
        select(models.Pasangan).where(models.Pasangan.nomor_urut == nomor_urut)
    )
    peserta_pemilu = db.scalar(
        select(models.PesertaPemilu).where(models.PesertaPemilu.nisn == nisn)
    )
    peserta_pemilu.nomor_urut_yang_dipilih = nomor_urut
    pasangan.jumlah_suara += 1
    db.commit()
    return 1
