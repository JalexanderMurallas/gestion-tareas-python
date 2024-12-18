from funciones import *
import streamlit as st

try:
    st.title('Gestión de Tareas')

    # Inicializar el estado de Streamlit
    if 'mostrar_campos' not in st.session_state:
        st.session_state.mostrar_campos = False

    if 'tareas' not in st.session_state:
        st.session_state.tareas = listar_tareas()

    # Botón para agregar tarea
    if st.button('Agregar Tarea'):
        st.session_state.mostrar_campos = True

    # Mostrar los campos si el estado está activo
    if st.session_state.mostrar_campos:
        titulo = st.text_input('Título')
        descripcion = st.text_area('Descripción')

        # Botón para guardar la tarea
        if st.button('Guardar'):
            if titulo.strip():  # Validar que el título no esté vacío
                agregar_tarea(titulo, descripcion)
                st.success('Tarea agregada')
                st.session_state.mostrar_campos = False
                st.session_state.tareas = listar_tareas()  # Actualizar la lista de tareas
                st.rerun()  # Recargar la interfaz
            else:
                st.error("El título no puede estar vacío.")

    # Mostrar la lista de tareas
    st.subheader("Tareas")
    for tarea in st.session_state.tareas:
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"{tarea.id} - {tarea.titulo} - {'✅ Completada' if tarea.completada else 'Pendiente'}")

        # Botón para marcar como completada
        if not tarea.completada and col2.button('Completar', key=f"completar-{tarea.id}"):
            marcar_completada(tarea.id)
            st.session_state.tareas = listar_tareas()
            st.rerun()  # Recargar la interfaz

        # Botón para eliminar la tarea
        if col3.button('Eliminar', key=f"eliminar-{tarea.id}"):
            eliminar_tarea(tarea.id)
            st.session_state.tareas = listar_tareas()
            st.rerun()  # Recargar la interfaz

    # Exportar
    st.subheader("Exportar o importar JSON")

     # Botón para exportar tareas
    if st.button("Exportar Tareas a JSON"):
        archivo_exportado = "tareas_exportadas.json"
        exportar_tareas(archivo_exportado)
        st.success(f"Tareas exportadas correctamente a '{archivo_exportado}'.")

    # Botón para importar tareas
    archivo_subido = st.file_uploader("Selecciona un archivo JSON para importar tareas", type="json")
    if archivo_subido is not None:
        # Leer el archivo JSON y agregar tareas
        try:
            tareas_importadas = json.load(archivo_subido)
            for tarea in tareas_importadas:
                agregar_tarea(tarea['titulo'], tarea['descripcion'])
            listar_tareas()
            st.success("Tareas importadas correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al importar tareas: {e}")

except Exception as e:
    st.error(f"Ha ocurrido un error: {e}")
    print(e)
