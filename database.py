# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
from config import SERVER, DATABASE, USERNAME, PASSWORD, PORT

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(
                host=SERVER,
                database=DATABASE,
                user=USERNAME,
                password=PASSWORD,
                port=PORT
            )
            self.cursor = self.connection.cursor()
            print("Успешное подключение к базе данных")
        except Error as e:
            print(f"Ошибка подключения: {e}")
    
    def create_tables(self):
        """Создание таблиц, если они не существуют"""
        try:
            
            query_students = '''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                last_name NVARCHAR(50) NOT NULL,
                first_name NVARCHAR(50) NOT NULL,
                middle_name NVARCHAR(50),
                group_name NVARCHAR(20) NOT NULL,
                birth_date DATE,
                phone VARCHAR(20)
            )
            '''
            self.cursor.execute(query_students)
            
            
            query_subjects = '''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                name NVARCHAR(100) NOT NULL UNIQUE,
                hours INTEGER
            )
            '''
            self.cursor.execute(query_subjects)
            
            
            query_grades = '''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade INTEGER CHECK (grade >= 2 AND grade <= 5),
                date DATE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            )
            '''
            self.cursor.execute(query_grades)
            
            self.connection.commit()
            print("Таблицы успешно созданы")
            
            
            self.add_test_data()
            
        except Error as e:
            print(f"Ошибка создания таблиц: {e}")
    
    def add_test_data(self):
        """Добавление тестовых данных"""
        try:
            
            self.cursor.execute("SELECT COUNT(*) FROM students")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                
                students = [
                    ('Иванов', 'Иван', 'Иванович', 'ИС-21', '2005-03-15', '+7-999-123-45-67'),
                    ('Петров', 'Петр', 'Петрович', 'ИС-21', '2005-07-22', '+7-999-234-56-78'),
                    ('Сидорова', 'Анна', 'Сергеевна', 'ИС-22', '2006-01-10', '+7-999-345-67-89'),
                    ('Козлов', 'Дмитрий', 'Алексеевич', 'ИС-22', '2005-11-30', '+7-999-456-78-90'),
                    ('Смирнова', 'Елена', 'Викторовна', 'ИС-21', '2006-05-05', '+7-999-567-89-01')
                ]
                
                add_student = '''
                INSERT INTO students (last_name, first_name, middle_name, group_name, birth_date, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
                '''
                
                for student in students:
                    self.cursor.execute(add_student, student)
                
                
                subjects = [
                    ('Математика', 120),
                    ('Информатика', 100),
                    ('Физика', 90),
                    ('Английский язык', 80),
                    ('История', 70)
                ]
                
                add_subject = '''
                INSERT INTO subjects (name, hours)
                VALUES (%s, %s)
                '''
                
                for subject in subjects:
                    self.cursor.execute(add_subject, subject)
                
                
                import random
                from datetime import date
                
                add_grade = '''
                INSERT INTO grades (student_id, subject_id, grade, date)
                VALUES (%s, %s, %s, %s)
                '''
                
                for student_id in range(1, 6):
                    for subject_id in range(1, 6):
                        grade = random.randint(3, 5)
                        self.cursor.execute(add_grade, (student_id, subject_id, grade, date.today()))
                
                self.connection.commit()
                print("Тестовые данные добавлены")
                
        except Error as e:
            print(f"Ошибка добавления тестовых данных: {e}")
    
    
    def add_student(self, last_name, first_name, middle_name, group_name, birth_date, phone):
        """Добавление студента"""
        query = '''
        INSERT INTO students (last_name, first_name, middle_name, group_name, birth_date, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (last_name, first_name, middle_name, group_name, birth_date, phone)
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_students(self):
        """Получение всех студентов"""
        query = "SELECT * FROM students ORDER BY last_name, first_name"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def update_student(self, student_id, last_name, first_name, middle_name, group_name, birth_date, phone):
        """Обновление данных студента"""
        query = '''
        UPDATE students 
        SET last_name=%s, first_name=%s, middle_name=%s, group_name=%s, birth_date=%s, phone=%s
        WHERE id=%s
        '''
        values = (last_name, first_name, middle_name, group_name, birth_date, phone, student_id)
        self.cursor.execute(query, values)
        self.connection.commit()
    
    def delete_student(self, student_id):
        """Удаление студента"""
        query = "DELETE FROM students WHERE id=%s"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()
    
    
    def add_subject(self, name, hours):
        """Добавление предмета"""
        query = "INSERT INTO subjects (name, hours) VALUES (%s, %s)"
        self.cursor.execute(query, (name, hours))
        self.connection.commit()
    
    def get_all_subjects(self):
        """Получение всех предметов"""
        query = "SELECT * FROM subjects ORDER BY name"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def update_subject(self, subject_id, name, hours):
        """Обновление предмета"""
        query = "UPDATE subjects SET name=%s, hours=%s WHERE id=%s"
        self.cursor.execute(query, (name, hours, subject_id))
        self.connection.commit()
    
    def delete_subject(self, subject_id):
        """Удаление предмета"""
        query = "DELETE FROM subjects WHERE id=%s"
        self.cursor.execute(query, (subject_id,))
        self.connection.commit()
    
    
    def add_grade(self, student_id, subject_id, grade, date):
        """Добавление оценки"""
        query = "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (student_id, subject_id, grade, date))
        self.connection.commit()
    
    def get_grades_by_student(self, student_id):
        """Получение оценок студента"""
        query = '''
        SELECT g.id, s.name, g.grade, g.date 
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id=%s
        ORDER BY g.date DESC
        '''
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchall()
    
    def update_grade(self, grade_id, grade, date):
        """Обновление оценки"""
        query = "UPDATE grades SET grade=%s, date=%s WHERE id=%s"
        self.cursor.execute(query, (grade, date, grade_id))
        self.connection.commit()
    
    def delete_grade(self, grade_id):
        """Удаление оценки"""
        query = "DELETE FROM grades WHERE id=%s"
        self.cursor.execute(query, (grade_id,))
        self.connection.commit()
    
    def close(self):
        """Закрытие соединения"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()