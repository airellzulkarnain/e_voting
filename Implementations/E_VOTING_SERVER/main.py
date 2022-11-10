from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import SessionLocal, engine
from server import app
from style import stylize
from time import sleep
import models, crud
import multiprocessing
import uvicorn
import random
import string
import os
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
def create_passcode(db: Session): 
    if db.scalar(select(models.Passcode)) is None:
        passcode = models.Passcode(keyword='admin')
        db.add(passcode)
        db.commit()

@get_db
def masuk(db: Session):
    if crud.cek_passcode(db, passcode.get()):
        main_window()
    else:
        error_msg.configure(text='Gagal Masuk !')


server = None
gambar_pasangan = dict()

def main_window():
    nomor_urut = StringVar()
    nomor_urut.set('1')
    nama_ketua = StringVar()
    nama_wakil = StringVar()
    token = StringVar()
    token.set('1')
    new_passcode = StringVar()
    gambar_ketua: str = ''
    gambar_wakil: str = ''
    def no_close():
        pass

    def start_server():
        for child in tambah_paslon_frame.winfo_children(): 
                child.state(['disabled'])
        treeview_pasangan.state(['disabled'])
        global server
        server = multiprocessing.Process(target=run_api, daemon=True)
        server.start()
        tombol_mulai.configure(text='Berhenti', command=stop_server)

    def stop_server():
        server.terminate()
        refresh()
        tombol_mulai.configure(text='Mulai', command=start_server)
        for child in tambah_paslon_frame.winfo_children(): 
                child.state(['!disabled'])
        treeview_pasangan.state(['!disabled'])

    @get_db
    def ubah_pasangan(db: Session): 
        pass

    @get_db
    def hapus_pasangan(db: Session):
        try: 
            nomor_urut = treeview_pasangan.item(treeview_pasangan.selection()[0])['values'][0]
            if messagebox.askyesno('Warning', 'Apakah anda yakin ingin menghapus pasangan ?', icon='warning'):
                crud.hapus_pasangan(db, nomor_urut)
                tombol_refresh_paslon.invoke()
        except IndexError:
            pass

    @get_db
    def lihat_token(db: Session):
        tombol_lihat_token.state(['disabled'])
        def close():
            tombol_lihat_token.state(['!disabled'])
            token_window.destroy()
        
        token_window = Toplevel(root)
        token_window.title('Token')
        token_window.geometry('300x300')
        token_window.resizable(FALSE, FALSE)
        token_window.protocol('WM_DELETE_WINDOW', close)
        lihat_token_frame = ttk.Frame(token_window)
        lihat_token_frame.grid(column=0, row=0, sticky=(N,E,W,S))
        treeview_token = ttk.Treeview(lihat_token_frame, columns=('token', 'terpakai'), show='headings')
        treeview_token.heading('token', text='Token')
        treeview_token.heading('terpakai', text='Terpakai')
        treeview_token.column('token', width=120)
        treeview_token.column('terpakai', width=120)
        treeview_token.grid(column=1, row=1, sticky=(N,E,W,S))
        scrollbar_token = ttk.Scrollbar(lihat_token_frame, orient=VERTICAL, command=treeview_token.yview)
        scrollbar_token.grid(column=2, row=1, sticky=(S, N))
        button_cetak = ttk.Button(lihat_token_frame, text='Cetak Token', command=cetak_token)
        button_cetak.grid(column=1, columnspan=2, row=2, sticky=(N,E,W,S))
        treeview_token.configure(yscrollcommand=scrollbar_token.set)
        for token in crud.lihat_token(db):
            treeview_token.insert('', 'end', values=(token.keyword, 'Sudah' if token.terpakai else 'Belum'))
        token_window.rowconfigure(0, weight=1)
        token_window.columnconfigure(0, weight=1)
        lihat_token_frame.columnconfigure(1, weight=1)
        lihat_token_frame.rowconfigure(1, weight=4)
        lihat_token_frame.rowconfigure(2, weight=1)

    @get_db
    def cetak_token(db: Session):
        crud.cetak_token(db)

    def refresh():
        treeview_pasangan.delete(*treeview_pasangan.get_children())
        ambil_pasangan()
        treeview_pasangan.update_idletasks()

    @get_db
    def masukan_pasangan(db: Session):
        global gambar_ketua
        global gambar_wakil
        if nama_ketua.get() != '' and nama_wakil.get() != '' and nomor_urut.get() != '' and gambar_ketua != '' and gambar_wakil != '': 
            if messagebox.askyesno('Info', 'Masukan Pasangan ?'):
                new_gambar_ketua = 'images/'+(''.join(random.choices(string.ascii_letters+string.digits, k=12))+'.'+os.path.basename(gambar_ketua).split('.')[1])
                new_gambar_wakil = 'images/'+(''.join(random.choices(string.ascii_letters+string.digits, k=12))+'.'+os.path.basename(gambar_wakil).split('.')[1])
                file_gambar_ketua = None
                file_gambar_wakil = None
                with open(gambar_ketua, 'rb') as gambar:
                    file_gambar_ketua = gambar.read()
                with open(new_gambar_ketua, 'wb') as file:
                    file.write(file_gambar_ketua)
                with open(gambar_wakil, 'rb') as gambar:
                    file_gambar_wakil = gambar.read()
                with open(new_gambar_wakil, 'wb') as file:
                    file.write(file_gambar_wakil)
                if crud.masukan_pasangan(db, nama_ketua.get(), nama_wakil.get(), new_gambar_ketua, new_gambar_wakil, int(nomor_urut.get())):
                    form_error.configure(text=' ')
                    messagebox.showinfo('Info', 'Pasangan berhasil ditambahkan')
                    label_gambar_ketua.configure(text='Gambar Ketua - No File Selected')
                    label_gambar_wakil.configure(text='Gambar Wakil - No File Selected')
                    tombol_gambar_wakil.configure(text='+')
                    tombol_gambar_ketua.configure(text='+')
                    nama_ketua.set('')
                    nama_wakil.set('')
                    nomor_urut.set('')
                    gambar_ketua = ''
                    gambar_wakil = ''
                    refresh()
        else: 
            form_error.configure(text='Tolong isi lengkapi semua form !')

    @get_db
    def ganti_passcode(db: Session):
        if messagebox.askyesno('warning', 'Apakah anda yakin ingin mengubah passcode ?', icon='warning'): 
            crud.ubah_passcode(db, new_passcode.get())
            new_passcode.set('')

    @get_db
    def buat_token(db: Session):
        if messagebox.askyesno('Info', 'Buat token ?'): 
            crud.buat_token(db, int(token.get()))

    def masukan_gambar_wakil():
        global gambar_wakil
        gambar_wakil = filedialog.askopenfilename(title='Choose an Image...', filetypes=[('image files', ('.png', '.jpg', '.jpeg', '.gif'))])
        label_gambar_wakil.configure(text=f'Gambar Ketua - File Selected')
        tombol_gambar_wakil.configure(text=os.path.basename(gambar_wakil))

    def masukan_gambar_ketua():
        global gambar_ketua
        gambar_ketua = filedialog.askopenfilename(title='Choose an Image...', filetypes=[('image files', ('.png', '.jpg', '.jpeg', '.gif'))])
        label_gambar_ketua.configure(text=f'Gambar Ketua - File Selected')
        tombol_gambar_ketua.configure(text=os.path.basename(gambar_ketua))
    
    @get_db
    def ambil_pasangan(db: Session):
        for pasangan in crud.ambil_pasangan(db):
            try:
                image_ketua = Image.open(pasangan.gambar_ketua)
                image_wakil = Image.open(pasangan.gambar_wakil)
                image_ketua.thumbnail((80, 80), Image.Resampling.LANCZOS)
                image_wakil.thumbnail((80, 80), Image.Resampling.LANCZOS)
                image_ketua_dan_wakil = Image.new('RGB', (120, 80), (250, 250, 250))
                image_ketua_dan_wakil.paste(image_ketua, (0, 0))
                image_ketua_dan_wakil.paste(image_wakil, (60, 0))
                global gambar_pasangan
                gambar_pasangan[pasangan.nomor_urut] = ImageTk.PhotoImage(image_ketua_dan_wakil)
                treeview_pasangan.insert('', 'end', image=gambar_pasangan[pasangan.nomor_urut], values=(pasangan.nomor_urut, pasangan.nama_ketua, pasangan.nama_wakil, pasangan.jumlah_suara))
            except:
                treeview_pasangan.insert('', 'end', values=(pasangan.nomor_urut, pasangan.nama_ketua, pasangan.nama_wakil, pasangan.jumlah_suara))

    login_window.destroy()
    main_window = Toplevel(root)
    main_window.wm_attributes('-fullscreen', 1)
    main_window.protocol('WM_DELETE_WINDOW', no_close)
    main_windows_frame = ttk.Frame(main_window, padding=(6, 10, 6, 10))
    main_windows_frame.grid(column=0, row=0, sticky=(N, E, W, S))

    tambah_paslon_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Tambah Pasangan'))
    masukan_nomor_urut = ttk.Spinbox(tambah_paslon_frame, from_=1.0, to=6.0, textvariable=nomor_urut)
    masukan_nama_ketua = ttk.Entry(tambah_paslon_frame, textvariable=nama_ketua)
    masukan_nama_wakil = ttk.Entry(tambah_paslon_frame, textvariable=nama_wakil)
    tombol_gambar_ketua = ttk.Button(tambah_paslon_frame, text='+', command=masukan_gambar_ketua)
    tombol_gambar_wakil = ttk.Button(tambah_paslon_frame, text='+', command=masukan_gambar_wakil)
    tombol_tambah = ttk.Button(tambah_paslon_frame, text='Tambah', command=masukan_pasangan)

    passcode_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Ubah Passcode'))
    masukan_ubah_passcode = ttk.Entry(passcode_frame, textvariable=new_passcode, show='*')
    tombol_ubah_passcode = ttk.Button(passcode_frame, text='Ubah', command=ganti_passcode)
    masukan_ubah_passcode.grid(column=1, row=1, sticky=(W, E), padx=4, pady=6)
    tombol_ubah_passcode.grid(column=2, row=1, sticky=(W, E), padx=4, pady=6)

    ttk.Label(tambah_paslon_frame, text='Nomor Urut').grid(column=1, row=1, sticky=(W, E))
    masukan_nomor_urut.grid(column=1, row=2, sticky=(W, E))
    masukan_nomor_urut.state(['readonly'])
    ttk.Label(tambah_paslon_frame, text='Nama Ketua').grid(column=1, row=3, sticky=(W, E))
    masukan_nama_ketua.grid(column=1, row=4, sticky=(W, E))
    ttk.Label(tambah_paslon_frame, text='Nama Wakil').grid(column=1, row=5, sticky=(W, E))
    masukan_nama_wakil.grid(column=1, row=6, sticky=(W, E))
    label_gambar_ketua = ttk.Label(tambah_paslon_frame, text='Gambar Ketua - No File Selected', width=35)
    tombol_gambar_ketua.grid(column=1, row=8, sticky=(W, E), padx=4, pady=6)
    label_gambar_wakil = ttk.Label(tambah_paslon_frame, text='Gambar Wakil - No File Selected', width=35)
    label_gambar_ketua.grid(column=1, row=7, sticky=(W, E))
    label_gambar_wakil.grid(column=1, row=9, sticky=(W, E))
    tombol_gambar_wakil.grid(column=1, row=10, sticky=(W, E), padx=4, pady=6)
    tombol_tambah.grid(column=1, row=11, sticky=(W, E), padx=4, pady=6)
    form_error = ttk.Label(tambah_paslon_frame, text=' ', foreground='red', width=35)
    form_error.grid(column=1, row=12, sticky=(W, E))
    paslon_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Pasangan'))
    treeview_pasangan = ttk.Treeview(paslon_frame, columns=('nomor_urut', 'nama_ketua', 'nama_wakil', 'jumlah_suara'), style='paslon.Treeview')
    treeview_pasangan.heading('nomor_urut', text='Nomor Urut')
    treeview_pasangan.heading('nama_ketua', text='Nama Ketua')
    treeview_pasangan.heading('nama_wakil', text='Nama Wakil')
    treeview_pasangan.heading('jumlah_suara', text='Jumlah Suara')
    treeview_pasangan.column('nomor_urut', width=30, anchor='center')
    treeview_pasangan.column('jumlah_suara', width=30, anchor='center')
    treeview_pasangan.column('#0', width=75)
    treeview_pasangan.bind('<<TreeviewSelect>>', )
    scrollbar_pasangan = ttk.Scrollbar(paslon_frame, orient=VERTICAL, command=treeview_pasangan.yview)
    treeview_pasangan.configure(yscrollcommand=scrollbar_pasangan.set)
    treeview_pasangan.grid(column=0, row=0, sticky=(N,E,W,S))
    scrollbar_pasangan.grid(column=1, row=0, sticky=(N,E,W,S))
    button_frame = ttk.Frame(paslon_frame)
    button_frame.grid(column=0, row=1, sticky=(N,E,W,S))
    tombol_update_paslon = ttk.Button(button_frame, text='Update', command=ubah_pasangan)
    tombol_delete_paslon = ttk.Button(button_frame, text='Delete', command=hapus_pasangan)
    tombol_refresh_paslon = ttk.Button(button_frame, text='Refresh', command=refresh)
    tombol_update_paslon.grid(column=1,row=0, sticky=(W, E), padx=4, pady=2)
    tombol_delete_paslon.grid(column=2,row=0, sticky=(W, E), padx=4, pady=2)
    tombol_refresh_paslon.grid(column=3,row=0, sticky=(W, E), padx=4, pady=2)

    paslon_frame.columnconfigure(0, weight=1)
    paslon_frame.rowconfigure(0, weight=1)
    token_frame = ttk.LabelFrame(main_windows_frame, labelwidget=ttk.Label(main_windows_frame, text='Verifikasi Token'))
    masukan_jumlah_token = ttk.Spinbox(token_frame, from_=1.0, to=200.0, textvariable=token)
    tombol_buat_token = ttk.Button(token_frame, text='Buat', command=buat_token)
    tombol_lihat_token = ttk.Button(token_frame, text='Lihat', command=lihat_token)
    tombol_mulai = ttk.Button(main_windows_frame, text='Mulai', command=start_server)
    tombol_keluar = ttk.Button(main_windows_frame, text='Tutup', command=root.destroy, style='keluar.TButton')
    masukan_jumlah_token.grid(column=1, row=1, sticky=(W, E))
    masukan_jumlah_token.state(['readonly'])
    tombol_buat_token.grid(column=2, row=1, sticky=(W, E), padx=4, pady=6)
    tombol_lihat_token.grid(column=3, row=1, sticky=(W, E), padx=4, pady=6)
    tambah_paslon_frame.grid(column=1, row=1, rowspan=3, sticky=(N, E, W, S))
    paslon_frame.grid(column=2, row=1, columnspan=2, sticky=(N, E, W, S))
    token_frame.grid(column=2, row=2, sticky=(N, E, W, S))
    passcode_frame.grid(column=2, row=3, sticky=(N, E, W, S))
    tombol_mulai.grid(column=3, row=2, sticky=(N, E, W, S), padx=4, pady=6)
    tombol_keluar.grid(column=3, row=3, sticky=(N, E, W, S), padx=4, pady=6)
    ambil_pasangan()

    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)

    main_windows_frame.columnconfigure(1, weight=1)
    main_windows_frame.columnconfigure(2, weight=6)
    main_windows_frame.columnconfigure(3, weight=1)
    main_windows_frame.rowconfigure(1, weight=100)
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
    multiprocessing.freeze_support()
    create_passcode()
    root = Tk()
    login_window = Toplevel(root)
    login_window_frame = ttk.Frame(login_window, padding=(4, 6, 4, 6))
    passcode = StringVar()
    masukan_passcode = ttk.Entry(login_window_frame, textvariable=passcode, font=('Times New Roman', 16, 'normal'), justify=CENTER, show='*')
    tombol_masuk = ttk.Button(login_window_frame, text='Masuk', command=masuk, style='login.TButton')
    logo_smkn_5 = ImageTk.PhotoImage(Image.open(r'images\logo_smkn_5.png').resize((120, 150)))
    logo_osis = ImageTk.PhotoImage(Image.open(r'images\logo_osis.png').resize((120, 120)))
    error_msg = ttk.Label(login_window_frame, text=' ', foreground='red')
    stylize(ttk.Style)

    root.withdraw()

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
