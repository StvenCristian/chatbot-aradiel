from flask import Flask, render_template,jsonify,request

import entity
import services as serv
import json
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/contexto')
def render_contexto():  # put application's code here
    return render_template('contexto.html')

@app.route('/dashboard')
def render_dashboard():  # put application's code here
    return render_template('dashboard.html')


@app.route('/api/atencion/generar')
def genera_atencion():
    response=serv.GenerarAtencion()
    if response is None:
        success=False
        message="Ocurrio un error interno"
    else:
        success = True
        message = "OK"
        obj = response
    return jsonify({"success":success,"message":message,"obj":json.dumps(response.__dict__)})

@app.route('/api/atencion/finalizar',methods=["POST"])
def finalizar_atencion():
    datos=request.json
    atencion=entity.Atencion()
    atencion.IdAtencion=datos['id_atencion']
    atencion.Calificacion=datos['calificacion']
    response=serv.FinalizarAtencion(atencion.IdAtencion,atencion.Calificacion)
    if response is None:
        success = False
        message = "Ocurrio un error interno"
    else:
        success = True
        message = "OK"
    return jsonify({"success": success, "message": message})

@app.route('/api/categorias/all')
def obtener_categorias():
    response=serv.ObtenerCategorias()
    print(response)
    if response is None:
        success=False
        message="Ocurrio un error interno"
    else:
        success = True
        message = "OK"
        obj = response
    return jsonify({"success":success,"message":message,"obj":json.dumps([ob.__dict__ for ob in response])})

@app.route('/api/atencion/all')
def obtener_total_atencion():
    response=serv.ObtenerListaAtencion()
    print(response)
    if response is None:
        success=False
        message="Ocurrio un error interno"
    else:
        success = True
        message = "OK"
        obj = response
    return jsonify({"success":success,"message":message,"obj":json.dumps([ob.__dict__ for ob in response])})

@app.route('/api/contexto/registrar',methods=["POST"])
def registrar_contexto():
    datos = request.json
    contexto = entity.Contexto()
    contexto.DetalleContexto = datos['detalle_contexto']
    contexto.IdCategoria = datos['id_categoria']
    response=serv.RegistrarContexto(contexto)
    if response is False:
        success=False
        message="Ocurrio un error interno"
    else:
        success = True
        message = "OK"
    return jsonify({"success":success,"message":message})

@app.route('/api/bot/preguntar',methods=["POST"])
def preguntar_bot():
    datos = request.json
    id_atencion=datos['id_atencion']
    pregunta = datos['pregunta']
    id_categoria = datos['id_categoria']
    response=serv.ObtenerRespuesta(pregunta,id_categoria,id_atencion)
    if response is None:
        success=False
        message="Ocurrio un error preguntando al bot"
    else:
        success = True
        message = "OK"
    return jsonify({"success":success,"message":message,"obj":json.dumps(response.__dict__)})

@app.route('/api/contexto/all')
def obtener_contextos():
    response=serv.ObtenerContextos()
    if response is None:
        success=False
        message="Ocurrio un error interno"
    else:
        success = True
        message = "OK"
        obj = response
    return jsonify({"success":success,"message":message,"obj":json.dumps([ob.__dict__ for ob in response])})

if __name__ == '__main__':
    app.run()


