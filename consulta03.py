# Importación de librerías y clases necesarias
from sqlalchemy.orm import sessionmaker  # Para crear sesiones de base de datos
from sqlalchemy import func  # Para funciones de agregación como count()
from clases import engine, Estudiante, Tarea, Entrega, Curso  # Modelos de la base de datos

# Creación de la sesión de base de datos
Session = sessionmaker(bind=engine)  # Configura la sesión con el engine de la base de datos
session = Session()  # Crea una nueva sesión para ejecutar consultas

# 1. CONFIGURACIÓN INICIAL
# ------------------------------------------------------------
# Lista de estudiantes específicos que queremos buscar
estudiantes_buscar = ['Jennifer Bolton', 'Elaine Perez', 'Heather Henderson', 'Charles Harris']

# 2. CONSULTA PRINCIPAL
# ------------------------------------------------------------
# Consulta para obtener tareas de los estudiantes con conteo de entregas
query = (
    session.query(
        Estudiante.nombre.label('estudiante'),  # Nombre del estudiante (con alias)
        Tarea.titulo.label('tarea'),            # Título de la tarea (con alias)
        Curso.titulo.label('curso'),            # Título del curso (con alias)
        func.count(Entrega.id).label('entregas') # Conteo de entregas (con alias)
    )
    # Realiza joins entre las tablas:
    .join(Entrega, Entrega.estudiante_id == Estudiante.id)  # Relación Estudiante-Entrega
    .join(Tarea, Tarea.id == Entrega.tarea_id)             # Relación Entrega-Tarea
    .join(Curso, Curso.id == Tarea.curso_id)               # Relación Tarea-Curso
    # Filtra solo los estudiantes de nuestra lista:
    .filter(Estudiante.nombre.in_(estudiantes_buscar))
    # Agrupa los resultados para el conteo:
    .group_by(Estudiante.nombre, Tarea.titulo, Curso.titulo)
    # Ordena los resultados:
    .order_by(Estudiante.nombre, Curso.titulo, Tarea.titulo)
)

# 3. PRESENTACIÓN DE RESULTADOS PRINCIPALES
# ------------------------------------------------------------
# Encabezado de la tabla de resultados
print("Tareas asignadas a estudiantes con conteo de entregas:")
print("--------------------------------------------------")
# Formato de columnas con alineación y tamaño fijo
print(f"{'Estudiante':<20} | {'Curso':<25} | {'Tarea':<25} | Entregas")
print("-" * 85)  # Línea separadora

# Itera sobre los resultados de la consulta principal
for estudiante, tarea, curso, entregas in query:
    # Imprime cada fila con formato alineado
    print(f"{estudiante:<20} | {curso:<25} | {tarea:<25} | {entregas:>8}")

# 4. CONSULTA SECUNDARIA (TOTALES POR ESTUDIANTE)
# ------------------------------------------------------------
print("\nResumen de entregas por estudiante:")
print("---------------------------------")
# Subconsulta para obtener el total de entregas por estudiante
subquery = (
    session.query(
        Estudiante.nombre,  # Nombre del estudiante
        func.count(Entrega.id).label('total_entregas')  # Conteo total de entregas
    )
    .join(Entrega, Entrega.estudiante_id == Estudiante.id)  # Relación Estudiante-Entrega
    .filter(Estudiante.nombre.in_(estudiantes_buscar))  # Filtra los mismos estudiantes
    .group_by(Estudiante.nombre)  # Agrupa solo por estudiante
    .order_by(Estudiante.nombre)  # Ordena alfabéticamente
)

# Itera sobre los resultados de la subconsulta
for nombre, total in subquery:
    print(f"{nombre}: {total} entregas totales")  # Muestra el resumen por estudiante