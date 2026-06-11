import streamlit as st
from logicas.logica_rut import validar_rut
from pestanas.rut import renderizar_pestana_rut
from pestanas.conicas import renderizar_pestana_conica
from pestanas.tramos import renderizar_pestana_tramos

def main():
    st.set_page_config(
        page_title="EID-1 | Cónicas y Límites desde el RUT",
        page_icon="📐",
        layout="wide"
    )

    st.title("📐 Análisis de Cónicas y Funciones por Tramos desde el RUT")
    st.caption("MAT1186 - Introducción al Cálculo | Universidad Católica de Temuco")
    st.divider()

    rut_ingresado = st.text_input(
        "Ingrese un RUT chileno válido para iniciar el análisis:",
        placeholder="Ej: 12.345.678-9 o 12345678-9",
        help="El RUT debe tener entre 7 y 8 dígitos en el cuerpo, seguido de un guión y el dígito verificador (0-9 o K)."
    )

    if not rut_ingresado:
        st.info("👆 Ingresa un RUT válido para comenzar el análisis completo.")
        return

    es_valido, res, error = validar_rut(rut_ingresado)

    if error:
        st.error(f"❌ Error de formato: {error}")
        return

    if not es_valido:
        st.error(
            f"❌ RUT inválido: el dígito verificador ingresado es **{res['dv_ingresado']}**, "
            f"pero el esperado para el cuerpo **{res['cuerpo_crudo']}** es **{res['dv_esperado']}**."
        )
        return

    st.success(f"✅ RUT **{res['cuerpo_crudo']}-{res['dv_ingresado']}** validado correctamente.")
    st.divider()

    pestana1, pestana2, pestana3 = st.tabs([
        "📋 1. Validación de RUT",
        "🔷 2. Análisis de Cónicas",
        "📈 3. Función por Tramos"
    ])

    with pestana1:
        renderizar_pestana_rut(res)

    with pestana2:
        renderizar_pestana_conica(res)

    with pestana3:
        renderizar_pestana_tramos(res)

if __name__ == '__main__':
    main()
