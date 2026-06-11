import streamlit as st

def renderizar_pestana_rut(res):
    st.header("Validación del RUT mediante Módulo 11")

    col_info, col_dv = st.columns([2, 1])
    with col_info:
        st.markdown(f"**RUT ingresado:** `{res['cuerpo_crudo']}-{res['dv_ingresado']}`")
        st.markdown(f"**Cuerpo normalizado (8 dígitos):** `{res['cuerpo']}`")
        st.markdown(f"**DV ingresado:** `{res['dv_ingresado']}`")
    with col_dv:
        st.metric("DV calculado", res['dv_esperado'])
        st.metric("Valor auxiliar v", res['v_val'])

    st.subheader("Paso 1 — Inversión del cuerpo del RUT")
    st.write(
        f"El algoritmo trabaja con el cuerpo invertido: `{res['cuerpo_crudo']}` → `{res['invertido']}`"
    )

    st.subheader("Paso 2 — Multiplicación por factores cíclicos [2, 3, 4, 5, 6, 7]")
    pasos_str = r" \quad ".join(
        [f"{p['digito']} \\times {p['mult']} = {p['prod']}" for p in res['pasos']]
    )
    st.latex(pasos_str)

    st.subheader("Paso 3 — Suma total y módulo 11")
    productos = " + ".join([str(p['prod']) for p in res['pasos']])
    st.latex(rf"\text{{Suma}} = {productos} = {res['suma']}")
    st.latex(rf"{res['suma']} \mod 11 = {res['mod11']}")

    st.subheader("Paso 4 — Cálculo del DV esperado")
    st.latex(rf"11 - {res['mod11']} = {res['dv_calculado_num']}")
    st.info(f"📌 {res['regla']}")

    st.subheader("Paso 5 — Definición de la variable auxiliar v")
    st.markdown(
        "La variable **v** se usa para calcular los coeficientes de la ecuación general de la cónica:"
    )
    st.latex(
        r"v = \begin{cases} 10, & \text{si DV} = K \\ 11, & \text{si DV} = 0 \\ \text{DV}, & \text{si DV} \in \{1, 2, \ldots, 9\} \end{cases}"
    )
    st.success(f"Para este RUT: **v = {res['v_val']}**")

    st.divider()
    st.subheader("Dígitos extraídos para la construcción de la cónica")
    columnas = st.columns(8)
    for indice, columna in enumerate(columnas):
        columna.metric(f"d{indice + 1}", res['cuerpo'][indice])
