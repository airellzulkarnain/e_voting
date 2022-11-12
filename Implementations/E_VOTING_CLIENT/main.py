import requests
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from style import stylize
from time import sleep



def no_close():
    pass

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
    login_window()

root = Tk()
root.title('E - Voting | Client')
root.geometry(f'300x70+{root.winfo_screenwidth()//2 - 150}+{root.winfo_screenheight()//2 - 35}')
root.resizable(FALSE, FALSE)
stylize(ttk.Style)

logo_pemilu = None
url = ''
nisn = ''
nomor_urut = 0
gambar_pasangan = dict()
temp_nisn = StringVar()
temp_token = StringVar()
ip = StringVar()
masukan_ip = ttk.Entry(root, textvariable=ip)
start_button = ttk.Button(root, text='Mulai', command=mulai)

ttk.Label(root, text='IP Address Server: ').grid(column=0, row=0, sticky=(N, E, W, S))
masukan_ip.grid(column=0, row=1, sticky=(N, E, W, S))
start_button.grid(column=0, row=2, sticky=(N, E, W, S))

masukan_ip.bind('<Return>', lambda e: start_button.invoke())
masukan_ip.focus()

root.columnconfigure(0, weight=1)

def load_image(image_url: str, resize: tuple | None = None):
    if resize:
        return ImageTk.PhotoImage(Image.open(BytesIO(requests.get(url+image_url).content)).resize(resize))
    return ImageTk.PhotoImage(Image.open(BytesIO(requests.get(url+image_url).content)))


def login_window():
    def pilih_pasangan():
        pass

    def masuk():
        res = requests.post(url+'verifikasi_token', data={"token": temp_token.get(), "nisn": temp_nisn.get()})
        if (res.status_code == 200 and res.json()) or temp_nisn.get() == 'admin': 
            global nisn
            nisn = res.json()
            login_window_frame.grid_forget()
            pemilihan_window()

    def pemilihan_window():
        kumpulan_kartu = dict()
        def buat_kartu_paslon(nama_ketua: str, nama_wakil: str, gambar_ketua:str, gambar_wakil: str, _nomor_urut: str)->ttk.Frame:
            kartu = ttk.Frame(canvas_pasangan_calon)
            global gambar_pasangan
            def pilih():
                kartu.configure(style='selected.TFrame')
                global nomor_urut
                nomor_urut = _nomor_urut
                print(nomor_urut)
            gambar_pasangan[_nomor_urut] = [load_image(gambar_ketua, (200, 270)), load_image(gambar_wakil, (200, 270))]
            ttk.Label(kartu, text=_nomor_urut, anchor='center').grid(column=1, columnspan=2, row=1, sticky=NSEW)
            ttk.Label(kartu, text='Ketua', anchor='center').grid(column=1, row=2, sticky=NSEW)
            ttk.Label(kartu, text='Wakil', anchor='center').grid(column=2, row=2, sticky=NSEW)
            ttk.Label(kartu, image=gambar_pasangan[_nomor_urut][0]).grid(column=1, row=3, sticky=NSEW)
            ttk.Label(kartu, image=gambar_pasangan[_nomor_urut][1]).grid(column=2, row=3, sticky=NSEW)
            ttk.Label(kartu, text=nama_ketua, anchor='center').grid(column=1, row=4, sticky=NSEW)
            ttk.Label(kartu, text=nama_wakil, anchor='center').grid(column=2, row=4, sticky=NSEW)
            kartu.rowconfigure(1, weight=1)
            kartu.rowconfigure(2, weight=1)
            kartu.rowconfigure(3, weight=1)
            kartu.rowconfigure(4, weight=1)
            kartu.columnconfigure(1, weight=1)
            kartu.columnconfigure(2, weight=1)
            kartu.bind('<Button-1>', pilih)
            return kartu
        
        frame_pemilihan = ttk.Frame(main_window)
        ttk.Label(frame_pemilihan, text='PASANGAN CALON KETUA DAN WAKIL KETUA OSIS', anchor='center', style='header1.TLabel').grid(column=1, row=1, sticky=NSEW)
        canvas_pasangan_calon = Canvas(frame_pemilihan)
        canvas_pasangan_calon.grid(column=1, row=2, sticky=NSEW)
        scrollbar_canvas = ttk.Scrollbar(frame_pemilihan, orient=HORIZONTAL, command=canvas_pasangan_calon.xview)
        scrollbar_canvas.grid(column=1, row=3, sticky=EW)
        canvas_pasangan_calon.configure(xscrollcommand=scrollbar_canvas.set)
        button_pilih = ttk.Button(frame_pemilihan, text='PILIH', command=pilih_pasangan, style='pilih.TButton')
        res = requests.get(url+'ambil_pasangan').json()
        for paslon in res:
            kumpulan_kartu[str(paslon['nomor_urut'])] = buat_kartu_paslon(paslon['nama_ketua'], paslon['nama_wakil'], paslon['gambar_ketua'], paslon['gambar_wakil'], paslon['nomor_urut'])
            canvas_pasangan_calon.create_window(10, 10, anchor=NW, window=kumpulan_kartu[str(paslon['nomor_urut'])], width=400 ,height=540)
        button_pilih.grid(column=1, row=4, sticky=NSEW)
        frame_pemilihan.grid(column=0, row=0, sticky=NSEW)
        frame_pemilihan.columnconfigure(1, weight=1)
        frame_pemilihan.rowconfigure(1, weight=1)
        frame_pemilihan.rowconfigure(2, weight=6)
        frame_pemilihan.rowconfigure(4, weight=1)


    def terimakasih_window():
        pass

    main_window = Toplevel(root)
    main_window.wm_attributes('-fullscreen', 1)
    main_window.protocol('WM_DELETE_WINDOW', no_close)
    main_window.bind('<Control-t><Key-a>', lambda e: root.destroy())
    login_window_frame = ttk.Frame(main_window)
    login_window_frame.grid(column=0, row=0, sticky=NSEW)

    main_window.rowconfigure(0, weight=1)
    main_window.columnconfigure(0, weight=1)

    global logo_pemilu
    form_frame = ttk.Frame(login_window_frame)
    logo_pemilu = load_image('images/pemilu_osis_smkn_5_kota_tangerang.png')
    ttk.Label(login_window_frame, image=logo_pemilu, anchor='center').grid(column=1, row=1, sticky=NSEW)
    masukan_nisn = ttk.Entry(form_frame, textvariable=temp_nisn, font=('Arial', 14, 'normal'))
    masukan_token = ttk.Entry(form_frame, textvariable=temp_token, font=('Arial', 14, 'normal'))
    tombol_masuk = ttk.Button(form_frame, text='Masuk', padding=(12, 10, 12, 10), command=masuk, style='masuk.TButton')
    form_frame.grid(column=2, row=1, sticky=NSEW)
    ttk.Label(form_frame, text='PEMILIHAN UMUM OSIS', style='header1.TLabel', anchor='center').grid(column=1, row=1, sticky=EW, pady=(root.winfo_screenheight()//3, 20))
    ttk.Label(form_frame, text='NISN').grid(column=1, row=2, sticky=EW, pady=6, padx=8)
    masukan_nisn.grid(column=1, row=3, sticky=EW, pady=6, padx=8)
    ttk.Label(form_frame, text='Token').grid(column=1, row=4, sticky=EW, pady=6, padx=8)
    masukan_token.grid(column=1, row=5, sticky=EW, pady=6, padx=8)
    tombol_masuk.grid(column=1, row=6, sticky=EW, pady=6, padx=8)


    form_frame.columnconfigure(1, weight=1)
    login_window_frame.rowconfigure(1, weight=1)
    login_window_frame.columnconfigure(1, weight=1)
    login_window_frame.columnconfigure(2, weight=1)

root.mainloop()