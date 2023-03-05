from tkinter import *
from Login import login
from Registro import registro

'''
    *
    * @author CALERO
'''

# ------------------------- Funcion de nuestra pantalla principal ------------------------------------------------
def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("450x480")
    pantalla.iconbitmap('imagenes/logo-fisi-usar.ico')
    pantalla.title("Computacion Visual - Jocker")

    # Creamos un canvas y establecemos la imagen de fondo
    global canvas
    canvas = Canvas(pantalla, width=pantalla.winfo_width(), height=pantalla.winfo_height())
    canvas.pack(fill=BOTH, expand=True)
    imagen_fondo = PhotoImage(file="imagenes/pantalla-principal.png")
    canvas.create_image(0, 0, image=imagen_fondo, anchor=NW)

    # Agregamos el evento de click en el canvas
    canvas.bind("<Button-1>", detectar_sesion_registrar)

    pantalla.mainloop()

def detectar_sesion_registrar(event):
    # Obtenemos las coordenadas del clic
    x = event.x
    y = event.y

    # Verificamos si se ha hecho clic en el botón de iniciar sesión
    if 133 <= x <= 313 and 177 <= y <= 259:
        login(pantalla)
    # Verificamos si se ha hecho clic en el botón de registro
    elif 133 <= x <= 313 and 268 <= y <= 350:
        registro(pantalla)


pantalla_principal()
