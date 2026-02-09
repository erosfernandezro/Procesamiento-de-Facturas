#  Procesamiento Inteligente de Facturas y Documentos

Este proyecto es una solución automatizada para la extracción, validación y almacenamiento de datos fiscales a partir de diversos formatos (PDF, Imágenes, TXT). Combina la potencia de **IA Generativa (Llama 3.3)** con **OCR** y una arquitectura modular para garantizar precisión y seguridad.

---

##  Decisiones Técnicas y Herramientas

* **Flask**: Elegido por su simplicidad para actuar como un servidor que escucha peticiones de **n8n** y procesa archivos rápidamente.
* **n8n**: Utilizado como orquestador para gestionar el ingreso de archivos y la interfaz de usuario, simplificando el flujo de trabajo.
* **Llama 3.3 (vía Groq)**: Un motor de IA extremadamente rápido que permite una estructuración forzada de datos mediante JSON.
* **EasyOCR**: Integrado para procesar fotos y documentos escaneados **sin requerir instalaciones externas** adicionales en el sistema.
* **SQLAlchemy (ORM)**: Implementado para manejar la base de datos de forma segura, evitando inyecciones SQL y organizando la persistencia de datos.
* **Pydantic**: Utilizado para la limpieza y normalización estricta de datos (ej. convertir importes monetarios y estandarizar fechas a `YYYY-MM-DD`).
* **PyPDF2**: Librería robusta para la extracción directa de texto en documentos digitales.

---

##  Descripción del Flujo

### 1. Entrada (Input)

El flujo se activa en **n8n**, que monitorea el ingreso de documentos a través de un formulario web o integración directa.

### 2. Procesamiento (Cerebro)

El servidor Flask recibe los archivos en el puerto `5000` bajo la ruta `/api/v1/extraer` y ejecuta tres pasos críticos:

* **Extracción de Texto**: Se extrae el contenido bruto del archivo (PDF, JPG, PNG o TXT).
* **Razonamiento y Few-Shot**: Se envía el texto a **Groq** junto con ejemplos de éxito previos para guiar a la IA en la identificación de campos clave (CUIT, Montos, Fechas).
* **Validación y Limpieza**: **Pydantic** asegura que la información sea consistente antes de entrar a la base de datos (ej. validación de 11 dígitos para el CUIT).

### 3. Salida (Output)

* **Persistencia**: Los datos se insertan automáticamente en una base de datos local `prod.db` mediante el ORM.
* **Confirmación**: El sistema devuelve un objeto JSON a **n8n** para confirmar que la información está segura y lista para su uso.

---

##  Ejecución y Configuración

### Requisitos

* Python 3.10+ e instalación de `requirements.txt`.
* Archivo `.env` en la raíz con tu `GROQ_API_KEY`.

### Pasos

1. **Instalar dependencias**:
```bash
pip install -r requirements.txt

```


2. **Iniciar el servidor**:
```bash
python -m app.main

```


3. **Procesar**: Ejecuta el flujo en **n8n**, carga tus archivos y visualiza los resultados en el archivo SQLite generado.

> **Visualización**: Puedes usar [SQLite Viewer](https://inloop.github.io/sqlite-viewer/) para arrastrar tu archivo `.db` y ver los datos organizados.

---

##  Evolución y Mejoras (Feedback Incorporado)

Este proyecto ha sido optimizado siguiendo estándares profesionales:

* **Arquitectura Modular**: El código se dividió en `/api`, `/models`, `/services` y `/db` para mejorar la legibilidad y mantenimiento.
* **Seguridad de Datos**: Se migró de SQL puro a un **ORM**, eliminando riesgos de seguridad y desacoplando la creación de tablas de la lógica de guardado.
* **Robustez de IA**: Se implementó **Few-Shot Learning** en los prompts para reducir "alucinaciones" y mejorar la precisión en tickets o fotos borrosas.
* **Logging**: Se utiliza `logging` para registrar movimientos y fallos, facilitando la auditoría de procesos fallidos.

---

**Desarrollado por Eros Fernandez Romero**
