from flask import Blueprint, request, jsonify
from models import db, Credito

creditos_bp = Blueprint('creditos_bp', __name__)

@creditos_bp.route('/creditos', methods=['POST'])
def registrar_credito():
    data = request.json
    nuevo_credito = Credito(
        cliente=data['cliente'],
        monto=data['monto'],
        tasa_interes=data['tasa_interes'],
        plazo=data['plazo'],
        fecha_otorgamiento=data['fecha_otorgamiento']
    )
    db.session.add(nuevo_credito)
    db.session.commit()
    return jsonify({"message": "Crédito registrado correctamente"}), 201

@creditos_bp.route('/creditos', methods=['GET'])
def listar_creditos():
    creditos = Credito.query.all()
    resultado = [{"id": c.id, "cliente": c.cliente, "monto": c.monto, "tasa_interes": c.tasa_interes, "plazo": c.plazo, "fecha_otorgamiento": c.fecha_otorgamiento} for c in creditos]
    return jsonify(resultado)

@creditos_bp.route('/creditos/<int:id>', methods=['PUT'])
def editar_credito(id):
    data = request.json
    credito = Credito.query.get(id)
    if not credito:
        return jsonify({"error": "Crédito no encontrado"}), 404

    credito.cliente = data.get('cliente', credito.cliente)
    credito.monto = data.get('monto', credito.monto)
    credito.tasa_interes = data.get('tasa_interes', credito.tasa_interes)
    credito.plazo = data.get('plazo', credito.plazo)
    credito.fecha_otorgamiento = data.get('fecha_otorgamiento', credito.fecha_otorgamiento)

    db.session.commit()
    return jsonify({"message": "Crédito actualizado correctamente"})

@creditos_bp.route('/creditos/<int:id>', methods=['DELETE'])
def eliminar_credito(id):
    credito = Credito.query.get(id)
    if not credito:
        return jsonify({"error": "Crédito no encontrado"}), 404

    db.session.delete(credito)
    db.session.commit()
    return jsonify({"message": "Crédito eliminado correctamente"})
