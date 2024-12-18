from createdb import *
import json
from sqlalchemy.orm import Session
from sqlalchemy import select


def agregar_tarea(titulo, descripcion):
    try:
        if not titulo:
            raise ValueError("El título de la tarea es obligatorio.")
        if not descripcion:
            raise ValueError("La descripción de la tarea es obligatoria.")

        with session.no_autoflush:  # Evita que se haga flush antes de tiempo
            nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
            session.add(nueva_tarea)
            session.commit()
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        session.close()


def listar_tareas():
    stmt = select(Tarea)
    result = session.execute(stmt)
    return result.scalars().all()

def marcar_completada(tarea_id):
    tarea = session.query(Tarea).filter_by(id=tarea_id).first()
    if tarea:
        tarea.completada = True
        session.commit()

def eliminar_tarea(tarea_id):
    tarea = session.query(Tarea).filter_by(id= tarea_id).first()
    if tarea: # verificar que la tarea existe
        session.delete(tarea)
        session.commit()
    else:
        print(f"No se encontro tarea con id {tarea_id}")

# Guardar y cargar tareas

def exportar_tareas(archivo):
    tareas = listar_tareas()
    with open(archivo, 'w') as f:
            json.dump(
            [{"id": tarea.id, "titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada} for tarea in tareas],
            f,
            indent=4
        )


def import_tareas(archivo):
    try:
        # Cargar las tareas desde el archivo JSON
        with open(archivo, 'r') as f:
            tareas = json.load(f)

        # Contador para rastrear tareas importadas
        tareas_importadas = 0

        # Crear una nueva sesión usando Session
        with Session() as nueva_sesion:  # Context manager para manejar la sesión
            try:
                for tarea in tareas:
                    # Verificar si existe una tarea con el mismo título y descripción
                    tarea_existente = nueva_sesion.query(Tarea).filter_by(
                        titulo=tarea['titulo'], descripcion=tarea['descripcion']
                    ).first()

                    if not tarea_existente:
                        nueva_tarea = Tarea(
                            titulo=tarea['titulo'], 
                            descripcion=tarea['descripcion']
                        )
                        nueva_sesion.add(nueva_tarea)
                        tareas_importadas += 1

                # Commit una sola vez después de procesar todas las tareas
                nueva_sesion.commit()
                print(f"Se importaron {tareas_importadas} tareas nuevas.")

            except Exception as e:
                nueva_sesion.rollback()
                print(f"Error durante la importación de tareas: {e}")

    except Exception as e:
        print(f"Error al abrir o procesar el archivo: {e}")

