# pjecz-plataforma-web-cli

Interfaz de Linea de Comando hecho en Typer/Python para consultar Plataforma Web.

## Instalar software adicional

En Fedora Linux agregue este software

```bash
sudo dnf -y groupinstall "Development Tools"
sudo dnf -y install glibc-langpack-en glibc-langpack-es
sudo dnf -y install pipenv poetry python3-virtualenv
sudo dnf -y install python3-devel python3-docs python3-idle
sudo dnf -y install python3.11
```

## Configuirar Poetry

Por defecto, con **poetry** el entorno se guarda en un directorio en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

```bash
poetry config --list
poetry config virtualenvs.in-project true
```

Verifique que este en True

```bash
poetry config virtualenvs.in-project
```

## Instalar

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

## Configurar

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```ini
# API
API_KEY=XXXXXXXX.XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXX
HOST=http://localhost:8002
LIMIT=100
TIMEOUT=20
SLEEP=2

# SENDGRID
SENDGRID_API_KEY=SG.XXXXXXXXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SENDGRID_FROM_EMAIL=remitente@pjecz.gob.mx

# SIGA rutas en el servidor Justicia
SIGA_JUSTICIA_RUTA=/mnt/respaldos/siga
```

Crear un archivo `.bashrc` para activar el entorno virtual y cargar las variables de entorno:

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet Plataforma Web CLI
else
    echo "== Plataforma Web CLI"
fi
echo

if [ -f .env ]
then
    echo "-- Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   API_KEY: ${API_KEY}"
    echo "   SIGA_JUSTICIA_RUTA: ${SIGA_JUSTICIA_RUTA}"
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
    alias cli="python3 ${PWD}/plataforma_web/app.py"
    echo "-- Ejecutar el CLI"
    echo "   cli --help"
    echo
fi
```

## Ejecutar

Ejecute con el alias `cli`

```bash
cli --help
```
