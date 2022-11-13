from tkinter.ttk import Style


def stylize(style: Style):
    style = style()
    style.configure('header1.TLabel', font=('Arial', 24, 'bold'))
    style.configure('header2.TLabel', font=('Arial', 18, 'normal'))
    style.configure('TScale', foreground='skyblue')
    style.map('TScale', foreground=[('disabled', 'skyblue')])