from flask import Flask, jsonify, request
import controllers.db_management as dbm
import time


dbm.create_db()

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Prueba tecnica'

@app.route('/search', methods=['GET'])
def search():
    t1 = time.time()
    data:str = request.get_json()['text'].strip()
    result:dict = dbm.school_search(data.upper())
    t2 = time.time()
    finish_time = round(t2-t1,5)
    response = {"message":f"Results for '{data}' (search took: {finish_time}s)"}
    response.update(result)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
