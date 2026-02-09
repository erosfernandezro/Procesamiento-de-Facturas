from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
import re
from datetime import datetime

class TipoDocumento(str, Enum):
    FACTURA_A = "Factura A"
    FACTURA_B = "Factura B"
    FACTURA_C = "Factura C"
    TICKET = "Ticket"
    RECIBO = "Recibo"
    COMPROBANTE = "Comprobante de Pago"

class Emisor(BaseModel):
    denominacion: str
    cuit: str
    cae: Optional[str] = None
    fecha: str

    @field_validator('fecha')
    @classmethod
    def normalizar_fecha(cls, v: str):
        # Intenta convertir cualquier formato a YYYY-MM-DD
        formatos = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
        for fmt in formatos:
            try:
                return datetime.strptime(v, fmt).strftime("%Y-%m-%d")
            except:
                continue
        return v

    @field_validator('cuit')
    @classmethod
    def validar_cuit(cls, v: str):
        solo_numeros = re.sub(r'\D', '', v)
        if len(solo_numeros) != 11:
            raise ValueError('El CUIT debe tener 11 dígitos')
        return solo_numeros

class Pago(BaseModel):
    monto_total: float = Field(..., gt=0)
    moneda: str = "ARS"

class DatosFactura(BaseModel):
    numero: str
    punto_venta: str
    tipo: str

class Documento10X(BaseModel):
    emisor: Emisor
    pago: Pago
    datos: DatosFactura
    objetivo: str = Field(..., description="Receptor de la factura y sus datos")
    producto: str = Field(..., description="Detalle de prestaciones, leyes o lotes pagados")