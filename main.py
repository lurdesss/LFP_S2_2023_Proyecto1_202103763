from tkinter import *
from tkinter import ttk, filedialog


class Menu():
    def __init__(self):
        self.principal()
        self.ventana.title("Analizador Léxico")
        self.centrar(self.ventana, 1000, 500)
        self.ventana.geometry("1000x500")
        self.frame_menu()

    def principal(self):
        self.ventana = Tk()
        self.ventana.resizable(0, 0)
        self.ventana.config(bg="#000000", relief="flat", bd=16)

    def centrar(self, ventana, ancho, alto):
        altura_pantalla = ventana.winfo_screenheight()
        ancho_pantalla = ventana.winfo_screenwidth()
        ancho_x = (ancho_pantalla//2) - (ancho//2)
        altura_y = (altura_pantalla//2) - (alto//2)
        ventana.geometry(f"+{ancho_x}+{altura_y}")

    def frame_menu(self):
        self.frame = Frame()
        self.frame.pack()
        self.frame.config(bg="#2F4F4F", width="1000",
                          height="500", bd=10)

        # Labels, texto titulo, texto archivo
        self.__lbl_Titulo = Label(self.frame, text="Analizador lexico", bg=(
            "#000000"), fg=("white"), font=("Arial", 14)).place(x=400, y=0)
        self.__lbl_Archivo = Label(self.frame, text="Archivo", bg=(
            "#000000"), fg=("white"), font=("Arial", 14)).place(x=100, y=100)
        # Buttons: Abrir, Guardar, Guardar como, Salir
        # Buttons: Analizar, Error, Reporte
        self.__btn_Analizar = Button(self.frame, text="Analizar", command=self.analizar_archivo,
                                     width=10, height=1, font=("Arial", 10), bg="#D5A273").place(x=640, y=410)
        self.__btn_Errores = Button(self.frame, text="Errores", command=self.error_archivo,
                                    width=10, height=1, font=("Arial", 10), bg="#D5A273").place(x=740, y=410)
        self.__btn_Reporte = Button(self.frame, text="Reporte", command=self.reporte_archivo,
                                    width=10, height=1, font=("Arial", 10), bg="#D5A273").place(x=840, y=410)
        # Text: area de texto entrada editable y f Analizador
        self.frame.mainloop()

    def abrir_archivo(self):
        Tk().withdraw()
        archivo = filedialog.askopenfilename(
            title="Seleccionar un archivo JSON",
            initialdir="./",
            filetypes=(
                ("Archivos JSON", "*.json"),
                ("Todos los archivos",  "*.*")
            )
        )
        if archivo == '':
            print('No se seleccionó ningun archivo\n')
            return None
        else:
            abrir_json = open(archivo, 'r', encoding='utf-8')
            texto = abrir_json.read()
            return texto

    def analizar_archivo(self):
        pass

    def error_archivo(self):
        pass

    def reporte_archivo(self):
        pass


Menu()
