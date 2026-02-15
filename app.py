from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jeba@200308",
    database="task_manager"
)

cursor = db.cursor()

# Home page
@app.route('/')
def home():
    cursor.execute("SELECT id, task_name, created_at FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    return render_template('home.html', tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    query = "INSERT INTO tasks (task_name) VALUES (%s)"
    cursor.execute(query, (task,))
    db.commit()
    return redirect(url_for('home'))

# Delete task
@app.route('/delete/<int:id>')
def delete_task(id):
    query = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    return redirect(url_for('home'))

# Edit task page
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'POST':
        new_task = request.form['task']
        query = "UPDATE tasks SET task_name = %s WHERE id = %s"
        cursor.execute(query, (new_task, id))
        db.commit()
        return redirect(url_for('home'))
    
    query = "SELECT * FROM tasks WHERE id = %s"
    cursor.execute(query, (id,))
    task = cursor.fetchone()
    return render_template('edit.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)

