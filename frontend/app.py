import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:5000')

@app.route('/')
def index():
    response = requests.get(f'{BACKEND_URL}/tasks')
    tasks = response.json()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form.get('description')
        }
        requests.post(f'{BACKEND_URL}/tasks', json=data)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/tasks/<int:id>/update', methods=['GET', 'POST'])
def update_task(id):
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form.get('description'),
            'status': request.form['status']
        }
        requests.put(f'{BACKEND_URL}/tasks/{id}', json=data)
        return redirect(url_for('index'))
    response = requests.get(f'{BACKEND_URL}/tasks/{id}')
    task = response.json()
    return render_template('update.html', task=task)

@app.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    requests.delete(f'{BACKEND_URL}/tasks/{id}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)