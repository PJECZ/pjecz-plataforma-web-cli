"""
Command Line Interface
"""
import typer

from pjecz_plataforma_web_cli.distritos.app import app as distritos_app
from pjecz_plataforma_web_cli.materias.app import app as materias_app
from pjecz_plataforma_web_cli.oficinas.app import app as oficinas_app
from pjecz_plataforma_web_cli.roles.app import app as roles_app
from pjecz_plataforma_web_cli.usuarios.app import app as usuarios_app

app = typer.Typer()
app.add_typer(distritos_app, name="distritos")
app.add_typer(materias_app, name="materias")
app.add_typer(oficinas_app, name="oficinas")
app.add_typer(roles_app, name="roles")
app.add_typer(usuarios_app, name="usuarios")

if __name__ == "__main__":
    app()
