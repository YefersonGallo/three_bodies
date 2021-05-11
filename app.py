from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from three_bodies import ThreeBody, gif

app = Flask(__name__)
CORS(app, support_credentials=True)

# Petición para comprobar la conexión del servidor
@app.route('/ping', methods=['GET'])
@cross_origin(supports_credentials=True)
def ping():
    return jsonify({'response': 'pong!'})


@app.route('/solve_problem', methods=['POST'])
@cross_origin(supports_credentials=True)
def solve():
    m_nd = request.json["m_nd"]
    r_nd = request.json["r_nd"]
    v_nd = request.json["v_nd"]
    t_nd = request.json["t_nd"]
    m_1 = request.json["m_1"]
    m_2 = request.json["m_2"]
    m_3 = request.json["m_3"]
    r_1 = request.json["r_1"]
    r_2 = request.json["r_2"]
    r_3 = request.json["r_3"]
    r_4 = request.json["r_4"]
    r_5 = request.json["r_5"]
    r_6 = request.json["r_6"]
    r_7 = request.json["r_7"]
    r_8 = request.json["r_8"]
    r_9 = request.json["r_9"]
    v_1 = request.json["v_1"]
    v_2 = request.json["v_2"]
    v_3 = request.json["v_3"]
    v_4 = request.json["v_4"]
    v_5 = request.json["v_5"]
    v_6 = request.json["v_6"]
    v_7 = request.json["v_7"]
    v_8 = request.json["v_8"]
    v_9 = request.json["v_9"]
    m = [m_1, m_2, m_2]
    r = [r_1, r_2, r_3, r_4, r_5, r_6, r_7, r_8, r_9]
    v = [v_1, v_2, v_3, v_4, v_5, v_6, v_7, v_8, v_9]
    t = 20
    bodies = ThreeBody(m_nd, r_nd, v_nd, t_nd, m, r, v, t)
    bodies.Simulation()
    return jsonify("ImagenCreada")


@app.route('/get_image')
@cross_origin(supports_credentials=True)
def get_image():
    return jsonify({'response': gif().decode('utf-8')})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
