from flask import Flask, render_template, request
import requests

# Inicializa la aplicación Flask
app = Flask(__name__)

# Clave de API para el servicio de conversión de moneda
API_KEY = "03945ec511d2265974505851"
# URL base para la API de conversión de moneda
URL_BASE = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# Define la ruta principal de la aplicación
@app.route("/", methods=["GET", "POST"])
def index():
    conversion = None  # Variable para almacenar el resultado de la conversión
    error = None  # Variable para almacenar mensajes de error

    # Si el método de la solicitud es POST, se procesa el formulario
    if request.method == "POST":
        # Obtiene las monedas de origen y destino del formulario y las convierte a mayúsculas
        from_currency = request.form.get("from_currency").upper()
        to_currency = request.form.get("to_currency").upper()
        # Obtiene la cantidad a convertir del formulario, por defecto es 1
        amount = float(request.form.get("amount", 1))
        try:
            # Realiza una solicitud a la API para obtener las tasas de conversión
            response = requests.get(URL_BASE + from_currency)
            data = response.json()  # Convierte la respuesta a formato JSON
            if data.get("result") == "success":
                # Obtiene las tasas de conversión del JSON
                rates = data.get("conversion_rates", {})
                if to_currency in rates:
                    # Calcula la conversión si la moneda destino está en las tasas
                    rate = rates[to_currency]
                    conversion = round(amount * rate, 2)
                else:
                    # Error si la moneda destino no se encuentra
                    error = f"Moneda destino '{to_currency}' no encontrada."
            else:
                # Error si la API devuelve un resultado distinto de "success"
                error = f"Error de la API: {data.get('error-type', 'Desconocido')}"
        except Exception as e:
            # Manejo de excepciones generales
            error = f"Error: {str(e)}"

    # Renderiza la plantilla HTML con los resultados de la conversión o el error
    return render_template("index.html", conversion=conversion, error=error)

# Ejecuta la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)