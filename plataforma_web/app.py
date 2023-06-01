"""
Command Line Interface
"""
import typer

from plataforma_web.autoridades.app import app as autoridades_app
from plataforma_web.centros_trabajos.app import app as centros_trabajos_app
from plataforma_web.distritos.app import app as distritos_app
from plataforma_web.domicilios.app import app as domicilios_app
from plataforma_web.edictos.app import app as edictos_app
from plataforma_web.funcionarios.app import app as funcionarios_app
from plataforma_web.inv_categorias.app import app as inv_categorias_app
from plataforma_web.inv_componentes.app import app as inv_componentes_app
from plataforma_web.inv_custodias.app import app as inv_custodias_app
from plataforma_web.inv_equipos.app import app as inv_equipos_app
from plataforma_web.inv_marcas.app import app as inv_marcas_app
from plataforma_web.inv_modelos.app import app as inv_modelos_app
from plataforma_web.inv_redes.app import app as inv_redes_app
from plataforma_web.listas_de_acuerdos.app import app as listas_de_acuerdos_app
from plataforma_web.materias.app import app as materias_app
from plataforma_web.materias_tipos_juicios.app import app as materias_tipos_juicios_app
from plataforma_web.modulos.app import app as modulos_app
from plataforma_web.oficinas.app import app as oficinas_app
from plataforma_web.permisos.app import app as permisos_app
from plataforma_web.roles.app import app as roles_app
from plataforma_web.sentencias.app import app as sentencias_app
from plataforma_web.siga_salas.app import app as siga_salas_app
from plataforma_web.usuarios.app import app as usuarios_app

app = typer.Typer()
app.add_typer(autoridades_app, name="autoridades")
app.add_typer(centros_trabajos_app, name="centros_trabajos")
app.add_typer(distritos_app, name="distritos")
app.add_typer(domicilios_app, name="domicilios")
app.add_typer(edictos_app, name="edictos")
app.add_typer(funcionarios_app, name="funcionarios")
app.add_typer(inv_categorias_app, name="inv_categorias")
app.add_typer(inv_componentes_app, name="inv_componentes")
app.add_typer(inv_custodias_app, name="inv_custodias")
app.add_typer(inv_equipos_app, name="inv_equipos")
app.add_typer(inv_marcas_app, name="inv_marcas")
app.add_typer(inv_modelos_app, name="inv_modelos")
app.add_typer(inv_redes_app, name="inv_redes")
app.add_typer(listas_de_acuerdos_app, name="listas_de_acuerdos")
app.add_typer(materias_app, name="materias")
app.add_typer(materias_tipos_juicios_app, name="materias_tipos_juicios")
app.add_typer(modulos_app, name="modulos")
app.add_typer(oficinas_app, name="oficinas")
app.add_typer(permisos_app, name="permisos")
app.add_typer(roles_app, name="roles")
app.add_typer(sentencias_app, name="sentencias")
app.add_typer(siga_salas_app, name="siga_salas")
app.add_typer(usuarios_app, name="usuarios")

if __name__ == "__main__":
    app()
