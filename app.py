import streamlit as st
from Logicas.logica_rut import validar_rut
from pestanas.rut import renderizar_pestana_rut
from pestanas.conicas import renderizar_pestana_conica
from pestanas.tramos import renderizar_pestana_tramos

def main():
    st.set_page_config(page_title="Análisis RUT & Cónicas", layout="wide")
    st.title("Proyecto Python: Análisis de RUT, Cónicas y Funciones")
    
    rut_ingresado = st.text_input("Ingrese un RUT chileno para iniciar el análisis:", placeholder="Ej: 12.345.678-9")
    
    if rut_ingresado:
        es_valido, res, error = validar_rut(rut_ingresado)
        
        if error:
            st.error(error)
            return
            
        if es_valido:
            pestana1, pestana2, pestana3 = st.tabs(["1. Validación de RUT", "2. Análisis de Cónicas", "3. Función por Tramos"])
            
            with pestana1:
                renderizar_pestana_rut(res)
                
            with pestana2:
                renderizar_pestana_conica(res)
                
            with pestana3:
                renderizar_pestana_tramos(res)
        else:
            st.error("El RUT ingresado es INVÁLIDO. El dígito verificador no coincide.")

if __name__ == '__main__':
    main()
