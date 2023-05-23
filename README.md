# pjecz-plataforma-web-cli

Interfaz de Linea de Comando hecho en Typer/Python para consultar Plataforma Web.

## Configuracion

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```ini
# API
API_KEY=XXXXXXXX.XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXX
HOST=http://localhost:8002
LIMIT=500
TIMEOUT=20

# SENDGRID
SENDGRID_API_KEY=SG.XXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SENDGRID_FROM_EMAIL=plataforma.web@pjecz.gob.mx
```

**NOTA:** En HOST **NO debe incluir** la ruta `/v3`

## Instalacion

En Fedora Linux agregue este software

    sudo dnf -y groupinstall "Development Tools"
    sudo dnf -y install glibc-langpack-en glibc-langpack-es
    sudo dnf -y install pipenv poetry python3-virtualenv
    sudo dnf -y install python3-devel python3-docs python3-idle
    sudo dnf -y install python3.11

Clone el repositorio

    cd ~/Documents/GitHub/PJECZ
    git clone https://github.com/PJECZ/pjecz-plataforma-web-cli.git
    cd pjecz-plataforma-web-cli

Instale el entorno virtual con **Python 3.11** y los paquetes necesarios

    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install wheel
    poetry install
