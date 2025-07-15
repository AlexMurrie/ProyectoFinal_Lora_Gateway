import requests
import tkinter as tk
from tkinter import ttk, messagebox

# === Obtener datos del servidor ===
def obtener_datos():
    url = 'https://bbl-net.com.ar/api_utilities/Prueba_SRV.php'
    data = {
        'user': 'admin',
        'password': 'admin',
        'comando': 'descargar'
    }

    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            jsonResponse = response.json()
            if jsonResponse['estado'] == 'ok' and jsonResponse['comando'] == 'descargar':
                return jsonResponse['respuesta']
            else:
                messagebox.showerror("Error", "Comando fallido o datos no encontrados.")
        else:
            messagebox.showerror("Error", f"Error en la solicitud: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Excepción", f"Ocurrió un error: {e}")
    return []

# === Mostrar los datos en el Listbox ===
def mostrar_datos(datos):
    listbox.delete(0, tk.END)
    for i, dato in enumerate(datos, start=1):
        item = f"{i}. Fecha: {dato['date']}, Datos: {dato['datos']}"
        listbox.insert(tk.END, item)

# === Buscar en los datos ===
def buscar():
    filtro = entry_buscar.get().lower()
    resultados = [d for d in datos_totales if filtro in d['date'].lower() or filtro in d['datos'].lower()]
    mostrar_datos(resultados)

# === Refrescar datos desde el servidor ===
def refrescar():
    global datos_totales
    datos_totales = obtener_datos()
    entry_buscar.delete(0, tk.END)  # limpiar búsqueda
    mostrar_datos(datos_totales)

# === Interfaz gráfica ===
root = tk.Tk()
root.title("Datos SRV")

# Frame superior: búsqueda + botón refresh
frame_superior = ttk.Frame(root)
frame_superior.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(frame_superior, text="Buscar:").pack(side=tk.LEFT)
entry_buscar = ttk.Entry(frame_superior)
entry_buscar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
ttk.Button(frame_superior, text="Buscar", command=buscar).pack(side=tk.LEFT, padx=5)
ttk.Button(frame_superior, text="Actualizar", command=refrescar).pack(side=tk.LEFT)

# Frame central: lista con scroll
frame_lista = ttk.Frame(root)
frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, font=("Courier", 10))
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)

# Cargar datos al inicio
datos_totales = obtener_datos()
mostrar_datos(datos_totales)

root.mainloop()
