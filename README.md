# pjecz-plataforma-web-cli

Interfaz de Linea de Comando hecho en Typer/Python para consultar Plataforma Web.

## Configuracion

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```ini
# API
API_KEY=XXXXXXXX.XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXX
HOST=https://datos.justiciadigital.gob.mx
LIMIT=100
TIMEOUT=20

# SENDGRID
SENDGRID_API_KEY=SG.XXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SENDGRID_FROM_EMAIL=remitente@pjecz.gob.mx
```

Crear un archivo `.bashrc` para activar el entorno virtual y cargar las variables de entorno:

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if [ -f .env ]
then
    echo "-- Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   API_KEY: ${API_KEY}"
    echo "   HOST: ${HOST}"
    echo "   LIMIT: ${LIMIT}"
    echo "   TIMEOUT: ${TIMEOUT}"
    echo "   SLEEP: ${SLEEP}"
    echo "   SENDGRID_API_KEY: ${SENDGRID_API_KEY}"
    echo "   SENDGRID_FROM_EMAIL: ${SENDGRID_FROM_EMAIL}"
    echo
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    alias cli="python3 ${PWD}/pjecz_plataforma_web_cli/app.py"
    echo "-- Ejecutar el CLI"
    echo "   cli --help"
    echo
fi
```

## Instalacion

En Fedora Linux agregue este software

```bash
sudo dnf -y groupinstall "Development Tools"
sudo dnf -y install glibc-langpack-en glibc-langpack-es
sudo dnf -y install pipenv poetry python3-virtualenv
sudo dnf -y install python3-devel python3-docs python3-idle
sudo dnf -y install python3.11
```

Clone el repositorio

```bash
cd ~/Documents/GitHub/PJECZ
git clone https://github.com/PJECZ/pjecz-plataforma-web-cli.git
cd pjecz-plataforma-web-cli
```

Instale el entorno virtual con **Python 3.11** y los paquetes necesarios

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install wheel
poetry install
```
