# Consulta 02
# 2. Todos los departamentos que tengan notas de entregas menores o iguales a 0.3 . En función de los departamentos, presentar el nombre del departamento y el número de cursos que tiene cada departamento

from sqlalchemy.orm import sessionmaker
from clases import engine, Entrega

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

departamentos = session.query(Departamento)

entregas = session.query(Entrega).all()
