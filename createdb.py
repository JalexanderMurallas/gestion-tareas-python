from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    descripcion = Column(String)
    completada = Column(Boolean, default=False)
    

engine = create_engine("sqlite:///tareas.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


