<a href="https://openweathermap.org/"><img height="120" align="right" src="https://upload.wikimedia.org/wikipedia/commons/1/15/OpenWeatherMap_logo.png"></a>

# 🌦️ Weather API - Prueba Técnica

Este proyecto es una API RESTful desarrollada con **Flask**, **PostgreSQL** y **OpenWeatherMap**, que permite:
- Obtener información del clima usando **OpenWeatherMap**.
- Gestionar leads almacenados en una base de datos PostgreSQL.
- Filtrar, ordenar y calcular presupuestos de los leads.
- Generar correos personalizados con IA usando prompts optimizados.

---

## 📥 Instalación

Este proyecto usa **Pipenv** para la gestión de dependencias. Para instalar los paquetes necesarios, ejecuta:

```sh
pipenv install
pipenv run migrate
pipenv run upgrade
pipenv run start
```

📌 **Nota:** Si estás trabajando en **Codespaces** o **Gitpod**, asegúrate de que tu puerto sea público para poder acceder a la API.

---

## 🌦️ API Utilizada - OpenWeatherMap

Se ha integrado la API de OpenWeatherMap para obtener información del clima.
Para usarla, es necesario contar con una **API Key**, que se puede obtener en [OpenWeatherMap](https://openweathermap.org/).

---

## 📌 Endpoints

### 🌤️ Obtener el clima
**GET** `/weather/<lat>/<lon>/<cnt>`

Obtiene el pronóstico del clima para una ubicación específica basada en **latitud**, **longitud** y cantidad de días.

#### 🔹 Ejemplo de uso:
```sh
curl -X GET "http://localhost:3000/weather/19.43/-99.13/5"
```

#### 🔹 Respuesta esperada:
```json
{
    "city": "Mexico City",
    "list": [
        {
            "dt_txt": "2024-02-08 12:00:00",
            "main": {
                "temp_max": 26.5,
                "temp_min": 14.2
            }
        }
    ]
}
```
---

### 💾 Guardar el día más caluroso
**POST** `/save_weather/<lat>/<lon>/<cnt>`

Guarda el día más caluroso en la base de datos para la ciudad consultada.

#### 🔹 Ejemplo de uso:
```sh
curl -X POST "http://localhost:3000/save_weather/19.43/-99.13/5"
```

#### 🔹 Respuesta esperada:
```json
{
    "message": "Día más caluroso guardado correctamente",
    "hottest_day": {
        "city_name": "Mexico City",
        "date": "2024-02-08 12:00:00",
        "temp_max": 26.5,
        "temp_min": 14.2
    }
}
```
---

### 🏡 Crear un lead
**POST** `/lead/create`

Crea un nuevo lead con nombre, ubicación y presupuesto.

#### 🔹 Ejemplo de uso:
```sh
curl -X POST "http://localhost:3000/lead/create" \
     -H "Content-Type: application/json" \
     -d '{
        "name": "Juan Pérez",
        "location": "Mexico City",
        "budget": 5000
     }'
```

#### 🔹 Respuesta esperada:
```json
{
    "msg": "Lead creado",
    "result": {
        "name": "Juan Pérez",
        "location": "MEXICO CITY",
        "budget": 5000
    }
}
```
---

### 🔍 Obtener leads por ciudad
**GET** `/lead/<city>`

Filtra y obtiene los leads de una ciudad específica, ordenados por presupuesto.

#### 🔹 Ejemplo de uso:
```sh
curl -X GET "http://localhost:3000/lead/Mexico City"
```

#### 🔹 Respuesta esperada:
```json
{
    "total_budget": 15000,
    "city": "Mexico City",
    "filtered_leads": [
        {
            "name": "Juan Pérez",
            "location": "MEXICO CITY",
            "budget": 5000
        }
    ]
}
```
---

## 📌 Generación de Correos con IA

Para estructurar correos amigables y profesionales, se ha diseñado un **prompt optimizado** para IA.

#### 🔹 Prompt utilizado:
```text
Formas parte de una constructora y vas a enviar un correo amable y profesional a un cliente para presentarle una oferta que podría interesarle.

Estructura del correo:
- Asunto: Una oferta especial para ti, {nombre}.
- Saludo cordial y una introducción amigable.
- Presentación de la oferta adaptada al presupuesto del cliente y el lugar en el que está ubicado.
- Beneficios clave que obtendría con esta oportunidad.
- Cierre amigable pero formal, invitándolo a conocer más detalles.

Asegúrate de que el tono sea cercano, pero manteniendo la formalidad.
```

#### 🔹 Ejemplo de salida generada:
**Para un lead con los siguientes datos:**
- **Nombre:** Jorge Suárez
- **Ubicación:** Medellín
- **Presupuesto:** 130 millones

**Correo generado:**
```text
Asunto: Una oferta especial para ti, Jorge

Hola Jorge,

Esperamos que estés teniendo un excelente día. Queremos contarte que en Medellín tenemos opciones ideales para ti.

Con tu presupuesto de 130 millones de pesos, podemos ofrecerte una excelente oportunidad que se adapta a tus necesidades.

Nos encantaría brindarte más información y asesorarte en tu decisión. ¿Podemos agendar una llamada esta semana?

Saludos,  
[Tu Nombre]  
[Tu Empresa]
```

---

## 🚀 Tecnologías Utilizadas

- **Flask**: Framework web para Python.
- **PostgreSQL**: Base de datos relacional.
- **OpenWeatherMap**: API de clima.
- **Pipenv**: Gestión de dependencias.
- **Flask-Migrate**: Manejo de migraciones de base de datos.

---

📌 **Autor:** Nicolle Rodríguez Laytón


¡Gracias por revisar este proyecto! 🌍✨

