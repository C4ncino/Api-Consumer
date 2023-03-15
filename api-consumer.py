from flask import Flask, render_template, request, redirect, abort
import requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'

app = Flask(__name__)

api_url = 'https://todo-api-84y2.onrender.com/api/tasks'
# api_url = 'http://127.0.0.1:5000/api/tasks'

@app.route('/', methods = {'GET', 'POST', 'PUT', 'DELETE'})

def home ():
    tasks = requests.get(api_url).json()['tasks']

    if request.method == 'GET':
        completed = []
        incompleted = []

        for task in tasks:
            if task['status'] == True:
                completed.append(task)
            else:
                incompleted.append(task)

        response = {
                    'completed' : completed,
                    'incompleted' : incompleted,
                    'counter1' : len(completed),
                    'counter2' : len(incompleted)
                    }
        return render_template('index.html', response = response)
    
    elif request.method == 'POST':
        method = request.form['_method']
        name = request.form['name']

        if method == 'POST':
            print(request.form)
            name = name.strip()
            try:
                requests.post(api_url, json={'name' : name})
                return redirect('/')
            except:
                abort(500)
        elif method == 'PUT':
            task = [task for task in tasks if task['name'] == name][0]
            uri = '/' + str(task['id'])
            try:
                requests.put(api_url + uri, json={'status' : (not task['status'])})
                return redirect('/')
            except:
                abort(500)
        elif method == 'DELETE':
            task = [task for task in tasks if task['name'] == name][0]
            uri = '/' + str(task['id'])
            try:
                requests.delete(api_url + uri)
                return redirect('/')
            except:
                abort(500)


        

if __name__ == '__main__':
    app.run(debug = True, port=5001)