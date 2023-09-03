# 1. Introducción

A través de este proyecto es posible de manera automática subir un vídeo a la plataforma de streaming YouTube, para ello se ha utilizado la API de YouTube y el lenguaje de programación Python.

# 2. Instalación

## 2.1 Requisitos

Las siguientes herramientas son necesarias para el desarrollo y ejecución del proyecto:

- Python 3.8 (mínimo)
- Watchdog
- Google API Python Client

## 2.2 Instalación

## 2.2.1 Creación del entorno virtual

Para la instalación de las librerías necesarias se recomienda la creación de un entorno virtual, para ello se debe ejecutar el siguiente comando:

```bash
python -m venv env
```

### 2.2.2 Activación del entorno virtual

Para activar el entorno virtual se debe ejecutar el siguiente comando:

Linux/MacOS:

```bash
source env/bin/activate
```
Windows:
    
```bash
env\Scripts\activate.bat
```

### 2.2.3 Instalación de las librerías

Para instalar las librerías necesarias se debe ejecutar el siguiente comando:

```bash
pip install -r requirements.txt
```

# 3. Ejecución

Para ejecutar el proyecto se debe ejecutar el siguiente comando:

```bash
python main.py [ruta de la carpeta que contiene los vídeos]
```
