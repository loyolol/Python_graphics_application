import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from database import Database
from config import COLLEGE_BLUE, COLLEGE_ORANGE, COLLEGE_GRAY

class CollegeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("НКПиИТ - Система управления студентами")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        self.db = Database()
        self.db.create_tables()
        
        self.setup_styles()
        
        self.create_menu()
        self.create_notebook()
        self.create_status_bar()
        
        self.load_students()
        self.load_subjects()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background=COLLEGE_GRAY)
        style.configure('TNotebook.Tab', background=COLLEGE_GRAY, padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', COLLEGE_BLUE)], 
                  foreground=[('selected', 'white')])
        
        style.configure('Treeview', background='white', fieldbackground='white', 
                       rowheight=25)
        style.configure('Treeview.Heading', background=COLLEGE_BLUE, 
                       foreground='white', relief='flat', font=('Arial', 10, 'bold'))
        style.map('Treeview.Heading', background=[('active', COLLEGE_ORANGE)])
        
        style.configure('TButton', padding=6, relief='flat')
        style.map('TButton',
                 background=[('active', COLLEGE_ORANGE)],
                 foreground=[('active', 'white')])
        
        style.configure('Accent.TButton', background=COLLEGE_ORANGE, foreground='white')
        style.map('Accent.TButton',
                 background=[('active', COLLEGE_BLUE)],
                 foreground=[('active', 'white')])
        
        style.configure('TLabel', background=COLLEGE_GRAY)
        style.configure('TFrame', background=COLLEGE_GRAY)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Экспорт в Excel", command=self.export_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.students_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.students_frame, text="Студенты")
        self.create_students_tab()
        
        self.subjects_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.subjects_frame, text="Предметы")
        self.create_subjects_tab()
        
        self.grades_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.grades_frame, text="Успеваемость")
        self.create_grades_tab()
    
    def create_students_tab(self):
        toolbar = ttk.Frame(self.students_frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        self.create_styled_button(toolbar, "Добавить", self.add_student_dialog).pack(side='left', padx=2)
        self.create_styled_button(toolbar, "Редактировать", self.edit_student_dialog).pack(side='left', padx=2)
        self.create_styled_button(toolbar, "Удалить", self.delete_student).pack(side='left', padx=2)
        
        ttk.Label(toolbar, text="Поиск:").pack(side='left', padx=(20, 2))
        self.search_entry = ttk.Entry(toolbar, width=30)
        self.search_entry.pack(side='left', padx=2)
        ttk.Button(toolbar, text="Найти", command=self.search_students).pack(side='left', padx=2)
        ttk.Button(toolbar, text="Сброс", command=self.load_students).pack(side='left', padx=2)
        
        columns = ('id', 'Фамилия', 'Имя', 'Отчество', 'Группа', 'Дата рождения', 'Телефон')
        self.students_tree = ttk.Treeview(self.students_frame, columns=columns, 
                                          show='headings', height=20)
        
        self.students_tree.heading('id', text='ID')
        self.students_tree.heading('Фамилия', text='Фамилия')
        self.students_tree.heading('Имя', text='Имя')
        self.students_tree.heading('Отчество', text='Отчество')
        self.students_tree.heading('Группа', text='Группа')
        self.students_tree.heading('Дата рождения', text='Дата рождения')
        self.students_tree.heading('Телефон', text='Телефон')
        
        self.students_tree.column('id', width=50)
        self.students_tree.column('Фамилия', width=120)
        self.students_tree.column('Имя', width=120)
        self.students_tree.column('Отчество', width=120)
        self.students_tree.column('Группа', width=80)
        self.students_tree.column('Дата рождения', width=100)
        self.students_tree.column('Телефон', width=120)
        
        scrollbar = ttk.Scrollbar(self.students_frame, orient='vertical', 
                                  command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        self.students_tree.bind('<<TreeviewSelect>>', self.on_student_select)
    
    def create_styled_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command,
                       bg=COLLEGE_ORANGE, fg='white',
                       font=("Arial", 10), padx=15, pady=5,
                       relief='flat', cursor='hand2')
        
        def on_enter(e):
            btn['background'] = COLLEGE_BLUE
        
        def on_leave(e):
            btn['background'] = COLLEGE_ORANGE
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_subjects_tab(self):
        toolbar = ttk.Frame(self.subjects_frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        self.create_styled_button(toolbar, "Добавить", self.add_subject_dialog).pack(side='left', padx=2)
        self.create_styled_button(toolbar, "Редактировать", self.edit_subject_dialog).pack(side='left', padx=2)
        self.create_styled_button(toolbar, "Удалить", self.delete_subject).pack(side='left', padx=2)
        
        columns = ('id', 'Название', 'Часы')
        self.subjects_tree = ttk.Treeview(self.subjects_frame, columns=columns, 
                                          show='headings', height=15)
        
        self.subjects_tree.heading('id', text='ID')
        self.subjects_tree.heading('Название', text='Название предмета')
        self.subjects_tree.heading('Часы', text='Кол-во часов')
        
        self.subjects_tree.column('id', width=50)
        self.subjects_tree.column('Название', width=300)
        self.subjects_tree.column('Часы', width=100)
        
        scrollbar = ttk.Scrollbar(self.subjects_frame, orient='vertical', 
                                  command=self.subjects_tree.yview)
        self.subjects_tree.configure(yscrollcommand=scrollbar.set)
        
        self.subjects_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
    
    def create_grades_tab(self):
        top_frame = ttk.Frame(self.grades_frame)
        top_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(top_frame, text="Студент:").pack(side='left')
        self.student_combo = ttk.Combobox(top_frame, width=50, state='readonly')
        self.student_combo.pack(side='left', padx=5)
        self.student_combo.bind('<<ComboboxSelected>>', self.load_student_grades)
        
        self.create_styled_button(top_frame, "Добавить оценку", self.add_grade_dialog).pack(side='left', padx=20)
        
        columns = ('id', 'Предмет', 'Оценка', 'Дата')
        self.grades_tree = ttk.Treeview(self.grades_frame, columns=columns, 
                                        show='headings', height=15)
        
        self.grades_tree.heading('id', text='ID')
        self.grades_tree.heading('Предмет', text='Предмет')
        self.grades_tree.heading('Оценка', text='Оценка')
        self.grades_tree.heading('Дата', text='Дата')
        
        self.grades_tree.column('id', width=50)
        self.grades_tree.column('Предмет', width=300)
        self.grades_tree.column('Оценка', width=80)
        self.grades_tree.column('Дата', width=100)
        
        scrollbar = ttk.Scrollbar(self.grades_frame, orient='vertical', 
                                  command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=scrollbar.set)
        
        self.grades_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        bottom_frame = ttk.Frame(self.grades_frame)
        bottom_frame.pack(fill='x', padx=5, pady=5)
        
        self.create_styled_button(bottom_frame, "Редактировать оценку", self.edit_grade_dialog).pack(side='left', padx=2)
        self.create_styled_button(bottom_frame, "Удалить оценку", self.delete_grade).pack(side='left', padx=2)
    
    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Готов к работе", 
                                    relief='sunken', anchor='w',
                                    bg=COLLEGE_ORANGE, fg='white')
        self.status_bar.pack(side='bottom', fill='x')
    
    def load_students(self):
        for row in self.students_tree.get_children():
            self.students_tree.delete(row)
        
        students = self.db.get_all_students()
        for student in students:
            self.students_tree.insert('', 'end', values=student)
        
        self.status_bar.config(text=f"Загружено {len(students)} студентов")
        self.update_student_combo()
    
    def search_students(self):
        search_text = self.search_entry.get().lower()
        
        for row in self.students_tree.get_children():
            self.students_tree.delete(row)
        
        students = self.db.get_all_students()
        found = 0
        for student in students:
            if search_text in str(student).lower():
                self.students_tree.insert('', 'end', values=student)
                found += 1
        
        self.status_bar.config(text=f"Найдено {found} студентов")
    
    def add_student_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление студента")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        fields = [
            ('Фамилия:', 'last_name'),
            ('Имя:', 'first_name'),
            ('Отчество:', 'middle_name'),
            ('Группа:', 'group_name'),
            ('Дата рождения (ГГГГ-ММ-ДД):', 'birth_date'),
            ('Телефон:', 'phone')
        ]
        
        entries = {}
        row = 0
        for label, key in fields:
            ttk.Label(dialog, text=label).grid(row=row, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            entries[key] = entry
            row += 1
        
        def save():
            if not entries['last_name'].get() or not entries['first_name'].get() or not entries['group_name'].get():
                messagebox.showerror("Ошибка", "Фамилия, имя и группа обязательны для заполнения")
                return
            
            try:
                student_id = self.db.add_student(
                    entries['last_name'].get(),
                    entries['first_name'].get(),
                    entries['middle_name'].get(),
                    entries['group_name'].get(),
                    entries['birth_date'].get() or None,
                    entries['phone'].get() or None
                )
                
                messagebox.showinfo("Успех", f"Студент добавлен с ID: {student_id}")
                dialog.destroy()
                self.load_students()
                
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='left', padx=5)
    
    def edit_student_dialog(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите студента для редактирования")
            return
        
        values = self.students_tree.item(selected[0])['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование студента")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        fields = [
            ('Фамилия:', 'last_name'),
            ('Имя:', 'first_name'),
            ('Отчество:', 'middle_name'),
            ('Группа:', 'group_name'),
            ('Дата рождения:', 'birth_date'),
            ('Телефон:', 'phone')
        ]
        
        entries = {}
        row = 0
        for label, key in fields:
            ttk.Label(dialog, text=label).grid(row=row, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            
            if key == 'last_name':
                entry.insert(0, values[1])
            elif key == 'first_name':
                entry.insert(0, values[2])
            elif key == 'middle_name':
                entry.insert(0, values[3] if values[3] else '')
            elif key == 'group_name':
                entry.insert(0, values[4])
            elif key == 'birth_date':
                entry.insert(0, values[5] if values[5] else '')
            elif key == 'phone':
                entry.insert(0, values[6] if values[6] else '')
            
            entries[key] = entry
            row += 1
        
        def save():
            try:
                self.db.update_student(
                    values[0],
                    entries['last_name'].get(),
                    entries['first_name'].get(),
                    entries['middle_name'].get(),
                    entries['group_name'].get(),
                    entries['birth_date'].get() or None,
                    entries['phone'].get() or None
                )
                
                messagebox.showinfo("Успех", "Данные студента обновлены")
                dialog.destroy()
                self.load_students()
                
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='left', padx=5)
    
    def delete_student(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите студента для удаления")
            return
        
        values = self.students_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить студента {values[1]} {values[2]}?"):
            self.db.delete_student(values[0])
            self.load_students()
            messagebox.showinfo("Успех", "Студент удален")
    
    def on_student_select(self, event):
        selected = self.students_tree.selection()
        if selected:
            values = self.students_tree.item(selected[0])['values']
            self.status_bar.config(text=f"Выбран студент: {values[1]} {values[2]} {values[3]}")
    
    def load_subjects(self):
        for row in self.subjects_tree.get_children():
            self.subjects_tree.delete(row)
        
        subjects = self.db.get_all_subjects()
        for subject in subjects:
            self.subjects_tree.insert('', 'end', values=subject)
        
        self.status_bar.config(text=f"Загружено {len(subjects)} предметов")
    
    def add_subject_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление предмета")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Название предмета:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Кол-во часов:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        hours_entry = ttk.Entry(dialog, width=30)
        hours_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def save():
            if not name_entry.get():
                messagebox.showerror("Ошибка", "Название предмета обязательно")
                return
            
            try:
                hours = int(hours_entry.get()) if hours_entry.get() else 0
                self.db.add_subject(name_entry.get(), hours)
                messagebox.showinfo("Успех", "Предмет добавлен")
                dialog.destroy()
                self.load_subjects()
            except ValueError:
                messagebox.showerror("Ошибка", "Часы должны быть числом")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='left', padx=5)
    
    def edit_subject_dialog(self):
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите предмет для редактирования")
            return
        
        values = self.subjects_tree.item(selected[0])['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование предмета")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Название предмета:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, values[1])
        
        ttk.Label(dialog, text="Кол-во часов:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        hours_entry = ttk.Entry(dialog, width=30)
        hours_entry.grid(row=1, column=1, padx=10, pady=5)
        hours_entry.insert(0, values[2])
        
        def save():
            try:
                hours = int(hours_entry.get()) if hours_entry.get() else 0
                self.db.update_subject(values[0], name_entry.get(), hours)
                messagebox.showinfo("Успех", "Предмет обновлен")
                dialog.destroy()
                self.load_subjects()
            except ValueError:
                messagebox.showerror("Ошибка", "Часы должны быть числом")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='left', padx=5)
    
    def delete_subject(self):
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите предмет для удаления")
            return
        
        values = self.subjects_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить предмет {values[1]}?"):
            self.db.delete_subject(values[0])
            self.load_subjects()
            messagebox.showinfo("Успех", "Предмет удален")
    
    def update_student_combo(self):
        students = self.db.get_all_students()
        student_list = [f"{s[1]} {s[2]} {s[3]} (ID: {s[0]})" for s in students]
        self.student_combo['values'] = student_list
        if student_list:
            self.student_combo.set('')
    
    def load_student_grades(self, event=None):
        selection = self.student_combo.get()
        if not selection:
            return
        
        try:
            student_id = int(selection.split('ID: ')[1].rstrip(')'))
        except:
            return
        
        for row in self.grades_tree.get_children():
            self.grades_tree.delete(row)
        
        grades = self.db.get_grades_by_student(student_id)
        for grade in grades:
            self.grades_tree.insert('', 'end', values=grade)
        
        self.status_bar.config(text=f"Загружено {len(grades)} оценок")
    
    def add_grade_dialog(self):
        if not self.student_combo.get():
            messagebox.showwarning("Предупреждение", "Выберите студента")
            return
        
        try:
            student_id = int(self.student_combo.get().split('ID: ')[1].rstrip(')'))
        except:
            messagebox.showerror("Ошибка", "Не удалось определить ID студента")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление оценки")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Предмет:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        
        subjects = self.db.get_all_subjects()
        subject_dict = {f"{s[1]}": s[0] for s in subjects}
        subject_combo = ttk.Combobox(dialog, values=list(subject_dict.keys()), width=25, state='readonly')
        subject_combo.grid(row=0, column=1, padx=10, pady=5)
        if subject_dict:
            subject_combo.set(list(subject_dict.keys())[0])
        
        ttk.Label(dialog, text="Оценка:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        grade_combo = ttk.Combobox(dialog, values=[2, 3, 4, 5], width=25, state='readonly')
        grade_combo.grid(row=1, column=1, padx=10, pady=5)
        grade_combo.set(4)
        
        ttk.Label(dialog, text="Дата:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        date_entry = ttk.Entry(dialog, width=25)
        date_entry.grid(row=2, column=1, padx=10, pady=5)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def save():
            if not subject_combo.get() or not grade_combo.get():
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                subject_id = subject_dict[subject_combo.get()]
                grade = int(grade_combo.get())
                
                self.db.add_grade(student_id, subject_id, grade, date_entry.get())
                
                messagebox.showinfo("Успех", "Оценка добавлена")
                dialog.destroy()
                self.load_student_grades()
                
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='left', padx=5)
    
    def edit_grade_dialog(self):
        selected = self.grades_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите оценку для редактирования")
            return
        
        values = self.grades_tree.item(selected[0])['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование оценки")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Предмет:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        ttk.Label(dialog, text=values[1]).grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        ttk.Label(dialog, text="Оценка:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        grade_combo = ttk.Combobox(dialog, values=[2, 3, 4, 5], width=20, state='readonly')
        grade_combo.grid(row=1, column=1, padx=10, pady=5)
        grade_combo.set(values[2])
        
        ttk.Label(dialog, text="Дата:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        date_entry = ttk.Entry(dialog, width=20)
        date_entry.grid(row=2, column=1, padx=10, pady=5)
        date_entry.insert(0, values[3])
        
        def save():
            try:
                self.db.update_grade(values[0], int(grade_combo.get()), date_entry.get())
                messagebox.showinfo("Успех", "Оценка обновлена")
                dialog.destroy()
                self.load_student_grades()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side='left', padx=5)
    
    def delete_grade(self):
        selected = self.grades_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите оценку для удаления")
            return
        
        values = self.grades_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить оценку по предмету {values[1]}?"):
            self.db.delete_grade(values[0])
            self.load_student_grades()
            messagebox.showinfo("Успех", "Оценка удалена")
    
    def export_to_excel(self):
        messagebox.showinfo("Информация", "Функция экспорта будет доступна в следующей версии")
    
    def show_about(self):
        about_text = """
        НКПиИТ - Система управления студентами
        Версия 1.0
        
        Разработано для колледжа НКПиИТ
        © 2026
        """
        messagebox.showinfo("О программе", about_text)
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()