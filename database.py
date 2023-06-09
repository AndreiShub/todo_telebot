import sqlite3
connect = sqlite3.connect('database.db') # создает подключение к базе данных database.db
cursor = connect.cursor() 

create_tabl_task = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    task TEXT,
    done BOOLEAN
    );
"""
create_tabl_user = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    chat_id INTEGER
    );
"""
cursor.execute(create_tabl_task) # выполняет SQL запрос на создание базы данных
cursor.execute(create_tabl_user)
connect.commit() # Сохранить изменения в базе данных.


def register(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    user = (message.from_user.first_name, message.from_user.id)
    cursor.execute("INSERT INTO users (name, chat_id) VALUES (?, ?)", user)
    connect.commit()
    connect.close()


def deletetask(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    chat_id = (message.from_user.id,)
    cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
    user = cursor.fetchone()
    if user is None:
        connect.close()
        return "Вы не зарегистрированы в системе!"
    else:
        task_id = message.text.split("/deletetask")[1]
        if task_id == "":
            connect.close()
            return "Ошибка"
        else:
            task_id = (int(task_id),)
            user = (int(user[0]),)
            cursor.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", task_id + user)
            task = cursor.fetchone()
            if task is None:
                connect.close()
                return "Такой записи нет"
            else:
                cursor.execute("DELETE FROM tasks WHERE id=?", task_id)
                connect.commit()
                connect.close()
                return "Ваша запись удалена"


def add_task(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    chat_id = (message.from_user.id,)
    cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
    user = cursor.fetchone()
    if user is None:
        connect.close()
        return "Вы не зареегистрированы"
    else:
        task = message.text.split('/add_task')[1]
        if task == "":
            connect.close()
            return "Ошибка: Пустая задача"
        else:
            task_data = (user[0], task, False)
            cursor.execute("INSERT INTO tasks (user_id, task, done) VALUES (?, ?, ?)", task_data)
            connect.commit()
            connect.close()
            return "Задача добавлена"


def list_task(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    chat_id = (message.from_user.id,)
    cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
    user = cursor.fetchone()
    if user is None:
       connect.close()
       return "Ты не зарегистрирован"
    else:
        user = (int(user[0]),)
        cursor.execute("SELECT * FROM tasks WHERE user_id=?", user)
        tasks = cursor.fetchall()
        if tasks:
            task = ''
            for i in tasks:
                task += f'ID записи: {i[0]}\nОписание задачи: {i[2]}\nСостояние задачи: {"Выполнено" if i[3] else "Невыполнено"}\n\n'
            connect.close()
            return task
        else:
            connect.close()
            return "У вас нет задач"

    
