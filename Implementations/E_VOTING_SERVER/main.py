from tkinter import *
from tkinter import ttk
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import SessionLocal, engine
from server import app
from style import stylize
import models, crud
import multiprocessing
import uvicorn
from PIL import Image, ImageTk


models.Base.metadata.create_all(bind=engine)

def get_db(func):
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(db)
        finally:
            db.close()
        return result
    return wrapper

def run_api():
    uvicorn.run(app, host='0.0.0.0')

@get_db
def masuk(db: Session):
    if crud.cek_passcode(db, passcode.get()):
        main_window()
    else:
        error_msg.configure(text='Gagal Masuk !')

server = None

def main_window():
    def no_close():
        pass

    def start_server():
        for child in tambah_paslon_frame.winfo_children(): 
                child.state(['disabled'])
        global server
        server = multiprocessing.Process(target=run_api)
        server.start()
        tombol_mulai.configure(text='Berhenti', command=stop_server)

    def stop_server():
        server.terminate()
        tombol_mulai.configure(text='Mulai', command=start_server)
        for child in tambah_paslon_frame.winfo_children(): 
                child.state(['!disabled'])

    def masukan_pasangan():
        pass

    def ganti_passcode():
        pass

    def buat_token():
        pass
    
    login_window.destroy()
    main_window = Toplevel(root)
    main_window.wm_attributes('-fullscreen', 1)
    main_window.protocol('WM_DELETE_WINDOW', no_close)
    main_windows_frame = ttk.Frame(main_window, padding=(6, 10, 6, 10))
    main_windows_frame.grid(column=0, row=0, sticky=(N, E, W, S))

    tambah_paslon_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Tambah Pasangan'))
    masukan_nomor_urut = ttk.Spinbox(tambah_paslon_frame, from_=1.0, to=6.0)
    masukan_nama_ketua = ttk.Entry(tambah_paslon_frame)
    masukan_nama_wakil = ttk.Entry(tambah_paslon_frame)
    tombol_gambar_ketua = ttk.Button(tambah_paslon_frame, text='+')
    tombol_gambar_wakil = ttk.Button(tambah_paslon_frame, text='+')
    tombol_tambah = ttk.Button(tambah_paslon_frame, text='Tambah')

    passcode_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Ubah Passcode'))
    masukan_ubah_passcode = ttk.Entry(passcode_frame)
    tombol_ubah_passcode = ttk.Button(passcode_frame, text='Ubah')
    masukan_ubah_passcode.grid(column=1, row=1, sticky=(W, E), padx=4, pady=6)
    tombol_ubah_passcode.grid(column=2, row=1, sticky=(W, E), padx=4, pady=6)

    ttk.Label(tambah_paslon_frame, text='Nomor Urut').grid(column=1, row=1, sticky=(W, E))
    masukan_nomor_urut.grid(column=1, row=2, sticky=(W, E))
    ttk.Label(tambah_paslon_frame, text='Nama Ketua').grid(column=1, row=3, sticky=(W, E))
    masukan_nama_ketua.grid(column=1, row=4, sticky=(W, E))
    ttk.Label(tambah_paslon_frame, text='Nama Wakil').grid(column=1, row=5, sticky=(W, E))
    masukan_nama_wakil.grid(column=1, row=6, sticky=(W, E))
    ttk.Label(tambah_paslon_frame, text='Gambar Ketua').grid(column=1, row=7, sticky=(W, E))
    tombol_gambar_ketua.grid(column=1, row=8, sticky=(W, E), padx=4, pady=6)
    ttk.Label(tambah_paslon_frame, text='Gambar Wakil').grid(column=1, row=9, sticky=(W, E))
    tombol_gambar_wakil.grid(column=1, row=10, sticky=(W, E), padx=4, pady=6)
    tombol_tambah.grid(column=1, row=11, sticky=(W, E), padx=4, pady=6)
    paslon_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Pasangan'))
    ttk.Label(paslon_frame, text='test').grid(column=0, row=0)
    token_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Verifikasi Token'))
    masukan_jumlah_token = ttk.Spinbox(token_frame, from_=1.0, to=200.0)
    tombol_buat_token = ttk.Button(token_frame, text='Buat')
    tombol_lihat_token = ttk.Button(token_frame, text='Lihat')
    tombol_mulai = ttk.Button(main_windows_frame, text='Mulai', command=start_server)
    tombol_keluar = ttk.Button(main_windows_frame, text='Tutup', command=root.destroy, style='keluar.TButton')
    masukan_jumlah_token.grid(column=1, row=1, sticky=(W, E, S))
    tombol_buat_token.grid(column=2, row=1, sticky=(W, E, S), padx=4, pady=6)
    tombol_lihat_token.grid(column=3, row=1, sticky=(W, E, S), padx=4, pady=6)
    tambah_paslon_frame.grid(column=1, row=1, rowspan=3, sticky=(N, E, W, S))
    paslon_frame.grid(column=2, row=1, columnspan=2, sticky=(N, E, W, S))
    token_frame.grid(column=2, row=2, sticky=(N, E, W, S))
    passcode_frame.grid(column=2, row=3, sticky=(N, E, W, S))
    tombol_mulai.grid(column=3, row=2, sticky=(N, E, W, S), padx=4, pady=6)
    tombol_keluar.grid(column=3, row=3, sticky=(N, E, W, S), padx=4, pady=6)

    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)

    main_windows_frame.columnconfigure(1, weight=1)
    main_windows_frame.columnconfigure(2, weight=6)
    main_windows_frame.columnconfigure(3, weight=1)
    main_windows_frame.rowconfigure(1, weight=30)
    main_windows_frame.rowconfigure(2, weight=1)
    main_windows_frame.rowconfigure(3, weight=1)

    tambah_paslon_frame.columnconfigure(1, weight=1)

    token_frame.columnconfigure(1, weight=3)
    token_frame.columnconfigure(2, weight=1)
    token_frame.columnconfigure(3, weight=1)
    token_frame.rowconfigure(1, weight=1)

    passcode_frame.columnconfigure(1, weight=4)
    passcode_frame.columnconfigure(2, weight=1)
    passcode_frame.rowconfigure(1, weight=1)




if __name__ == '__main__':
    root = Tk()
    login_window = Toplevel(root)
    login_window_frame = ttk.Frame(login_window, padding=(4, 6, 4, 6))
    passcode = StringVar()
    masukan_passcode = ttk.Entry(login_window_frame, textvariable=passcode, font=('Times New Roman', 16, 'normal'), justify=CENTER, show='X')
    tombol_masuk = ttk.Button(login_window_frame, text='Masuk', command=masuk, style='login.TButton')
    logo_smkn_5 = ImageTk.PhotoImage(Image.open(r'images\logo_smkn_5.png').resize((120, 150)))
    logo_osis = ImageTk.PhotoImage(Image.open(r'images\logo_osis.png').resize((120, 120)))
    error_msg = ttk.Label(login_window_frame, text=' ', foreground='red')
    stylize(ttk.Style)


    root.withdraw()
    root.wm_attributes('-transparentcolor', 'purple')


    login_window.title('E - Voting Server | Login')
    login_window.geometry(f'720x524+{root.winfo_screenwidth()//2 - 360}+{root.winfo_screenheight()//2 - 262}')
    login_window.resizable(FALSE, FALSE)
    login_window.protocol('WM_DELETE_WINDOW', root.destroy)


    login_window_frame.rowconfigure(0, weight=1)
    login_window_frame.columnconfigure(0, weight=1)


    login_window_frame.grid(column=0, row=0)
    ttk.Label(login_window_frame, image=logo_smkn_5).grid(column=1, row=1)
    ttk.Label(login_window_frame, text='SERVER E - VOTING PEMILIHAN\nKETUA DAN WAKIL KETUA OSIS\nSMKN 5 KOTA TANGERANG', font=('Times New Roman', 18, 'bold'), justify=CENTER).grid(column=2, row=1, padx=40)
    ttk.Label(login_window_frame, image=logo_osis).grid(column=3, row=1)
    error_msg.grid(column=2, row=4)
    ttk.Label(login_window_frame, text='By Airell Zulkarnain', font=('Times New Roman', 10, 'normal')).grid(column=2, row=5, pady=(200, 0))
    masukan_passcode.grid(column=2, row=2, sticky=(W, E), pady=(50, 10))
    tombol_masuk.grid(column=2, row=3, sticky=(W, E))


    masukan_passcode.focus()
    masukan_passcode.bind('<Return>', lambda x: tombol_masuk.invoke())


    root.mainloop()
