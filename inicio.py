import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Lista de asignaturas de Ingeniería en Sistemas de Información - Plan de Estudios Completo
# "cursadas" = materias que deben estar cursadas (no necesariamente aprobadas)
# "aprobadas" = materias que deben estar aprobadas obligatoriamente
INITIAL_TASKS = [
    # NIVEL I - Primer Año
    {"id": 1, "description": "Análisis Matemático I", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 2, "description": "Álgebra y Geometría Analítica", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 3, "description": "Física I", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 4, "description": "Inglés I", "level": 1, "cursadas": [], "aprobadas": [], "c": 4, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 5, "description": "Lógica y Estructuras Discretas", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 3, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 6, "description": "Algoritmos y Estructuras de Datos", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 10, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 7, "description": "Arquitectura de Computadoras", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 4, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 8, "description": "Sistemas y Procesos de Negocio", "level": 1, "cursadas": [], "aprobadas": [], "c": "-", "a": 3, "status": "none", "created_at": "2023-01-01 00:00:00"},
    
    # NIVEL II - Segundo Año
    {"id": 9, "description": "Análisis Matemático II", "level": 2, "cursadas": [1, 2], "aprobadas": [], "c": "-", "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 10, "description": "Física II", "level": 2, "cursadas": [1, 3], "aprobadas": [], "c": 10, "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 11, "description": "Ingeniería y Sociedad", "level": 2, "cursadas": [], "aprobadas": [], "c": "-", "a": 3, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 12, "description": "Inglés II", "level": 2, "cursadas": [4], "aprobadas": [], "c": 4, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 13, "description": "Sintaxis y Semántica de los Lenguajes", "level": 2, "cursadas": [5, 6], "aprobadas": [], "c": "-", "a": 4, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 14, "description": "Paradigmas de Programación", "level": 2, "cursadas": [5, 6], "aprobadas": [], "c": "-", "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 15, "description": "Sistemas Operativos", "level": 2, "cursadas": [7], "aprobadas": [], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 16, "description": "Análisis de Sistemas de Información (Integradora)", "level": 2, "cursadas": [6, 8], "aprobadas": [], "c": "-", "a": 5, "status": "none", "created_at": "2023-01-01 00:00:00"},
    
    # NIVEL III - Tercer Año
    {"id": 17, "description": "Probabilidad y Estadística", "level": 3, "cursadas": [1, 2], "aprobadas": [], "c": "-", "a": 3, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 18, "description": "Economía", "level": 3, "cursadas": [], "aprobadas": [1, 2], "c": 6, "a": 3, "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 19, "description": "Bases de Datos", "level": 3, "cursadas": [13, 16], "aprobadas": [5, 6], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 20, "description": "Desarrollo de Software", "level": 3, "cursadas": [14, 16], "aprobadas": [5, 6], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 21, "description": "Comunicación de Datos", "level": 3, "cursadas": [], "aprobadas": [3, 7], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 22, "description": "Análisis Numérico", "level": 3, "cursadas": [9], "aprobadas": [1, 2], "c": 6, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 23, "description": "Diseño de Sistemas de Información (Integradora)", "level": 3, "cursadas": [14, 16], "aprobadas": [4, 6, 8], "c": "-", "a": 6, "status": "none", "created_at": "2023-01-01 00:00:00"},
    
    # NIVEL IV - Cuarto Año
    {"id": 24, "description": "Legislación", "level": 4, "cursadas": [11], "aprobadas": [], "c": 4, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 25, "description": "Ingeniería y Calidad de Software", "level": 4, "cursadas": [19, 20, 23], "aprobadas": [13, 14], "c": 6, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 26, "description": "Redes de Datos", "level": 4, "cursadas": [15, 21], "aprobadas": [], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 27, "description": "Investigación Operativa", "level": 4, "cursadas": [17, 22], "aprobadas": [], "c": 10, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 28, "description": "Simulación", "level": 4, "cursadas": [17], "aprobadas": [9], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 29, "description": "Tecnologías para la Automatización", "level": 4, "cursadas": [10, 22], "aprobadas": [9], "c": 6, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 30, "description": "Administración de Sistemas de Información (Integradora)", "level": 4, "cursadas": [18, 23], "aprobadas": [16], "c": "-", "a": 6, "status": "none", "created_at": "2023-01-01 00:00:00"},
    
    # NIVEL V - Quinto Año
    {"id": 31, "description": "Inteligencia Artificial", "level": 5, "cursadas": [28], "aprobadas": [17, 22], "c": 6, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 32, "description": "Ciencia de Datos", "level": 5, "cursadas": [28], "aprobadas": [17, 19], "c": 3, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 33, "description": "Sistemas de Gestión", "level": 5, "cursadas": [18, 27], "aprobadas": [23], "c": 8, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 34, "description": "Gestión Gerencial", "level": 5, "cursadas": [24, 30], "aprobadas": [18], "c": 6, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 35, "description": "Seguridad en los Sistemas de Información", "level": 5, "cursadas": [26, 30], "aprobadas": [20, 21], "c": 3, "a": "-", "status": "none", "created_at": "2023-01-01 00:00:00"},
    {"id": 36, "description": "Proyecto Final (Integradora)", "level": 5, "cursadas": [25, 26, 30], "aprobadas": [12, 20, 23], "c": "-", "a": 6, "status": "none", "created_at": "2023-01-01 00:00:00"},
]

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Asignaturas")
        self.root.geometry("800x600")
        self.filename = "tasks.json"
        self.tasks = self.load_tasks()

        # Estilo para la interfaz
        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Arial", 10))
        
        # Configurar estilos personalizados para botones con colores completos
        style.configure("Cursada.TButton", 
                       padding=6, 
                       font=("Arial", 10, "bold"), 
                       background="#FFD700", 
                       foreground="black",
                       relief="flat",
                       borderwidth=0,
                       highlightthickness=0,
                       focuscolor="none")
        style.map("Cursada.TButton",
                 background=[('active', '#E6C200'), ('pressed', '#CCAD00')])
        
        style.configure("Aprobada.TButton", 
                       padding=6, 
                       font=("Arial", 10, "bold"), 
                       background="#90EE90", 
                       foreground="black",
                       relief="flat",
                       borderwidth=0)
        style.map("Aprobada.TButton",
                 background=[('active', '#7FDD7F'), ('pressed', '#6ECC6E')])
        
        style.configure("EnCurso.TButton", 
                       padding=6, 
                       font=("Arial", 10, "bold"), 
                       background="#FF8C00", 
                       foreground="black",
                       relief="flat",
                       borderwidth=0)
        style.map("EnCurso.TButton",
                 background=[('active', '#E67E00'), ('pressed', '#CC7000')])
        
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Frame principal
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        # Frame para entrada
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill="x", pady=5)

        tk.Label(self.input_frame, text="Descripción:", font=("Arial", 10)).pack(side="left")
        self.task_entry = tk.Entry(self.input_frame, font=("Arial", 10))
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5)

        tk.Label(self.input_frame, text="Nivel (1, 2, etc.):", font=("Arial", 10)).pack(side="left")
        self.level_entry = tk.Entry(self.input_frame, width=5, font=("Arial", 10))
        self.level_entry.pack(side="left", padx=5)

        # Frame para botones
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=5)

        self.add_button = ttk.Button(self.button_frame, text="Nueva Materia", command=self.add_task, style="TButton")
        self.add_button.pack(side="left", padx=5, fill="x", expand=True)

        self.cursada_button = ttk.Button(self.button_frame, text="Cursada", command=self.mark_cursada, style="Cursada.TButton")
        self.cursada_button.pack(side="left", padx=5, fill="x", expand=True)

        self.complete_button = ttk.Button(self.button_frame, text="Aprobada", command=self.complete_task, style="Aprobada.TButton")
        self.complete_button.pack(side="left", padx=5, fill="x", expand=True)

        self.en_curso_button = ttk.Button(self.button_frame, text="En Curso", command=self.mark_en_curso, style="EnCurso.TButton")
        self.en_curso_button.pack(side="left", padx=5, fill="x", expand=True)

        self.clear_button = ttk.Button(self.button_frame, text="Limpiar", command=self.clear_task, style="TButton")
        self.clear_button.pack(side="left", padx=5, fill="x", expand=True)

        self.delete_button = ttk.Button(self.button_frame, text="Eliminar Materia", command=self.delete_task, style="TButton")
        self.delete_button.pack(side="left", padx=5, fill="x", expand=True)

        # Treeview para mostrar tareas
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Descripción", "Cursadas", "Aprobadas", "C", "A"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Asignatura")
        self.tree.heading("Cursadas", text="Cursadas")
        self.tree.heading("Aprobadas", text="Aprobadas")
        self.tree.heading("C", text="C")
        self.tree.heading("A", text="A")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Descripción", width=350, anchor="w")
        self.tree.column("Cursadas", width=80, anchor="center")
        self.tree.column("Aprobadas", width=80, anchor="center")
        self.tree.column("C", width=40, anchor="center")
        self.tree.column("A", width=40, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Configurar colores para las filas
        self.tree.tag_configure("none", background="lightgrey", foreground="black")
        self.tree.tag_configure("cursada", background="#FFD700", foreground="black")  # Amarillo dorado como en la imagen
        self.tree.tag_configure("completada", background="#90EE90", foreground="black")  # Verde claro como en la imagen
        self.tree.tag_configure("en_curso", background="#FF8C00", foreground="black")  # Naranja notorio para en curso
        self.tree.tag_configure("disponible", background="plum", foreground="black")  # Violeta original restaurado
        self.tree.tag_configure("level_header", background="darkblue", foreground="white", font=("Arial", 11, "bold"))

        self.update_task_treeview()

    def is_task_available(self, task):
        """Determina si una materia está disponible para cursar basándose en las correlativas"""
        # Si la materia ya está cursada, en curso o completada, no está disponible para cursar
        if task['status'] in ["cursada", "en_curso", "completada"]:
            return False
        
        # Verificar correlativas para cursar (deben estar cursadas o completadas)
        for cursada_id in task['cursadas']:
            if not any(t['id'] == cursada_id and t['status'] in ["cursada", "en_curso", "completada"] for t in self.tasks):
                return False
        
        # Verificar correlativas que deben estar aprobadas (deben estar completadas)
        for aprobada_id in task['aprobadas']:
            if not any(t['id'] == aprobada_id and t['status'] == "completada" for t in self.tasks):
                return False
        
        return True

    def load_tasks(self):
        # Intentar cargar desde el archivo JSON si existe, sino usar la lista inicial
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    loaded_tasks = json.load(file)
                    # Asegurar que todas las tareas tengan los campos C y A
                    for task in loaded_tasks:
                        if 'c' not in task:
                            task['c'] = '-'
                        if 'a' not in task:
                            task['a'] = '-'
                        
                        # Aplicar valores específicos para Nivel I
                        if task['id'] == 1:
                            task['c'] = '-'
                            task['a'] = 5
                        elif task['id'] == 2:
                            task['c'] = '-'
                            task['a'] = 5
                        elif task['id'] == 3:
                            task['c'] = '-'
                            task['a'] = 5
                        elif task['id'] == 4:
                            task['c'] = 4
                            task['a'] = '-'
                        elif task['id'] == 5:
                            task['c'] = '-'
                            task['a'] = 3
                        elif task['id'] == 6:
                            task['c'] = '-'
                            task['a'] = 10
                        elif task['id'] == 7:
                            task['c'] = '-'
                            task['a'] = 4
                        elif task['id'] == 8:
                            task['c'] = '-'
                            task['a'] = 3
                        # Aplicar valores específicos para Nivel II
                        elif task['id'] == 9:
                            task['c'] = '-'
                            task['a'] = 5
                        elif task['id'] == 10:
                            task['c'] = 10
                            task['a'] = 5
                        elif task['id'] == 11:
                            task['c'] = '-'
                            task['a'] = 3
                        elif task['id'] == 12:
                            task['c'] = 4
                            task['a'] = '-'
                        elif task['id'] == 13:
                            task['c'] = '-'
                            task['a'] = 4
                        elif task['id'] == 14:
                            task['c'] = '-'
                            task['a'] = 5
                        elif task['id'] == 15:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 16:
                            task['c'] = '-'
                            task['a'] = 5
                        # Aplicar valores específicos para Nivel III
                        elif task['id'] == 17:
                            task['c'] = '-'
                            task['a'] = 3
                        elif task['id'] == 18:
                            task['c'] = 6
                            task['a'] = 3
                        elif task['id'] == 19:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 20:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 21:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 22:
                            task['c'] = 6
                            task['a'] = '-'
                        elif task['id'] == 23:
                            task['c'] = '-'
                            task['a'] = 6
                        # Aplicar valores específicos para Nivel IV
                        elif task['id'] == 24:
                            task['c'] = 4
                            task['a'] = '-'
                        elif task['id'] == 25:
                            task['c'] = 6
                            task['a'] = '-'
                        elif task['id'] == 26:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 27:
                            task['c'] = 10
                            task['a'] = '-'
                        elif task['id'] == 28:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 29:
                            task['c'] = 6
                            task['a'] = '-'
                        elif task['id'] == 30:
                            task['c'] = '-'
                            task['a'] = 6
                        # Aplicar valores específicos para Nivel V
                        elif task['id'] == 31:
                            task['c'] = 6
                            task['a'] = '-'
                        elif task['id'] == 32:
                            task['c'] = 3
                            task['a'] = '-'
                        elif task['id'] == 33:
                            task['c'] = 8
                            task['a'] = '-'
                        elif task['id'] == 34:
                            task['c'] = 6
                            task['a'] = '-'
                        elif task['id'] == 35:
                            task['c'] = 3
                            task['a'] = '-'
                        elif task['id'] == 36:
                            task['c'] = '-'
                            task['a'] = 6
                    
                    return loaded_tasks
            except (json.JSONDecodeError, FileNotFoundError):
                # Si hay error en el archivo, usar la lista inicial
                return INITIAL_TASKS.copy()
        else:
            # Si no existe el archivo, usar la lista inicial
            return INITIAL_TASKS.copy()

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)
        self.update_task_treeview()

    def add_task(self):
        description = self.task_entry.get().strip()
        level = self.level_entry.get().strip()

        if not description:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una descripción para la tarea.")
            return
        if not level.isdigit() or int(level) < 1:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nivel válido (1, 2, etc.).")
            return

        # Generar nuevo ID empezando desde 101
        existing_ids = [task['id'] for task in self.tasks]
        new_id = 101
        while new_id in existing_ids:
            new_id += 1

        task = {
            'id': new_id,  # Las nuevas tareas tendrán IDs empezando desde 101
            'description': description,
            'level': int(level),
            'cursadas': [],
            'aprobadas': [],
            'c': 3,  # Campo C con valor por defecto 3
            'a': "-",  # Campo A con valor por defecto "-"
            'status': "none",
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.level_entry.delete(0, tk.END)
        messagebox.showinfo("Éxito", f"Tarea '{description}' (ID: {new_id}, Nivel {level}) agregada.")

    def mark_cursada(self):
        try:
            selected_item = self.tree.selection()[0]
            # Obtener el ID de la tarea seleccionada, asegurándose de que no sea un encabezado de nivel
            item_values = self.tree.item(selected_item)["values"]
            if not item_values or "NIVEL" in str(item_values[1]) or not str(item_values[0]).isdigit():
                messagebox.showwarning("Advertencia", "Selecciona una asignatura válida, no un encabezado de nivel.")
                return

            task_id = int(item_values[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    if task['status'] == "completada":
                        messagebox.showwarning("Advertencia", "No se puede marcar como cursada una asignatura ya completada.")
                        return
                    task['status'] = "cursada"
                    self.save_tasks()
                    messagebox.showinfo("Éxito", f"Asignatura '{task['description']}' marcada como cursada.")
                    return
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una asignatura para marcar como cursada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo marcar la asignatura: {e}")

    def mark_en_curso(self):
        try:
            selected_item = self.tree.selection()[0]
            # Obtener el ID de la tarea seleccionada, asegurándose de que no sea un encabezado de nivel
            item_values = self.tree.item(selected_item)["values"]
            if not item_values or "NIVEL" in str(item_values[1]) or not str(item_values[0]).isdigit():
                messagebox.showwarning("Advertencia", "Selecciona una asignatura válida, no un encabezado de nivel.")
                return

            task_id = int(item_values[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    if task['status'] == "completada":
                        messagebox.showwarning("Advertencia", "No se puede marcar como en curso una asignatura ya completada.")
                        return
                    task['status'] = "en_curso"
                    self.save_tasks()
                    messagebox.showinfo("Éxito", f"Asignatura '{task['description']}' marcada como en curso.")
                    return
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una asignatura para marcar como en curso.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo marcar la asignatura: {e}")

    def complete_task(self):
        try:
            selected_item = self.tree.selection()[0]
            # Obtener el ID de la tarea seleccionada, asegurándose de que no sea un encabezado de nivel
            item_values = self.tree.item(selected_item)["values"]
            if not item_values or "NIVEL" in str(item_values[1]) or not str(item_values[0]).isdigit():
                messagebox.showwarning("Advertencia", "Selecciona una asignatura válida, no un encabezado de nivel.")
                return

            task_id = int(item_values[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    missing_cursadas = [c for c in task['cursadas'] if not any(t['id'] == c and t['status'] in ["cursada", "en_curso", "completada"] for t in self.tasks)]
                    missing_aprobadas = [a for a in task['aprobadas'] if not any(t['id'] == a and t['status'] == "completada" for t in self.tasks)]
                    if missing_cursadas or missing_aprobadas:
                        # Convertir los IDs a descripciones para una mejor visualización en el mensaje de error
                        missing_cursadas_desc = [t['description'] for t in self.tasks if t['id'] in missing_cursadas]
                        missing_aprobadas_desc = [t['description'] for t in self.tasks if t['id'] in missing_aprobadas]
                        error_msg = f"No se puede completar '{task['description']}'.\n\nFaltan correlativas:"
                        if missing_cursadas_desc:
                            error_msg += f"\n• Para cursar: {', '.join(missing_cursadas_desc)}"
                        if missing_aprobadas_desc:
                            error_msg += f"\n• Para aprobar: {', '.join(missing_aprobadas_desc)}"
                        messagebox.showwarning("Correlativas Faltantes", error_msg)
                        return
                    task['status'] = "completada"
                    self.save_tasks()
                    messagebox.showinfo("Éxito", f"¡Felicitaciones! Asignatura '{task['description']}' completada.")
                    return
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una asignatura para completar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la asignatura: {e}")

    def clear_task(self):
        try:
            selected_item = self.tree.selection()[0]
            # Obtener el ID de la tarea seleccionada, asegurándose de que no sea un encabezado de nivel
            item_values = self.tree.item(selected_item)["values"]
            if not item_values or "NIVEL" in str(item_values[1]) or not str(item_values[0]).isdigit():
                messagebox.showwarning("Advertencia", "Selecciona una asignatura válida, no un encabezado de nivel.")
                return

            task_id = int(item_values[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    task['status'] = "none"
                    self.save_tasks()
                    messagebox.showinfo("Éxito", f"Asignatura '{task['description']}' limpiada (estado por defecto).")
                    return
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una asignatura para limpiar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo limpiar la asignatura: {e}")

    def delete_task(self):
        try:
            selected_item = self.tree.selection()[0]
            # Obtener el ID de la tarea seleccionada, asegurándose de que no sea un encabezado de nivel
            item_values = self.tree.item(selected_item)["values"]
            if not item_values or "NIVEL" in str(item_values[1]) or not str(item_values[0]).isdigit():
                messagebox.showwarning("Advertencia", "Selecciona una asignatura válida, no un encabezado de nivel.")
                return

            task_id = int(item_values[0])
            
            # No permitir eliminar las materias originales (ID 1-36)
            if 1 <= task_id <= 36:
                messagebox.showwarning("Advertencia", "No se pueden eliminar las materias del plan de estudios original.\n\nUsa el botón 'Limpiar' para resetear su estado si es necesario.")
                return
            
            for task in self.tasks:
                if task['id'] == task_id:
                    dependent_tasks = [t for t in self.tasks if task_id in t['cursadas'] or task_id in t['aprobadas']]
                    if dependent_tasks:
                        dependent_names = [t['description'] for t in dependent_tasks]
                        messagebox.showwarning("Advertencia", f"No se puede eliminar '{task['description']}'.\n\nEs correlativa de:\n• {chr(10).join(dependent_names)}")
                        return
                    
                    # Confirmar eliminación
                    if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar '{task['description']}'?"):
                        self.tasks.remove(task)
                        self.save_tasks()
                        messagebox.showinfo("Éxito", f"Asignatura '{task['description']}' eliminada.")
                    return
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una asignatura para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la asignatura: {e}")

    def update_task_treeview(self):
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ordenar las tareas por nivel y luego por ID
        sorted_tasks = sorted(self.tasks, key=lambda t: (t['level'], t['id']))
        
        current_level = None
        for task in sorted_tasks:
            level = task['level']
            # Si el nivel actual es diferente al anterior, insertar un encabezado de nivel
            if current_level != level:
                level_name = ""
                if level == 1:
                    level_name = "NIVEL I - Primer Año"
                elif level == 2:
                    level_name = "NIVEL II - Segundo Año"
                elif level == 3:
                    level_name = "NIVEL III - Tercer Año + Electivas (1)"
                elif level == 4:
                    level_name = "NIVEL IV - Cuarto Año + Electivas (2)"
                elif level == 5:
                    level_name = "NIVEL V - Quinto Año + Electivas (4)"
                else:
                    level_name = f"NIVEL {level}"
                    
                self.tree.insert("", "end", text="", values=("", level_name, "", "", "", ""), tags=("level_header",))
                current_level = level

            # Preparar las columnas de cursadas y aprobadas
            cursadas_text = "-" if task['level'] == 1 else "-".join(str(c) for c in task['cursadas']) if task['cursadas'] else "-"
            aprobadas_text = "-" if task['level'] == 1 else "-".join(str(a) for a in task['aprobadas']) if task['aprobadas'] else "-"
            
            # Obtener valores de los nuevos campos (con valores por defecto para compatibilidad)
            c_value = task.get('c', '-')
            a_value = task.get('a', '-')

            # Determinar el estado de la tarea para el color
            if task['status'] in ["cursada", "en_curso", "completada"]:
                # Usar el estado actual (amarillo, naranja o verde)
                task_tag = task['status']
            elif task['id'] >= 101:
                # Las nuevas materias (ID >= 101) siempre tienen color gris por defecto
                task_tag = "none"
            elif self.is_task_available(task):
                # Si está disponible para cursar, usar color lila
                task_tag = "disponible"
            else:
                # Estado por defecto (gris)
                task_tag = "none"

            # Insertar la tarea con ID en columna separada
            self.tree.insert("", "end", text="", values=(task['id'], task['description'], cursadas_text, aprobadas_text, c_value, a_value), tags=(task_tag,))

def main():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
