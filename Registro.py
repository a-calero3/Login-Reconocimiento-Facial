from tkinter import *
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import os
'''
    *
    * @author CALERO
'''

# ------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def registro(pantalla):
    global usuario
    global contra  # Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1

    pantalla1 = Toplevel(pantalla)  # Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Sistema de Registro")
    pantalla1.geometry("420x650")  # Asignamos el tamaño de la ventana
    pantalla1.iconbitmap('imagenes/logo-fisi-usar.ico')  # Agregamos el icono de la facultad

    # Cargar la imagen de fondo
    global canvas
    canvas = Canvas(pantalla1, width=pantalla1.winfo_width(), height=pantalla1.winfo_height())
    canvas.pack(fill=BOTH, expand=True)
    imagen_fondo = PhotoImage(file="imagenes/registro.png")
    canvas.create_image(0, 0, image=imagen_fondo, anchor=NW)

    # --------- Empezaremos a crear las entradas ----------------------------------------
    usuario = StringVar()
    contra = StringVar()

    # Creamos los campos de entrada de usuario y contraseña
    usuario_entrada = Entry(pantalla1, textvariable=usuario)
    canvas.create_window(100, 340, window=usuario_entrada)
    contra_entrada = Entry(pantalla1, textvariable=contra, show="*")
    canvas.create_window(100, 430, window=contra_entrada)

    # ------------------------ Crearemos una funcion que se encargara de registrar el usuario ---------------------

    def registrar_usuario():
        usuario_info = usuario.get()  # Obetnemos la informacion alamcenada en usuario
        contra_info = contra.get()  # Obtenemos la informacion almacenada en contra

        archivo = open(usuario_info, "w")  # Abriremos la informacion en modo escritura
        archivo.write(usuario_info + "\n")  # escribimos la info
        archivo.write(contra_info)
        archivo.close()

        # Limpiaremos los text variable
        usuario_entrada.delete(0, END)
        contra_entrada.delete(0, END)

        # Ahora le diremos al usuario que su registro ha sido exitoso
        print("Registro Convencional Exitoso")
        pantalla1.destroy()

    # --------------------------- Funcion para almacenar el registro facial --------------------------------------

    def registro_facial():
        # Vamos a capturar el rostro
        cap = cv2.VideoCapture(0)  # Elegimos la camara con la que vamos a hacer la deteccion
        while (True):
            ret, frame = cap.read()  # Leemos el video
            cv2.imshow('Registro Facial', frame)  # Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
                break
        usuario_img = usuario.get()

        # crea la carpeta si no existe
        if not os.path.exists("registro-capturas"):
            os.mkdir("registro-capturas")

        nombre_archivo = usuario_img + ".jpg"
        ruta_archivo = os.path.join("registro-capturas", nombre_archivo)
        cv2.imwrite(ruta_archivo, frame)
        print("Ruta completa:", ruta_archivo)

        cap.release()  # Cerramos
        cv2.destroyAllWindows()

        usuario_entrada.delete(0, END)  # Limpiamos los text variables
        contra_entrada.delete(0, END)
        print("Registro Facial Exitoso")
        pantalla1.destroy()

        # ----------------- Detectamos el rostro y exportamos los pixeles --------------------------

        #img = usuario_img + ".jpg"
        img = os.path.join("registro-capturas", usuario_img + ".jpg")
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)

        def reg_rostro(img, lista_resultados):
            data = pyplot.imread(img)
            for i in range(len(lista_resultados)):
                x1, y1, ancho, alto = lista_resultados[i]['box']
                x2, y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i + 1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg, (150, 200),
                                      interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen con un tamaño de 150x200

                # crea la carpeta si no existe
                if not os.path.exists("registro-capturas"):
                    os.mkdir("registro-capturas")

                nombre_archivo2 = usuario_img + ".jpg"
                ruta_archivo2 = os.path.join("registro-capturas", nombre_archivo2)
                cv2.imwrite(ruta_archivo2, cara_reg)

                pyplot.imshow(data[y1:y2, x1:x2])
            pyplot.show()

        reg_rostro(img, caras)

    def detectar_registro(event):
        # Obtenemos las coordenadas del clic
        x = event.x
        y = event.y

        # Verificamos si se ha hecho clic en el botón de inicio de sesión tradicional
        if 90 <= x <= 322 and 510 <= y <= 570:
            registrar_usuario()
        # Verificamos si se ha hecho clic en el botón de inicio de sesión facial
        elif 90 <= x <= 322 and 580 <= y <= 640:
            registro_facial()

    canvas.bind("<Button-1>", detectar_registro)
    pantalla1.mainloop()
