import streamlit as st

from logica_rut import validar_rut
from logica_conicas import generar_conica, graficar_conica
from utilidades import formato_num, formato_signo, formato_primer_signo
from logica_tramos import generar_datos_tramos

def renderizar_pestana_rut(res):
    st.subheader("Validación del Módulo 11 (Paso a Paso)")
    st.write(f"**RUT:** `{res['cuerpo_crudo']}-{res['dv_ingresado']}`")
    st.write(f"**Cuerpo ajustado:** `{res['cuerpo']}` | **DV ingresado:** `{res['dv_ingresado']}`")
    
    pasos_str = r" \quad ".join([f"{p['digito']} \\times {p['mult']} = {p['prod']}" for p in res['pasos']])
    st.latex(pasos_str)
    st.latex(rf"\text{{Suma}} = {res['suma']} \implies {res['suma']} \pmod{{11}} = {res['mod11']}")
    st.latex(rf"11 - {res['mod11']} = {res['dv_calculado_num']}")
    st.info(res['regla'])
    
    st.success("El RUT es Válido.")
    
    st.subheader("Dígitos Extraídos para Ecuaciones")
    columnas = st.columns(8)
    for indice, columna in enumerate(columnas):
        columna.metric(f"d{indice+1}", res['cuerpo'][indice])