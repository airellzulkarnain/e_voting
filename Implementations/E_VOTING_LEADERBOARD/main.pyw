from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from io import BytesIO
from style import stylize
import string
import threading
from time import sleep
import requests
import random


def update_progress():
    global jumlah_suara
    while True:
        for pasangan in requests.get(url+'ambil_pasangan').json(): 
            jumlah_suara[pasangan['nomor_urut']][0].set(str(requests.get(url+f'ambil_persentase/{pasangan["nomor_urut"]}').json())[:5]+'%')
            jumlah_suara[pasangan['nomor_urut']][1].set(str(requests.get(url+f'ambil_persentase/{pasangan["nomor_urut"]}').json()))
        sleep(600)

def update_timer():
    global timer
    while True:
        time = timer.get().split(':')
        if f'{time[0]}:{time[1]}' != '00:00':
            if time[1] == '00':
                time[0] = f'0{int(time[0])-1}'
                time[1] = '59'
            else: 
                time[1] = int(time[1])-1
                time[1] = f'0{time[1]}' if int(time[1]) < 10 else time[1]
            timer.set(f'{time[0]}:{time[1]}')
        else: 
            timer.set('10:00')
        sleep(1)


def call_main_window():
    def pasangan_calon(nama_ketua: str, nama_wakil: str, gambar_ketua: str, gambar_wakil: str, nomor_urut: str)->ttk.Frame:
        global jumlah_suara
        global kumpulan_gambar
        jumlah_suara[nomor_urut] = [StringVar(), StringVar()]
        kumpulan_gambar[nomor_urut] = [load_gambar(gambar_ketua, (120, 160)), load_gambar(gambar_wakil, (120, 160))]
        pasangan = ttk.Frame(main_frame, relief='solid', padding=(10, 20, 20, 10))
        ttk.Label(pasangan, text=nomor_urut, anchor='center', style='header2.TLabel', width=2).grid(column=1, row=1, rowspan=2, sticky=NSEW)
        ttk.Label(pasangan, image=kumpulan_gambar[nomor_urut][0], anchor='center', width=25, style='header2.TLabel').grid(column=2, row=1, rowspan=2, sticky=NSEW)
        ttk.Label(pasangan, image=kumpulan_gambar[nomor_urut][1], anchor='center', width=25, style='header2.TLabel').grid(column=3, row=1, rowspan=2, sticky=NSEW)
        ttk.Label(pasangan, text=f'{nama_ketua} & {nama_wakil}', anchor='center', width=50, style='header2.TLabel').grid(column=4, row=1, sticky=NSEW)
        ttk.Progressbar(pasangan, mode='determinate', orient=HORIZONTAL, length=100, variable=jumlah_suara[nomor_urut][1]).grid(column=4, row=2, sticky=EW)
        ttk.Label(pasangan, textvariable=jumlah_suara[nomor_urut][0], anchor='center', style='header2.TLabel', width=5).grid(column=5, row=1, rowspan=2, sticky=NSEW)
        pasangan.columnconfigure(1, weight=1)
        pasangan.columnconfigure(2, weight=2)
        pasangan.columnconfigure(3, weight=2)
        pasangan.columnconfigure(4, weight=10)
        pasangan.columnconfigure(5, weight=1)
        pasangan.rowconfigure(1, weight=1)
        pasangan.rowconfigure(2, weight=1)
        return pasangan

    
    def load_gambar(url_gambar: str, resize: tuple | None = None):
        if resize: 
            return ImageTk.PhotoImage(Image.open(BytesIO(requests.get(url+url_gambar).content)).resize(resize))
        return ImageTk.PhotoImage(Image.open(BytesIO(requests.get(url+url_gambar).content)))

    main_window = Toplevel(root)
    main_window.attributes('-fullscreen', 1)
    main_window.protocol('WM_DELETE_WINDOW', root.destroy)
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)
    main_frame = ttk.Frame(main_window)
    main_frame.grid(column=0, row=0, sticky=NSEW)
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    ttk.Label(main_frame, text='PASANGAN CALON KETUA DAN WAKIL KETUA OSIS', anchor='center', style='header1.TLabel').grid(row=0, column=1, sticky=NSEW, pady=(20, 50))

    counter = 1
    global kumpulan_pasangan
    global timer
    for pasangan in requests.get(url+'ambil_pasangan').json():
        kumpulan_pasangan[pasangan['nomor_urut']] = pasangan_calon(pasangan['nama_ketua'], pasangan['nama_wakil'], pasangan['gambar_ketua'], pasangan['gambar_wakil'], pasangan['nomor_urut'])
        kumpulan_pasangan[pasangan['nomor_urut']].grid(column=1, row=counter, sticky=EW)
        counter += 1
    ttk.Label(main_frame, textvariable=timer, font=('Calibri', 28, 'normal'), anchor=W).grid(column=1, row=counter, sticky=NSEW)
    threading.Thread(target=update_timer, daemon=True).start()
    threading.Thread(target=update_progress, daemon=True).start()


def mulai():
    for char in ip.get():
        if char not in string.digits+'.':
            messagebox.showerror('Error', 'Alamat IP tidak valid')
            return
    try: 
        requests.get(f'http://{ip.get()}:8000/', timeout=3).status_code
        global url
        url = f'http://{ip.get()}:8000/'
    except:
        return
    
    root.withdraw()
    call_main_window()

root = Tk()
root.title('E - Voting | LEADERBOARD')
root.geometry(f'300x70+{root.winfo_screenwidth()//2 - 150}+{root.winfo_screenheight()//2 - 35}')
root.resizable(FALSE, FALSE)
stylize(ttk.Style)

url = ''
jumlah_suara = dict()
kumpulan_gambar = dict()
kumpulan_pasangan = dict()
timer = StringVar()
timer.set('00:00')
ip = StringVar()
masukan_ip = ttk.Entry(root, textvariable=ip)
start_button = ttk.Button(root, text='Mulai', command=mulai)

ttk.Label(root, text='IP Address Server: ').grid(column=0, row=0, sticky=NSEW)
masukan_ip.grid(column=0, row=1, sticky=NSEW)
start_button.grid(column=0, row=2, sticky=NSEW)

masukan_ip.bind('<Return>', lambda e: start_button.invoke())
masukan_ip.focus()

root.columnconfigure(0, weight=1)
root.mainloop()
