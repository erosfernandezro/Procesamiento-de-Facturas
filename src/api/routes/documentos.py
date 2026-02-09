from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.extractor_service import ExtractorService
from app.utils.file_helper import extraer_texto_universal
from app.models.documento_db import DocumentoDB

# Definición del Blueprint con el prefijo /api
bp = Blueprint('documentos', __name__)
extractor = ExtractorService()

@bp.route('/v1/extraer', methods=['POST'])
def extraer_datos():
    # 1. Validar presencia del archivo
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Falta el archivo en la petición"}), 400
    
    file = request.files['file']
    
    # 2. Obtener sesión de base de datos (Inyección de dependencias manual)
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        # 3. Extraer texto según el formato (Usa EasyOCR para imágenes)
        texto_crudo = extraer_texto_universal(file)
        
        if not texto_crudo.strip():
            return jsonify({"status": "error", "message": "No se detectó texto en el documento"}), 422

        # 4. Procesar con IA (Llama 3.3 vía Groq con Few-Shot Prompting)
        documento_validado = extractor.procesar_documento(texto_crudo)
        
        # 5. Mapear a modelo de Base de Datos y Persistir (ORM)
        nueva_factura = DocumentoDB(
            emisor_denominacion=documento_validado.emisor.denominacion,
            emisor_cuit=documento_validado.emisor.cuit,
            emisor_cae=documento_validado.emisor.cae,
            emisor_fecha=documento_validado.emisor.fecha,
            monto_total=documento_validado.pago.monto_total,
            moneda=documento_validado.pago.moneda,
            numero=documento_validado.datos.numero,
            punto_venta=documento_validado.datos.punto_venta,
            tipo=documento_validado.datos.tipo,
            objetivo=documento_validado.objetivo,
            producto=documento_validado.producto
        )
        
        db.add(nueva_factura)
        db.commit()
        db.refresh(nueva_factura)

        # 6. Respuesta exitosa
        return jsonify({
            "status": "success",
            "db_id": nueva_factura.id,
            "data": documento_validado.model_dump()
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({
            "status": "error", 
            "message": f"Error procesando {file.filename}: {str(e)}"
        }), 422
    finally:
        db.close()