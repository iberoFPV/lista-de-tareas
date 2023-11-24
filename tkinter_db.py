from tkinter import *
import sqlite3

# Función para eliminar una tarea por su ID
def remove(id):
    def _remove():
        with conn:
            c.execute("DELETE FROM todo WHERE ID = ?", (id, ))
        render_todos()
    return _remove

# Función para marcar una tarea como completada o pendiente por su ID
def complete(id):
    def _complete():
        todo = c.execute("SELECT * from todo WHERE id = ?", (id, )).fetchone()
        with conn:
            c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        render_todos()
    return _complete

# Función para renderizar las tareas en la interfaz gráfica
def render_todos():
    rows = c.execute("SELECT * FROM todo").fetchall()

    # Limpiar el marco antes de renderizar las tareas nuevamente
    for widget in frame.winfo_children():
        widget.destroy()

    # Iterar sobre las tareas y agregar Checkbuttons y botones de eliminar
    for i, row in enumerate(rows):
        id, _, description, completed = row
        color_bg = '#27AE60' if completed else '#FF6347'  # Fondo verde para tareas completadas, rojo para tareas pendientes
        color_fg = '#333333' if completed else '#FFFFFF'  # Texto gris oscuro para tareas completadas, blanco para tareas pendientes

        # Crear un Checkbutton para cada tarea
        l = Checkbutton(frame, text=description, fg=color_fg, bg=color_bg, width=42, anchor='w', command=complete(id), selectcolor=color_bg)
        l.grid(row=i, column=0, sticky='w')

        # Crear un botón para eliminar cada tarea
        btn = Button(frame, text='Eliminar', command=remove(id), bg='#F0F0F0', fg='#262626')
        btn.grid(row=i, column=1)

        # Seleccionar el Checkbutton si la tarea está completada, deseleccionar si no lo está
        l.select() if completed else l.deselect()

# Función para agregar una nueva tarea
def add_todo():
    todo = e.get()
    if todo:
        with conn:
            c.executemany("INSERT INTO todo (description, completed) VALUES (?, ?)", [(todo, False)])
        e.delete(0, END)
        render_todos()

# Crear la ventana principal
root = Tk()
root.title('Lista de tareas')
root.geometry('500x500')
root.configure(bg='#262626')  # Fondo oscuro

# Conectar a la base de datos SQLite y crear la tabla si no existe
conn = sqlite3.connect('todo.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")
conn.commit()

# Crear etiquetas, entrada de texto y botones en la interfaz gráfica
l = Label(root, text='Tarea', bg='#262626', fg='#FFFFFF')  # Fondo oscuro, texto blanco
l.grid(row=0, column=0)

e = Entry(root, width=40, bg='#F0F0F0', fg='#333333')  # Fondo gris claro, texto gris oscuro
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=add_todo, bg='#27AE60', fg='#262626')  # Fondo verde, texto blanco
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis tareas', padx=5, pady=5, bg='#333333', fg='#FFFFFF')  # Fondo gris oscuro, texto blanco
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

e.focus()

# Asignar eventos de teclado
root.bind('<Return>', lambda x: add_todo())

# Iniciar el bucle principal de la aplicación
root.mainloop()

