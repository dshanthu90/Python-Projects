import os
from flask import (Flask, jsonify, request, flash, url_for, json, make_response)

import sqlite3



# Setting the DB name
DB_FILE = os.path.abspath('sqlite_db.db')

app = Flask(__name__)


# define DB connection method
def db_connect():
    conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    #conn.row_factory = sqlite3.Row
    return conn


# now db will have the cursor object
# commenting this line since creating the db object here is creating when instantiating the object and is not able to use it in next thread
# db = db_connect()

# Create Table objects in it
with app.open_resource('schema.sql', mode='r') as f:
    db = db_connect()
    db.executescript(f.read())
    db.commit()


@app.route('/')
def home_page():
    return "Honey Do Mobile App Home Page"
# 1. This method will display all task list if no arg/user id is not provided
# 2. This method will list the tasks assigned to that user if user id is provided
# 3. This method will also create a new task if its a post method.
# this method is at user level - Need to write/include ways to change assignment
@app.route('/honeydo/honeycombs/<int:combId>/tasks' , defaults={'userId': None})
@app.route('/honeydo/honeycombs/<int:combId>/tasks/<int:userId>', methods=['GET','POST'])
def list_task(combId, userId):
    db = db_connect()
    if request.method == 'POST':
        detail = request.form['TaskDescription']
        due = request.form['Due']
        created_by = userId
        assigned = request.form['AssignedTo']
        status = 0
        error = None

        if not detail:
            error = 'Error : Task Description is required to create a task .'

        if not assigned:
            assigned = userId

        if error is not None:
            flash(error)
        else:

            db.execute(
                'INSERT INTO task_list(task_detail,task_due,task_created_by, task_assigned, task_comb_id, task_status) VALUES(?,?,?,?,?,?)',
                (detail, due, created_by, assigned, combId, status)
            )
            db.commit()
            task_row = db.execute('SELECT task_detail, task_assigned, task_due FROM task_list WHERE  task_status = 0 AND task_comb_id=? ORDER BY task_due DESC',(combId,)  ).fetchall()
            task_list= []
            for task in task_row:
                json_task = json.dumps(task)
                task_list.append(json_task)
            return jsonify(task_list)
            #return redirect(url_for('list_task'))
            #return "Task Created"
    if request.method == 'GET' and userId is not None:
        task_row = db.execute('SELECT task_detail, task_due FROM task_list WHERE task_assigned=? AND task_comb_id=? AND task_status = 0 ORDER BY task_due DESC', (userId,combId) ).fetchall()
        if task_row is None:
            return "No tasks today !"
        else:
            task_list = []
            for task in task_row:
                json_task = json.dumps(task)
                task_list.append(json_task)
            return jsonify(task_list)


    elif request.method == 'GET' and userId is None:
        task_row = db.execute('SELECT  task_detail, task_assigned , task_due from task_list WHERE task_status = 0').fetchall()
        if task_row is None:
            return "No tasks today !"
        else:
            task_list = []
            for task in task_row:
                json_task = json.dumps(task)
                task_list.append(json_task)
            return jsonify(task_list)
@app.route('/honeydo/honeycombs/<int:combId>/tasks/<int:userId>/task/<int:taskId>', methods=('GET', 'PUT'))
def update_task(combId, userId, taskId):
    db = db_connect()
    if request.method=='PUT':
        db.execute('UPDATE task_list SET task_status=1 WHERE task_id=? AND task_comb_id=?', (taskId, combId))
        db.commit()
        task_row = db.execute(
            'SELECT task_detail, task_assigned, task_due FROM task_list WHERE  task_status = 0 AND task_comb_id=? AND task_assigned=? ORDER BY task_due DESC',
            (combId,userId)).fetchall()
        task_list = []
        for task in task_row:
            json_task = json.dumps(task)
            task_list.append(json_task)
        return jsonify(task_list)
        # Need to remove return statement
        #return "Task marked to done"
    elif request.method=='GET':
        task_row = db.execute('select * from task_list WHERE task_id=?', (taskId,)).fetchall()
        task_list = []
        for task in task_row:
            json_task = json.dumps(task)
            task_list.append(json_task)
            # print (task_list)
        return jsonify(task_list)


#To unassign receive a code of 0  and to change assignment, receive respective codes
@app.route('/honeydo/honeycombs/<int:combId>/tasks/<int:userId>/task/<int:taskId>/assignment/<int:assign>', methods=['PUT'])
def update_assignment(combId,userId,taskId,assign):
    db = db_connect()
    if assign == 0 :
        db.execute('UPDATE task_list SET task_assigned=NULL  WHERE task_id=? AND task_comb_id=?',(taskId,combId))
        db.commit()
        return "Task unassigned"
    else:
        db.execute('UPDATE task_list SET task_assigned=? WHERE task_id=? AND task_comb_id=?',(assign, taskId, combId))
        db.commit()
        return "Task assigned."


# Test codes
#    if request.method == 'GET':
#        task = [{"task desc": "buy milk", "task_due": "Today"}, {"task desc": "Pay EB Bill","task_due": "Tooday"}]
#        #return '{"abc": "223", "list": [{"child": "1"}, {"child": "2"}]}'
#        return json.dumps(task)
#        #return "post method"
#    return "Call Task create Method"


if __name__ == '__main__':
    app.run()
