"""
Command Line Interface
"""
import typer

from pjecz_plataforma_web_cli.autoridades.app import app as autoridades_app
from pjecz_plataforma_web_cli.centros_trabajos.app import app as centros_trabajos_app
from pjecz_plataforma_web_cli.distritos.app import app as distritos_app
from pjecz_plataforma_web_cli.domicilios.app import app as domicilios_app
from pjecz_plataforma_web_cli.materias.app import app as materias_app
from pjecz_plataforma_web_cli.materias_tipos_juicios.app import app as materias_tipos_juicios_app
from pjecz_plataforma_web_cli.modulos.app import app as modulos_app
from pjecz_plataforma_web_cli.oficinas.app import app as oficinas_app
from pjecz_plataforma_web_cli.permisos.app import app as permisos_app
from pjecz_plataforma_web_cli.roles.app import app as roles_app
from pjecz_plataforma_web_cli.usuarios.app import app as usuarios_app

app = typer.Typer()
app.add_typer(autoridades_app, name="autoridades")
app.add_typer(centros_trabajos_app, name="centros_trabajos")
app.add_typer(distritos_app, name="distritos")
app.add_typer(domicilios_app, name="domicilios")
app.add_typer(materias_app, name="materias")
app.add_typer(materias_tipos_juicios_app, name="materias_tipos_juicios")
app.add_typer(modulos_app, name="modulos")
app.add_typer(oficinas_app, name="oficinas")
app.add_typer(permisos_app, name="permisos")
app.add_typer(roles_app, name="roles")
app.add_typer(usuarios_app, name="usuarios")

if __name__ == "__main__":
    app()
