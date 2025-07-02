import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import json
import os
import datetime


ARCHIVO_CONTRASENAS = "contrasenas.json" #odio saber que la "ñ" no funciona :(

def cargar_contrasenas():
    if os.path.exists(ARCHIVO_CONTRASENAS):
        with open(ARCHIVO_CONTRASENAS, "r") as f:
            return json.load(f)
    return {}

def guardar_contrasenas(contrasenas):
    with open(ARCHIVO_CONTRASENAS, "w") as f:
        json.dump(contrasenas, f, indent=4)

def generar_contrasena(longitud=16):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def agregar_contrasena():
    nombre = simpledialog.askstring("Nombre", "¿Para qué es esta contraseña?")
    if not nombre:
        return
    longitud = simpledialog.askinteger("Longitud", "Longitud de la contraseña:", initialvalue=16, minvalue=8, maxvalue=64)
    if not longitud:
        return
    contrasena = generar_contrasena(longitud)
    contrasenas = cargar_contrasenas()
    contrasenas[nombre] = contrasena
    guardar_contrasenas(contrasenas)
    messagebox.showinfo("Contraseña generada", f"Nombre: {nombre}\nContraseña: {contrasena}")

def mostrar_contrasenas():
    contrasenas = cargar_contrasenas()
    if not contrasenas:
        messagebox.showinfo("Contraseñas guardadas", "No hay contraseñas guardadas.")
        return
    ventana = tk.Toplevel(root)
    ventana.title("Contraseñas guardadas")
    texto = tk.Text(ventana, width=50, height=15)
    texto.pack(padx=10, pady=10)
    for nombre, contrasena in contrasenas.items():
        texto.insert(tk.END, f"{nombre}: {contrasena}\n")
    texto.config(state='disabled')

def mostrar_menu_contrasenas():
    #voton para ocultar el menù :v
    menu_principal.pack_forget()
    menu_contrasenas.pack(pady=20)

def volver_menu_principal():
    #voton para regresar
    menu_contrasenas.pack_forget()
    menu_principal.pack(pady=20)
    
def actualizar_fecha_hora():
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_fecha_hora.config(text=ahora)
    label_fecha_hora.after(1000, actualizar_fecha_hora)
    

root = tk.Tk()
root.title("BeccaTool - Herramientas")

def eliminar_contrasena():
    contrasenas = cargar_contrasenas()
    if not contrasenas:
        messagebox.showinfo("Eliminar contraseña", "No hay contraseñas guardadas.")
        return
    # Selección de nombre a eliminar
    nombres = list(contrasenas.keys())
    nombre = simpledialog.askstring("Eliminar contraseña", f"¿Cuál deseas eliminar?\nOpciones: {', '.join(nombres)}")
    if not nombre:
        return
    if nombre not in contrasenas:
        messagebox.showerror("Error", "No existe una contraseña con ese nombre.")
        return
    confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la contraseña '{nombre}'?")
    if confirm:
        del contrasenas[nombre]
        guardar_contrasenas(contrasenas)
        messagebox.showinfo("Eliminada", f"Contraseña '{nombre}' eliminada correctamente.")

#esto es lo principal
menu_principal = tk.Frame(root)
label_menu = tk.Label(menu_principal, text="Selecciona una herramienta:", font=("Arial", 14))
label_menu.pack(pady=10)
btn_contrasenas = tk.Button(menu_principal, text="Contraseñas", width=25, command=mostrar_menu_contrasenas)
btn_contrasenas.pack(pady=5)
menu_principal.pack(pady=20)

#// zaza del futuro si lees esto, aqui està el menù y sus logicas
menu_contrasenas = tk.Frame(root)
label_contra = tk.Label(menu_contrasenas, text="Gestor de Contraseñas", font=("Arial", 12))
label_contra.pack(pady=10)
btn_generar = tk.Button(menu_contrasenas, text="Generar y guardar contraseña", width=30, command=agregar_contrasena)
btn_generar.pack(pady=5)
btn_mostrar = tk.Button(menu_contrasenas, text="Mostrar contraseñas guardadas", width=30, command=mostrar_contrasenas)
#// opcion para eliminar las contraseña
btn_delete = tk.Button(menu_contrasenas, text="Eliminar contraseña", width=30, command=eliminar_contrasena)
btn_delete.pack(pady=5)
btn_mostrar.pack(pady=5)
btn_volver = tk.Button(menu_contrasenas, text="Volver", width=30, command=volver_menu_principal)
btn_volver.pack(pady=10)
#Fecha y hora :v
label_fecha_hora = tk.Label(root, font=("Arial", 10))
label_fecha_hora.place(relx=1.0, y=0, anchor="ne")
actualizar_fecha_hora()

root.mainloop()