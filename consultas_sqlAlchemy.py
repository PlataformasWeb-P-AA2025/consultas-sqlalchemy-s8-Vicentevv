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
        
# Consulta 2: Obtener y mostrar todos los cursos
print("\n--- TODOS LOS CURSOS ---")
cursos = session.query(Curso).all()
for curso in cursos:
    print(curso.id, curso.titulo)  # Muestra el ID y título de cada curso

# Consulta 3: Mostrar los cursos que pertenecen al departamento con ID = 1 (CS)
print("\n--- CURSOS DEL DEPARTAMENTO CS (ID = 1) ---")
# Usamos Session.get para obtener el departamento por su ID y evitar el warning de legacy
departamento = session.get(Departamento, 1)
if departamento:
    for curso in departamento.cursos:
        print(curso.titulo)  # Muestra los títulos de los cursos del departamento CS
else:
    print("No se encontró el departamento con ID 1.")


# Consulta 5: Mostrar las inscripciones del estudiante 'Leslie Perez'
print("\n--- INSCRIPCIONES DE Leslie Perez ---")
estudiante = session.query(Estudiante).filter_by(nombre='Leslie Perez').first()
if estudiante:
    for insc in estudiante.inscripciones:
        print(insc.curso.titulo, insc.fecha_inscripcion)  # Muestra el curso y la fecha de inscripción
else:
    print("No se encontró al estudiante 'Leslie Perez'.")

# Consulta 6: Mostrar calificaciones de las entregas del estudiante con ID = 1
print("\n--- CALIFICACIONES DEL ESTUDIANTE CON ID 1 ---")
entregas = session.query(Entrega).filter_by(estudiante_id=1).all()
for entrega in entregas:
    print(entrega.tarea.titulo, entrega.calificacion)  # Muestra el título de la tarea y la calificación
