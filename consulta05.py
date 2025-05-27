from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from clases import engine, Curso, Entrega, Tarea

Session = sessionmaker(bind=engine)
session = Session()

# 5.1 Obtener todos los cursos
cursos = session.query(Curso).order_by(Curso.titulo).all()

print("Promedio de calificaciones por curso:")
print("------------------------------------")
print(f"{'Curso':<30} | {'Promedio':<10} | {'Entregas':<8}")
print("-" * 60)

# 5.2 Ciclo para obtener entregas y promedios por cada curso
for curso in cursos:
    # Consulta para obtener el promedio y conteo de entregas del curso
    resultado = (
        session.query(
            func.avg(Entrega.calificacion).label('promedio'),
            func.count(Entrega.id).label('total_entregas')
        )
        .join(Tarea, Tarea.id == Entrega.tarea_id)
        .filter(Tarea.curso_id == curso.id)
        .first()
    )
    
    promedio = resultado.promedio if resultado.promedio is not None else 0
    total_entregas = resultado.total_entregas if resultado.total_entregas is not None else 0
    
    print(f"{curso.titulo:<30} | {promedio:.2f}{'':<8} | {total_entregas:>8}")

