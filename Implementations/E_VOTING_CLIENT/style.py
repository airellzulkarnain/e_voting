from tkinter.ttk import Style


def stylize(style: Style):
    style = style()
    style.theme_use('alt')
    style.configure("TButton", background="#008cff", foreground="white", relief="flat")
    style.map(
        "TButton", background=[("active", "#008cff")], relief=[("pressed", "solid")]
    )
    style.configure("TFrame", background="whitesmoke")
    style.configure("selected.TFrame", background="blue")
    style.configure("TLabel", background="whitesmoke", font=('Arial', 14, 'normal'))
    style.configure("TEntry", background="whitesmoke")
    style.configure('masuk.TButton', font=('Arial', 16, 'bold'))
    style.configure('pilih.TButton', font=('Arial', 18, 'bold'))
    style.configure("header1.TLabel", font=('Arial', 20, 'bold'))