#!/usr/bin/env python3
import cv2
import time
import os
import json
import paramiko
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk

# === Autenticación previa tipo hacker ===
def autenticacion_previa():
    auth_window = tk.Tk()
    auth_window.title("🔐 Autenticación Hackercracks")
    auth_window.configure(bg="black")
    auth_window.geometry("500x250")

    tk.Label(auth_window, text="💀 HACKERCRACKS", fg="#00FF00", bg="black", font=("Courier New", 24)).pack(pady=10)
    tk.Label(auth_window, text="Autenticación requerida", fg="#00FF00", bg="black", font=("Courier New", 12)).pack(pady=5)

    tk.Label(auth_window, text="Código de Acceso:", fg="#00FF00", bg="black").pack()
    clave_entry = tk.Entry(auth_window, show="*", font=("Courier New", 10), bg="#1a1a1a", fg="#00FF00")
    clave_entry.pack(pady=5)

    progreso_label = tk.Label(auth_window, text="", fg="#00FF00", bg="black")
    progreso_label.pack()

    def validar():
        clave = clave_entry.get()
        if clave == "Password=1=1":
            progreso_label.config(text="✅ Verificando identidad...")
            auth_window.update()
            time.sleep(1)

            for i in range(3):
                progreso_label.config(text=f"🔄 Cargando sistema... {'.' * (i+1)}")
                auth_window.update()
                time.sleep(0.5)

            progreso_label.config(text="📸 Activando cámara...")
            auth_window.update()
            time.sleep(1)

            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            if ret:
                cv2.imwrite("foto_usuario.jpg", frame)
            cam.release()

            auth_window.destroy()
        else:
            messagebox.showerror("Acceso denegado", "❌ Código incorrecto.")

    tk.Button(auth_window, text="Ingresar", command=validar, bg="#111111", fg="#00FF00").pack(pady=10)
    auth_window.mainloop()

# Ejecutar antes de mostrar la ventana principal
autenticacion_previa()

# === Archivo de conexiones guardadas ===
CONEXIONES_FILE = "conexiones.json"

def cargar_conexiones():
    if os.path.exists(CONEXIONES_FILE):
        with open(CONEXIONES_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_conexiones(data):
    with open(CONEXIONES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def seleccionar_archivo():
    path = filedialog.askopenfilename()
    if path:
        entrada_origen.delete(0, tk.END)
        entrada_origen.insert(0, path)

def seleccionar_carpeta():
    path = filedialog.askdirectory()
    if path:
        entrada_origen.delete(0, tk.END)
        entrada_origen.insert(0, path)

def validar_campos():
    return all([
        entrada_origen.get(),
        entrada_usuario.get(),
        entrada_contra.get(),
        entrada_ip.get(),
        entrada_ruta.get()
    ])

def actualizar_progreso(transmitido, total):
    porcentaje = int((transmitido / total) * 100)
    barra_progreso["value"] = porcentaje
    ventana.update_idletasks()

def transferir():
    if not validar_campos():
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    archivo_local = entrada_origen.get()
    usuario = entrada_usuario.get()
    contrasena = entrada_contra.get()
    ip = entrada_ip.get()
    ruta_destino = entrada_ruta.get()
    puerto = int(entrada_puerto.get()) if entrada_puerto.get() else 22

    try:
        barra_progreso["value"] = 0
        client = paramiko.Transport((ip, puerto))
        client.connect(username=usuario, password=contrasena)
        sftp = paramiko.SFTPClient.from_transport(client)

        archivo_remoto = os.path.join(ruta_destino, os.path.basename(archivo_local))
        filesize = os.path.getsize(archivo_local)

        with open(archivo_local, 'rb') as f:
            sftp.putfo(f, archivo_remoto, callback=lambda x, y: actualizar_progreso(x, filesize))

        sftp.close()
        client.close()

        messagebox.showinfo("Éxito", "✅ Transferencia completada con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Error en la transferencia:\n{str(e)}")

def ejecutar_transferencia():
    threading.Thread(target=transferir).start()

def guardar_conexion():
    conexiones = cargar_conexiones()
    nombre = combo_guardado.get()

    if not nombre:
        messagebox.showwarning("Advertencia", "Debes asignar un nombre a la conexión.")
        return

    conexiones[nombre] = {
        "usuario": entrada_usuario.get(),
        "ip": entrada_ip.get(),
        "puerto": entrada_puerto.get(),
        "ruta": entrada_ruta.get()
    }

    if var_recordar_contra.get():
        conexiones[nombre]["contrasena"] = entrada_contra.get()

    guardar_conexiones(conexiones)
    actualizar_combo()
    messagebox.showinfo("Guardado", "🔐 Conexión guardada exitosamente.")

def usar_conexion():
    nombre = combo_guardado.get()
    conexiones = cargar_conexiones()

    if nombre in conexiones:
        datos = conexiones[nombre]
        entrada_usuario.delete(0, tk.END)
        entrada_usuario.insert(0, datos["usuario"])
        entrada_ip.delete(0, tk.END)
        entrada_ip.insert(0, datos["ip"])
        entrada_puerto.delete(0, tk.END)
        entrada_puerto.insert(0, datos["puerto"])
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, datos["ruta"])

        if "contrasena" in datos:
            entrada_contra.delete(0, tk.END)
            entrada_contra.insert(0, datos["contrasena"])
            var_recordar_contra.set(True)
        else:
            entrada_contra.delete(0, tk.END)
            var_recordar_contra.set(False)
    else:
        messagebox.showwarning("Advertencia", "Conexión no encontrada.")

def eliminar_conexion():
    nombre = combo_guardado.get()
    conexiones = cargar_conexiones()

    if nombre in conexiones:
        if messagebox.askyesno("Confirmar", f"¿Eliminar la conexión '{nombre}'?"):
            conexiones.pop(nombre)
            guardar_conexiones(conexiones)
            actualizar_combo()
            messagebox.showinfo("Eliminado", "Conexión eliminada.")
    else:
        messagebox.showerror("Error", "Conexión no encontrada.")

def actualizar_combo():
    combo_guardado["values"] = list(cargar_conexiones().keys())

# === Interfaz gráfica tipo hacker ===
ventana = ThemedTk(theme="arc")
ventana.title("🧠 Hackercracks - SCP MIGRATE")
ventana.geometry("750x500")
ventana.configure(bg="black")

var_recordar_contra = tk.BooleanVar()

# Estilo hacker
fuente = ("Courier New", 10)
color_texto = "#00FF00"
color_entrada = "#1a1a1a"

ventana.option_add("*Foreground", color_texto)
ventana.option_add("*Background", "black")
ventana.option_add("*Entry.Background", color_entrada)
ventana.option_add("*Entry.Foreground", color_texto)
ventana.option_add("*Button.Background", "#111111")
ventana.option_add("*Button.Foreground", color_texto)
ventana.option_add("*Label.Foreground", color_texto)
ventana.option_add("*Font", fuente)

style = ttk.Style(ventana)
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=color_entrada, foreground=color_texto, background="black")
style.configure("TProgressbar", foreground=color_texto, background=color_texto)

# Widgets
tk.Label(ventana, text="📁 Archivo/Carpeta Origen:").grid(row=0, column=0, sticky="e")
entrada_origen = tk.Entry(ventana, width=50)
entrada_origen.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
tk.Button(ventana, text="Archivo", command=seleccionar_archivo).grid(row=0, column=3)
tk.Button(ventana, text="Carpeta", command=seleccionar_carpeta).grid(row=0, column=4)

tk.Label(ventana, text="👤 Usuario Remoto:").grid(row=1, column=0, sticky="e")
entrada_usuario = tk.Entry(ventana)
entrada_usuario.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

tk.Label(ventana, text="🔐 Contraseña:").grid(row=2, column=0, sticky="e")
entrada_contra = tk.Entry(ventana, show="*")
entrada_contra.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
tk.Checkbutton(ventana, text="🔒 Recordar contraseña", variable=var_recordar_contra, bg="black", fg=color_texto, selectcolor="black", font=fuente).grid(row=2, column=3, columnspan=2)

tk.Label(ventana, text="🌐 IP o Dominio:").grid(row=3, column=0, sticky="e")
entrada_ip = tk.Entry(ventana)
entrada_ip.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

tk.Label(ventana, text="📂 Ruta Remota:").grid(row=4, column=0, sticky="e")
entrada_ruta = tk.Entry(ventana)
entrada_ruta.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

tk.Label(ventana, text="🔌 Puerto SSH (default 22):").grid(row=5, column=0, sticky="e")
entrada_puerto = tk.Entry(ventana)
entrada_puerto.grid(row=5, column=1, padx=5, pady=5)

tk.Label(ventana, text="💾 Conexión guardada:").grid(row=6, column=0, sticky="e")
combo_guardado = ttk.Combobox(ventana)
combo_guardado.grid(row=6, column=1, padx=5, pady=5)
tk.Button(ventana, text="Usar", command=usar_conexion).grid(row=6, column=2)
tk.Button(ventana, text="Guardar", command=guardar_conexion).grid(row=6, column=3)
tk.Button(ventana, text="Eliminar", command=eliminar_conexion).grid(row=6, column=4)

barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=500, mode="determinate")
barra_progreso.grid(row=7, column=0, columnspan=5, padx=10, pady=20)

tk.Button(ventana, text="🚀 Iniciar Transferencia", bg="#111111", fg=color_texto, command=ejecutar_transferencia).grid(row=8, column=0, columnspan=5, pady=10)

actualizar_combo()
ventana.mainloop()
