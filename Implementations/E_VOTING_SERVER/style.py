from tkinter.ttk import Style


def stylize(style: Style) -> None:
    style = style()
    style.theme_use("alt")
    style.configure("TButton", background="#008cff", foreground="white", relief="flat")
    style.configure("login.TButton", width=20, font=("Arial", 16, "normal"))
    style.map(
        "TButton", background=[("active", "#008cff")], relief=[("pressed", "solid")]
    )
    style.configure("TFrame", background="whitesmoke")
    style.configure("TLabelframe", background="whitesmoke")
    style.configure("TLabel", background="whitesmoke")
    style.configure("keluar.TButton", background="#f73829", foreground="white")
    style.map(
        "keluar.TButton",
        background=[("active", "#f73829")],
        relief=[("pressed", "solid")],
    )
    style.map("TLabel", background=[("disabled", "whitesmoke")])
    style.map("TEntry", background=[("disabled", "whitesmoke")])
    style.configure(
        "paslon.Treeview", rowheight=80, font=("Arial", 14, "normal")
    )
    style.map("paslon.Treeview", background=[("disabled", "whitesmoke")], foreground=[("disabled", "black")])
