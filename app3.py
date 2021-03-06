#!flask/bin/python
# Version: 1.1
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
import json


app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'devops':
        return 'devops'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
def read_data():
   with open("4forces.json","r") as f:
     data = f.read()
   tasks = json.loads(data)
   return tasks

tasks = read_data()
 
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True, _scheme='https')
        else:
            new_task[field] = task[field]
    return new_task

def write_data(tasks):
    data = json.dumps(tasks)
    with open("4forces.json","w") as f:
        f.write(data)
    return
    
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
@auth.login_required
def create_task():
    # id = 0;
    if not request.json or not 'title' in request.json:
        abort(400)
    # if len(tasks) < 0:
    #     id = 0
    if len(tasks) > 0:
        id = tasks[-1]['id'] + 1
    task = {
        'id': id,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'comment': request.json.get('comment', ""),
        'done': False
    }
    tasks.append(task)
    write_data(tasks)
    return jsonify( { 'task': make_public_task(task) } ), 201
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['comment'] = request.json.get('comment', task[0]['comment'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    write_data(tasks)
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    write_data(tasks)
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)

