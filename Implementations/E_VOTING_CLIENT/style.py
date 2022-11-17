from tkinter.ttk import Style


def stylize(style: Style):
    style = style()
    style.theme_use('alt')
    style.configure("TButton", background="#008cff", foreground="white", relief="flat")
    style.map(
        "TButton", background=[("active", "#008cff")], relief=[("pressed", "solid")]
    )
    style.configure("TFrame", background="whitesmoke")
    style.configure("selected.TFrame", background="skyblue")
    style.configure("kartu.TLabel", font=('Calibri', 14, 'normal'))
    style.configure("kartu_nama.TLabel", font=('Calibri', 14, 'normal'))
    style.configure("kartuselected.TLabel", background="skyblue", font=('Calibri', 14, 'bold'))
    style.configure("TLabel", background="whitesmoke", font=('Calibri', 14, 'normal'))
    style.configure("TEntry", background="whitesmoke")
    style.configure('masuk.TButton', font=('Calibri', 16, 'bold'))
    style.configure('pilih.TButton', font=('Calibri', 18, 'bold'))
    style.configure("header1.TLabel", font=('Calibri', 28, 'bold'))