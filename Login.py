from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
#from PIL import ImageTk, Image
#from deepface import DeepFace
#import mediapipe as mp
'''
    *
    * @author CALERO
'''

# ------------------------Funcion que asignaremos al boton login -------------------------------------------------
def login(pantalla):
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Sistema de Login")
    pantalla2.geometry("420x650")  # Creamos la ventana 300x250
    pantalla2.iconbitmap('imagenes/logo-fisi-usar.ico')  # Agregamos el icono de la facultad

    # Creamos un canvas y establecemos la imagen de fondo
    global canvas
    canvas = Canvas(pantalla2, width=pantalla2.winfo_width(), height=pantalla2.winfo_height())
    canvas.pack(fill=BOTH, expand=True)
    imagen_fondo = PhotoImage(file="imagenes/login.png")
    canvas.create_image(0, 0, image=imagen_fondo, anchor=NW)

    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

    # Creamos los campos de entrada de usuario y contraseña
    usuario_entrada2 = Entry(pantalla2, textvariable=verificacion_usuario)
    canvas.create_window(100, 340, window=usuario_entrada2)
    contra_entrada2 = Entry(pantalla2, textvariable=verificacion_contra, show="*")
    canvas.create_window(100, 440, window=contra_entrada2)


    # --------------------------Funcion para el Login Facial --------------------------------------------------------
    def login_facial():
        # ------------------------------Vamos a capturar el rostro-----------------------------------------------------
        cap = cv2.VideoCapture(0)  # Elegimos la camara con la que vamos a hacer la deteccion
        while (True):
            ret, frame = cap.read()  # Leemos el video
            cv2.imshow('Login Facial', frame)  # Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
                break
        usuario_login = verificacion_usuario.get()  # Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir

        # crea la carpeta si no existe
        if not os.path.exists("capturas-guardadas"):
            os.mkdir("capturas-guardadas")

        nombre_archivo = usuario_login + "LOG.jpg"
        ruta_archivo = os.path.join("capturas-guardadas", nombre_archivo)
        cv2.imwrite(ruta_archivo, frame)

        cap.release()  # Cerramos
        cv2.destroyAllWindows()

        usuario_entrada2.delete(0, END)  # Limpiamos los text variables
        contra_entrada2.delete(0, END)

        # ----------------- Funcion para guardar el rostro --------------------------

        def log_rostro(img, lista_resultados):
            data = pyplot.imread(img)
            for i in range(len(lista_resultados)):
                x1, y1, ancho, alto = lista_resultados[i]['box']
                x2, y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i + 1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg, (150, 200),
                                      interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen 150x200

                if not os.path.exists("capturas-guardadas"):
                    os.mkdir("capturas-guardadas")

                nombre_archivo2 = usuario_login + "LOG.jpg"
                ruta_archivo2 = os.path.join("capturas-guardadas", nombre_archivo2)
                cv2.imwrite(ruta_archivo2, cara_reg)

                return pyplot.imshow(data[y1:y2, x1:x2])
            pyplot.show()

        # -------------------------- Detectamos el rostro-------------------------------------------------------
        img = os.path.join("capturas-guardadas", usuario_login + "LOG.jpg")
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        log_rostro(img, caras)

        # -------------------------- Funcion para comparar los rostros --------------------------------------------
        def orb_sim(img1, img2):
            orb = cv2.ORB_create()  # Creamos el objeto de comparacion

            kpa, descr_a = orb.detectAndCompute(img1, None)  # Creamos descriptor 1 y extraemos puntos claves
            kpb, descr_b = orb.detectAndCompute(img2, None)  # Creamos descriptor 2 y extraemos puntos claves

            comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Creamos comparador de fuerza

            matches = comp.match(descr_a, descr_b)  # Aplicamos el comparador a los descriptores

            regiones_similares = [i for i in matches if
                                  i.distance < 70]  # Extraemos las regiones similares en base a los puntos claves
            if len(matches) == 0:
                return 0
            return len(regiones_similares) / len(matches)  # Exportamos el porcentaje de similitud

        # ---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------

        # Vamos a importar la lista de archivos con la libreria os
        ruta = "registro-capturas"
        im_archivos = os.listdir(ruta)
        if usuario_login + ".jpg" in im_archivos:  # Comparamos los archivos con el que nos interesa
            rostro_reg = cv2.imread(os.path.join("registro-capturas", usuario_login + ".jpg"),
                                    0)  # Importamos el rostro del registro
            rostro_log = cv2.imread(os.path.join("capturas-guardadas", usuario_login + "LOG.jpg"),
                                    0)  # Importamos el rostro del inicio de sesion
            similitud = orb_sim(rostro_reg, rostro_log)
            if similitud >= 0.75: #factor de similitud
                print("Inicio de Sesion Exitoso")
                print("Bienvenido al sistema usuario: ", usuario_login)
                print("Compatibilidad con la foto del registro: ", similitud)
                #print("Emocion: ", sen)
                pantalla2.destroy()
            else:
                print("Rostro incorrecto, Certifique su usuario")
                print("Compatibilidad con la foto del registro: ", similitud)
                print("Incompatibilidad de rostros")
        else:
            print("Usuario no encontrado")

    # ------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------

    def verificacion_login():
        log_usuario = verificacion_usuario.get()
        log_contra = verificacion_contra.get()

        usuario_entrada2.delete(0, END)
        contra_entrada2.delete(0, END)

        lista_archivos = os.listdir()  # Vamos a importar la lista de archivos con la libreria os
        if log_usuario in lista_archivos:  # Comparamos los archivos con el que nos interesa
            archivo2 = open(log_usuario, "r")  # Abrimos el archivo en modo lectura
            verificacion = archivo2.read().splitlines()  # leera las lineas dentro del archivo ignorando el resto
            if log_contra in verificacion:
                print("Inicio de sesion exitoso")
                pantalla2.destroy()
            else:
                print("Contraseña incorrecta, ingrese de nuevo")
        else:
            print("Usuario no encontrado")

    def detectar_session(event):
        # Obtenemos las coordenadas del clic
        x = event.x
        y = event.y

        # Verificamos si se ha hecho clic en el botón de inicio de sesión tradicional
        if 90 <= x <= 322 and 510 <= y <= 570:
            verificacion_login()
        # Verificamos si se ha hecho clic en el botón de inicio de sesión facial
        elif 90 <= x <= 322 and 580 <= y <= 640:
            login_facial()

    canvas.bind("<Button-1>", detectar_session)
    pantalla2.mainloop()