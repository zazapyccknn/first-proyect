import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import json
import os
import datetime
import tkinter.filedialog as filedialog

ARCHIVO_CONTRASENAS = "contrasenas.json"  # odio saber que la "ñ" no funciona :(

# =========================
# Gestor de Contraseñas
# =========================

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

def eliminar_contrasena():
    contrasenas = cargar_contrasenas()
    if not contrasenas:
        messagebox.showinfo("Eliminar contraseña", "No hay contraseñas guardadas.")
        return
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

def mostrar_menu_contrasenas():
    menu_principal.pack_forget()
    menu_contrasenas.pack(pady=20)

def volver_menu_principal():
    menu_contrasenas.pack_forget()
    menu_principal.pack(pady=20)

# =========================
# Libreta de Notas
# =========================

def open_libreta():
    ventana_de_libreta = tk.Toplevel(root)
    ventana_de_libreta.title("---- APUNTES ----")
    ventana_de_libreta.geometry("600x600")

    txt_libreta = tk.Text(ventana_de_libreta, wrap=tk.WORD, font=("Arial", 15))
    txt_libreta.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def save_libreta():
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "w") as f:
                f.write(txt_libreta.get("1.0", tk.END))
            messagebox.showinfo("Guardado", "Apuntes guardados correctamente.")

    def load_libreta():
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "r") as f:
                txt_libreta.delete("1.0", tk.END)
                txt_libreta.insert(tk.END, f.read())
            messagebox.showinfo("Cargado", "Apuntes cargados correctamente.")

    btn_guardar = tk.Button(ventana_de_libreta, text="Guardar", command=save_libreta)
    btn_guardar.pack(side="left", padx=10, pady=5)

    btn_cargar = tk.Button(ventana_de_libreta, text="Cargar", command=load_libreta)
    btn_cargar.pack(side="left", padx=10, pady=5)

# =========================
# Fecha y Hora
# =========================

def actualizar_fecha_hora():
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_fecha_hora.config(text=ahora)
    label_fecha_hora.after(1000, actualizar_fecha_hora)

# =========================
# Interfaz Principal
# =========================

root = tk.Tk()
root.title("BeccaTool - Herramientas")

# Menú principal
menu_principal = tk.Frame(root)
label_menu = tk.Label(menu_principal, text="Selecciona una herramienta:", font=("Arial", 14))
label_menu.pack(pady=10)
btn_contrasenas = tk.Button(menu_principal, text="Contraseñas", width=25, command=mostrar_menu_contrasenas)
btn_contrasenas.pack(pady=5)
btn_libreta = tk.Button(menu_principal, text="Libreta de Notas", width=25, command=open_libreta)
btn_libreta.pack(pady=5)
menu_principal.pack(pady=20)

# Menú de contraseñas
menu_contrasenas = tk.Frame(root)
label_contra = tk.Label(menu_contrasenas, text="Gestor de Contraseñas", font=("Arial", 12))
label_contra.pack(pady=10)
btn_generar = tk.Button(menu_contrasenas, text="Generar y guardar contraseña", width=30, command=agregar_contrasena)
btn_generar.pack(pady=5)
btn_mostrar = tk.Button(menu_contrasenas, text="Mostrar contraseñas guardadas", width=30, command=mostrar_contrasenas)
btn_mostrar.pack(pady=5)
btn_delete = tk.Button(menu_contrasenas, text="Eliminar contraseña", width=30, command=eliminar_contrasena)
btn_delete.pack(pady=5)
btn_volver = tk.Button(menu_contrasenas, text="Volver", width=30, command=volver_menu_principal)
btn_volver.pack(pady=10)

# Fecha y hora (siempre visible, arriba a la derecha)
label_fecha_hora = tk.Label(root, font=("Arial", 10))
label_fecha_hora.place(relx=1.0, y=0, anchor="ne")
actualizar_fecha_hora()

#no borrar, se va todo a la shit
root.mainloop()