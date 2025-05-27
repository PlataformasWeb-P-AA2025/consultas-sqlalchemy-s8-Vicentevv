from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from clases import engine, Departamento, Curso, Entrega, Tarea

Session = sessionmaker(bind=engine)
session = Session()

# Subconsulta para obtener departamentos con entregas <= 0.3
deptos_con_bajas_calif = (
    session.query(distinct(Departamento.id))
    .join(Curso, Curso.departamento_id == Departamento.id)
    .join(Tarea, Tarea.curso_id == Curso.id)
    .join(Entrega, Entrega.tarea_id == Tarea.id)
    .filter(Entrega.calificacion <= 0.3)
).subquery()

# Consulta principal que cuenta cursos por departamento (solo los que cumplen el criterio)
query = (
    session.query(
        Departamento.nombre,
        func.count(distinct(Curso.id)).label('num_cursos')
    )
    .join(Curso, Curso.departamento_id == Departamento.id)
    .filter(Departamento.id.in_(deptos_con_bajas_calif))
    .group_by(Departamento.id)
    .order_by(Departamento.nombre)
)

# Ejecución y presentación de resultados
print("Departamentos con entregas de calificación <= 0.3:")
for nombre, num_cursos in query:
    print(f"{nombre}: {num_cursos} cursos")