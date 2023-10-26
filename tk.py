import backend as bk


def select_char(color: int) -> str:
    sel_char = ""
    

    def choose_char(char: str):
        nonlocal sel_char, top
        sel_char = char
        top.destroy()

    top = tk.Toplevel(win)
    top.geometry("240x90")
    top.title("child")
    frame = tk.Frame(master=top)

    col = "w" if color == bk.WHITE else "b"

    for i, x in enumerate(but_chars):
        icon = icons[col + x.lower()]
        cmd = partial(choose_char, x)
        tk.Button(
            master=frame, text=x, width=45, height=45, command=cmd, image=icon
        ).grid(row=0, column=i)
    frame.pack(padx=15, pady=15)

    top.wait_window()

    return sel_char
