from quart import Quart, jsonify
app = Quart(__name__)

@app.route('/hello')
async def hello():
    response = {"message": "Hola Mundo"}
    return jsonify(response)
if __name__ == '__main__':
    app.run(host='localhost', port=5050)

#curl -X GET http://127.0.0.1:5050/hello