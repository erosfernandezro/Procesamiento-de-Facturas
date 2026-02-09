import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from app.models.documento import Documento10X

load_dotenv()

class ExtractorService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Error: No se encontró la GROQ_API_KEY en el archivo .env")
            
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            model_kwargs={"response_format": {"type": "json_object"}}
        )

    def procesar_documento(self, texto: str) -> Documento10X:
        # FEW-SHOT: Ejemplos con DATOS INVENTADOS para guiar a la IA
        ejemplos_exitosos = [
            {
                "input": "SERVICIOS GLOBALES S.H. - CUIT: 30-99999999-9 - Factura B 0001-00004321. Fecha: 10/01/2026. Total: $15.200,00. Concepto: Mantenimiento de software. Cliente: Juan Pérez.",
                "output": {
                    "emisor": {
                        "denominacion": "SERVICIOS GLOBALES S.H.",
                        "cuit": "30999999999",
                        "cae": "12345678901234",
                        "fecha": "2026-01-10"
                    },
                    "pago": {
                        "monto_total": 15200.0,
                        "moneda": "ARS"
                    },
                    "datos": {
                        "numero": "00004321",
                        "punto_venta": "0001",
                        "tipo": "Factura B"
                    },
                    "objetivo": "Juan Pérez - Consumidor Final",
                    "producto": "Mantenimiento preventivo de software y limpieza de bases de datos."
                }
            },
            {
                "input": "TICKET FACTURA B - KIOSCO EL PASO - CUIT 20-11111111-2. Vta: 0005-00123. Fecha 15-02-2026. GOLOSINAS VARIAS $1.500. TOTAL $1.500.",
                "output": {
                    "emisor": {
                        "denominacion": "KIOSCO EL PASO",
                        "cuit": "20111111112",
                        "cae": None,
                        "fecha": "2026-02-15"
                    },
                    "pago": {
                        "monto_total": 1500.0,
                        "moneda": "ARS"
                    },
                    "datos": {
                        "numero": "00123",
                        "punto_venta": "0005",
                        "tipo": "Ticket"
                    },
                    "objetivo": "Público en general",
                    "producto": "Compra de golosinas y artículos de quiosco."
                }
            }
        ]

        prompt = f"""Eres un experto analista de documentos fiscales argentinos (Facturas, Tickets, Recibos).
        Tu tarea es extraer información precisa y devolverla en formato JSON.

        Sigue el estilo de estos ejemplos exitosos:

        EJEMPLO 1:
        Texto: {ejemplos_exitosos[0]['input']}
        Resultado: {json.dumps(ejemplos_exitosos[0]['output'])}

        EJEMPLO 2:
        Texto: {ejemplos_exitosos[1]['input']}
        Resultado: {json.dumps(ejemplos_exitosos[1]['output'])}

        DOCUMENTO ACTUAL A PROCESAR:
        {texto}

        REGLAS CRÍTICAS:
        1. El CUIT debe tener solo 11 dígitos numéricos.
        2. Si no encuentras el CAE, pon null.
        3. El campo 'objetivo' debe identificar al receptor.
        4. El campo 'producto' debe ser un resumen claro de los conceptos facturados.
        """
        
        res = self.llm.invoke(prompt)
        datos = json.loads(res.content)
        return Documento10X(**datos)