from flask import Flask, render_template, request, redirect, abort
import requests

app = Flask(__name__)

api_url = 'https://todo-api-84y2.onrender.com/api/tasks'

@app.route('/', methods = {'GET', 'POST'})
def home ():
    if request.method == 'GET':
        tasks = requests.get(api_url).json()['tasks']
        completed = []
        incompleted = []

        for task in tasks:
            if task['status'] == True:
                completed.append(task)
            else:
                incompleted.append(task)

        response = {'completed' : completed,
                    'incompleted' : incompleted,
                    'counter1' : len(completed),
                    'counter2' : len(incompleted)
                    }

        return render_template('index.html', response = response)
    else:   # POST
        name = request.form['name']
        try:
            requests.post(api_url, json={'name' : name})
            return redirect('/')
        except:
            abort(500)

if __name__ == '__main__':
    app.run(debug = True)