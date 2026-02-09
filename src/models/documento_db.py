from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class DocumentoDB(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del Emisor (mapeados desde el modelo Pydantic)
    emisor_denominacion = Column(String)
    emisor_cuit = Column(String)
    emisor_cae = Column(String, nullable=True)
    emisor_fecha = Column(String)
    
    # Datos de Pago
    monto_total = Column(Float)
    moneda = Column(String, default="ARS")
    
    # Datos de Factura/Ticket
    numero = Column(String)
    punto_venta = Column(String)
    tipo = Column(String)
    
    # Información extraída por IA
    objetivo = Column(String)
    producto = Column(String)