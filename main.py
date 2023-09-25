import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
# from analizador import analizar
from analizador import genera_reporte, analizar, errores_en
import sys
import os


class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#2c2e2f",
            foreground="#e8e8e8",
            insertbackground="#444546",
            selectbackground="#5b5d5d",
            width=75,
            height=26,
            font=("Courier New", 11),
        )

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=35, bg="#444546")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="#e8e8e8",
                font=("Courier New", 11, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto 1")
        self.geometry("750x510")
        self.config(background="#f0f0f0")
        self.centrar(self, 750, 510)
        self.resizable(0, 0)
        self.overrideredirect(True)
        self.scroll = ScrollText(self)
        self.scroll.place(x=5, y=25)
        self.after(200, self.scroll.redraw())
        # self.scroll_for_analisis = ScrollText(self)
        # self.scroll_for_analisis.place(x=550, y=24)
        # labels
        self.lbl_editable = Label(self, text="[ Área editable ]", bg=(
            "#f0f0f0"), fg=("#151718"), font=("Lucida Sans", 10))
        self.lbl_editable.place(x=300, y=4)

        # self.lbl_analisis = Label(self, text="[ Análisis generado ]", bg=(
        #     "#f0f0f0"), fg=("#151718"), font=("Lucida Sans", 10))
        # self.lbl_analisis.place(x=750, y=3)

        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=self.filemenu, background='#2b2b2b',
                              foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu.add_command(label="Abrir", command=self.abrir_archivo, background='#2b2b2b',
                                  foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu.add_command(label="Guardar", command=self.guardar_como, background='#2b2b2b',
                                  foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu.add_command(label="Salir", command=self.quit, background='#2b2b2b',
                                  foreground='white', activeforeground='black', activebackground='gray52')

        btn_Analizar = Button(self, text="Analizar", command=self.analizar_json,
                              width=10, height=1, font=("Lucida Sans", 10), bg="#f7ff19")
        btn_Analizar.place(x=180, y=475)

        btn_Errores = Button(self, text="Errores", command=self.fn_errores,
                             width=10, height=1, font=("Lucida Sans", 10), bg="#f7ff19")
        btn_Errores.place(x=280, y=475)

        btn_Reportes = Button(self, text="Reporte", command=self.generar_reporte,
                              width=10, height=1, font=("Lucida Sans", 10), bg="#f7ff19")
        btn_Reportes.place(x=380, y=475)
        btn_inicializar = Button(self, text="Inicializar", command=self.inicializar,
                                 width=10, height=1, font=("Lucida Sans", 10), bg="#f7ff19")
        btn_inicializar.place(x=480, y=475)

    def centrar(self, ventana, ancho, alto):  # centra la ventana
        altura_pantalla = ventana.winfo_screenheight()
        ancho_pantalla = ventana.winfo_screenwidth()
        ancho_x = (ancho_pantalla//2) - (ancho//2)
        altura_y = (altura_pantalla//2) - (alto//2)
        ventana.geometry(f"+{ancho_x}+{altura_y}")

    def abrir_archivo(self):
        filepath = askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        self.scroll.delete(1.0, tk.END)  # Limpia el área de texto
        with open(filepath, "r") as input_file:
            text = input_file.read()
            # Inserta la información del archivo seleccionado
            self.scroll.insert(tk.END, text)
        self.title(f"Proyecto 1 - {filepath}")

    def guardar_como(self):
        filepath = asksaveasfilename(
            defaultextension="json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.scroll.get(1.0, tk.END)
            output_file.write(text)
        self.title(f"Proyecto 1 - {filepath}")

    def generar_reporte(self):
        print("Generando...")
        # self.scroll_for_analisis.delete(1.0, tk.END)
        dato1 = self.scroll.get(1.0, tk.END)
        arbol = genera_reporte(dato1)
        # print(arbol.dot.source)
        arbol.dot.view()

    def analizar_json(self):
        self.lbl_analisis = Label(self, text="[ Análisis generado ]", bg=(
            "#f0f0f0"), fg=("#151718"), font=("Lucida Sans", 10))
        self.lbl_analisis.place(x=300, y=3)
        print("Analizando...")
        dato2 = self.scroll.get(1.0, tk.END)
        self.scroll.delete(1.0, tk.END)
        analisis = ""
        analisis = analizar(dato2)
        tokensIn = analisis.count("Token")
        long = len(analisis)
        valor_nuevo = analisis[1:long-1]
        nuevo = valor_nuevo.split(
            "Token")
        while valor_nuevo:
            for i in range(tokensIn):
                self.scroll.insert(
                    tk.END, f"Token: {nuevo[i+1]}"+"\n")
            break

    def fn_errores(self):
        print("Buscando errores...")
        dato3 = self.scroll.get(1.0, tk.END)
        get_errores = errores_en(dato3)
        valor_menos = len(get_errores)
        print(get_errores[1:valor_menos-1])

    def inicializar(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)


app = Ventana()
app.mainloop()
