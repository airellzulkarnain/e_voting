from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Pasangan(Base):
    __tablename__ = 'pasangan'

    id = Column(Integer, primary_key=True)
    nomor_urut = Column(Integer, nullable=False, unique=True)
    nama_ketua = Column(String, nullable=False)
    nama_wakil = Column(String, nullable=False)
    gambar_wakil = Column(String, nullable=False)
    gambar_ketua = Column(String, nullable=False)
    jumlah_suara = Column(Integer, nullable=False, default=0)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False, unique=True)
    terpakai = Column(Boolean, nullable=False, default=False)


class Passcode(Base):
    __tablename__ = 'passcode'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False, default='admin')
