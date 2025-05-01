from flask import Flask, request, jsonify
from database import mydb_connection
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
print(__name__)
print(app)


@app.route("/", methods=["GET"])
def index():
    mydb = mydb_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    mytables = mycursor.fetchall()
    mydb.close()
    return jsonify({"message": "Hello, World!", "tableList": mytables}), 201


@app.route("/AddTask", methods=["POST"])
def add_task():
    request_data = request.get_json()
    print(request_data)
    if request.json is None:
        return jsonify({"error": "Invalid JSON"}), 400
    elif "task" not in request_data or request_data["task"] == "":
        return jsonify({"error": "Missing 'task' field"}), 400
    else:
        mydb = mydb_connection()
        mycursor = mydb.cursor()
        mycursor.execute(
            "INSERT INTO todo_list (task) values (%s)", (request_data["task"],)
        )
        mydb.commit()
        mydb.close()
    return jsonify({"message": "Task added successfully!"}), 201


@app.route("/EditTask/<int:item_id>", methods=["PUT"])
def edit_task(item_id):
    request_data = request.get_json()
    if request.json is None:
        return jsonify({"error": "Invalid JSON"}), 400
    elif "task" not in request_data or request_data["task"] == "":
        return jsonify({"error": "Missing 'task' field"}), 400
    else:
        mydb = mydb_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id FROM todo_list WHERE id= %s", (item_id,))
        task = mycursor.fetchone()
        if task is None:
            mydb.commit()
            mydb.close()
            return jsonify({"error": "Task not found"}), 404
        else:
            mycursor.execute(
                "UPDATE todo_list SET task = %s WHERE id = %s",
                (request_data["task"], item_id),
            )
            mydb.commit()
            mydb.close()
    return jsonify({"message": "Task updated successfully!"}), 201


@app.route("/DeleteTask/<int:item_id>", methods=["DELETE"])
def delete_task(item_id):
    mydb = mydb_connection()
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM todo_list WHERE id = %s", (item_id,))
    mydb.commit()
    mydb.close()
    return jsonify({"message": "Task deleted successfully!"}), 201


@app.route("/ListTask", methods=["GET"])
def list_task():
    mydb = mydb_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM todo_list WHERE is_deleted = 0")
    tasks = [dict(zip([column[0] for column in mycursor.description], row)) for row in mycursor.fetchall()]
    mydb.close()

    return jsonify({"message": "Success", "taskList": tasks}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
