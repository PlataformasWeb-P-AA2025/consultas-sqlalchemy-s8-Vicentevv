from sqlalchemy.orm import sessionmaker
from clases import engine, Entrega

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

print("\n--- ENTREGAS DE ESTUDIANTES EN EL DEPARTAMENTO DE ARTE ---")

# Consultar todas las entregas
entregas = session.query(Entrega).all()

# Consulta 1: Recorrer todas las entregas y filtrar las que pertenezcan al departamento "Arte"
for entrega in entregas:
    tarea = entrega.tarea
    curso = tarea.curso
    departamento = curso.departamento
    estudiante = entrega.estudiante
    instructor = curso.instructor

    if departamento.nombre == "Arte":
        print(f"Tarea: {tarea.titulo}, Estudiante: {estudiante.nombre}, "
              f"Calificación: {entrega.calificacion}, "
              f"Instructor: {instructor.nombre}, Departamento: {departamento.nombre}")
