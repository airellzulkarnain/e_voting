from tkinter import *
from tkinter import ttk
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from server import app
import models, crud
import multiprocessing
import uvicorn
from PIL import Image, ImageTk


models.Base.metadata.create_all(bind=engine)


def no_close():
    pass

def get_db(func):
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(db)
        finally:
            db.close()
    return wrapper


@get_db
def masuk(db: Session):
    global error_msg
    if crud.login(db, passcode):
        pass # open the main window
    else:
        error_msg = ttk.Label(login_window_frame, text='Gagal masuk !', foreground='red')
        error_msg.grid(column=2, row=4)

root = Tk()
root.withdraw()
root.wm_attributes('-transparentcolor', 'purple')

login_window = Toplevel(root)
login_window.title('E - Voting Server | Login')
login_window.geometry(f'720x510+{root.winfo_screenwidth()//2 - 360}+{root.winfo_screenheight()//2 - 300}')
login_window.resizable(FALSE, FALSE)
login_window.protocol('WM_DELETE_WINDOW', root.destroy)

login_window_frame = ttk.Frame(login_window, padding=(4, 6, 4, 6))
login_window_frame.grid(column=0, row=0)
login_window_frame.rowconfigure(0, weight=1)
login_window_frame.columnconfigure(0, weight=1)
logo = ImageTk.PhotoImage(Image.open(r'images\logo_smkn_5.png').resize((120, 150)))

ttk.Label(login_window_frame, image=logo).grid(column=1, row=1)
ttk.Label(login_window_frame, text='SERVER E - VOTING PEMILIHAN\nKETUA DAN WAKIL KETUA OSIS\nSMKN 5 KOTA TANGERANG', font=('Times New Roman', 18, 'bold'), justify=CENTER).grid(column=2, row=1, padx=40)
ttk.Label(login_window_frame, image=logo).grid(column=3, row=1)
ttk.Label(login_window_frame, text='By Airell Zulkarnain', font=('Times New Roman', 12, 'normal')).grid(column=2, row=5, pady=(200, 0), sticky=(S))
passcode = StringVar()

style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', background = 'blue', foreground = 'white', width = 20, font=('Times New Roman', 16, 'normal'))
style.map('TButton', background=[('active','blue')])

masukan_passcode = ttk.Entry(login_window_frame, textvariable=passcode, font=('Times New Roman', 16, 'normal'), justify=CENTER)
tombol_masuk = ttk.Button(login_window_frame, text='Masuk', command=masuk, style='TButton')
masukan_passcode.grid(column=2, row=2, sticky=(W, E), pady=(50, 10))
tombol_masuk.grid(column=2, row=3, sticky=(W, E))
masukan_passcode.focus()
masukan_passcode.bind('<Return>', lambda x: tombol_masuk.invoke())

root.mainloop()