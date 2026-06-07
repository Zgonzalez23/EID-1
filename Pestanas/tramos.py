import streamlit as st
from Logicas.logica_tramos import generar_datos_tramos
from utilidades import comparar_limite, comparar_valores

def renderizar_pestana_tramos(res):
    datos = generar_datos_tramos(res['cuerpo'], res['dv_ingresado'])
    
    st.header("1. Regla de Selección")
    st.info(datos['regla'])
    st.write(f"Punto crítico de análisis: **a = {datos['a']}**")
    
    st.header("2. Función Generada")
    st.latex(datos['formula_latex'])
    
    st.header("3. Evidencia Computacional")
    st.write("Tabla de valores cercanos al punto de análisis:")
    st.table(datos['tabla_valores'])
    
    st.header("4. Representación Gráfica")
    st.plotly_chart(datos['figura'], use_container_width=True)
    
    st.markdown("---")
    st.header("5. Análisis Matemático (Defensa Oral)")
    st.write("Completa los siguientes campos basándote en el análisis de límites laterales:")
    
    col1, col2 = st.columns(2)
    with col1:
        user_lim_izq = st.text_input("Límite por la izquierda (lim x -> a-):", key="lim_izq", placeholder="Ej: 5 o -infinito")
        user_conc_lim = st.selectbox("Conclusión sobre la existencia del límite bilateral:", ["", "Sí, existe", "No, no existe"], key="conc_lim")
        user_conc_cont = st.selectbox("Conclusión sobre continuidad:", ["", "Sí, es continua", "No, es discontinua"], key="conc_cont")
    with col2:
        user_lim_der = st.text_input("Límite por la derecha (lim x -> a+):", key="lim_der", placeholder="Ej: 5 o +infinito")
        user_fa_existe_sel = st.selectbox("Valor de la función f(a):", ["", "Existe", "No existe / Indefinido"], key="fa_existe")
        if user_fa_existe_sel == "Existe":
            user_val_fa = st.text_input("Ingresa el valor de f(a):", key="val_fa_input")
        else:
            user_val_fa = ""
        user_tipo_disc = st.selectbox("Tipo de discontinuidad:", ["", "Removible (Evitable)", "Salto (Finito)", "Infinita (Asintótica)"], key="tipo_disc")
        
    st.markdown("#### Resultados de la Validación en tiempo real:")
    status_lim_izq = comparar_limite(user_lim_izq, datos['lim_izq_exacto'])
    status_lim_der = comparar_limite(user_lim_der, datos['lim_der_exacto'])
    
    status_conc_lim = "✅ Correcto" if user_conc_lim == datos['lim_bilateral_existe'] else ("⚠️ Vacío" if not user_conc_lim else "❌ Incorrecto")
    status_cont = "✅ Correcto" if user_conc_cont == "No, es discontinua" else ("⚠️ Vacío" if not user_conc_cont else "❌ Incorrecto")
    
    if not user_fa_existe_sel:
        status_fa = "⚠️ Vacío"
    elif user_fa_existe_sel == datos['fa_existe']:
        if user_fa_existe_sel == "Existe":
            status_fa = comparar_valores(user_val_fa, datos['fa_exacto'])
        else:
            status_fa = "✅ Correcto"
    else:
        status_fa = "❌ Incorrecto"
        
    status_disc = "✅ Correcto" if user_tipo_disc == datos['tipo_discontinuidad'] else ("⚠️ Vacío" if not user_tipo_disc else "❌ Incorrecto")
    
    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.write(f"- **Límite por la izquierda:** {status_lim_izq}")
        st.write(f"- **Existencia del límite:** {status_conc_lim}")
        st.write(f"- **Continuidad:** {status_cont}")
    with vcol2:
        st.write(f"- **Límite por la derecha:** {status_lim_der}")
        st.write(f"- **Valor f(a):** {status_fa}")
        st.write(f"- **Tipo de discontinuidad:** {status_disc}")
        
    st.text_area("Justificación escrita del comportamiento observado:", key="justificacion", placeholder="Escribe aquí tu análisis para preparar la defensa oral...")
 
    with st.expander("Ver Justificación Matemática y Desarrollo de Límites Laterales"):
        st.subheader("Desarrollo de Límites Paso a Paso")
        st.write(f"Análisis matemático para el punto crítico $a = {datos['a']}$:")
        
        if datos['residuo'] == 0:
            st.write("Dado que el residuo es 0, la función simplificada es racional con un factor común:")
            st.latex(rf"f(x) = \frac{{(x - {datos['a']})(x + {res['cuerpo'][0]})}}{{x - {datos['a']}}}")
            st.write("Calculamos los límites laterales para $x \\neq a$ simplificando la expresión:")
            st.latex(rf"\lim_{{x \to {datos['a']}^-}} f(x) = \lim_{{x \to {datos['a']}^-}} (x + {res['cuerpo'][0]}) = {datos['a']} + {res['cuerpo'][0]} = {datos['lim_izq_exacto']}")
            st.latex(rf"\lim_{{x \to {datos['a']}^+}} f(x) = \lim_{{x \to {datos['a']}^+}} (x + {res['cuerpo'][0]}) = {datos['a']} + {res['cuerpo'][0]} = {datos['lim_der_exacto']}")
            st.markdown(rf"""
            Dado que ambos límites laterales son iguales y finitos:
            $$\lim_{{x \to {datos['a']}}} f(x) = {datos['lim_izq_exacto']}$$
            Sin embargo, la función en el punto $x = {datos['a']}$ no está definida:
            $$f({datos['a']}) = \frac{{0}}{{0}} \quad (\text{{Indefinido}})$$
            Como el límite existe pero la función no está definida, corresponde a una **Discontinuidad Removible (Evitable)**.
            """)
        elif datos['residuo'] == 1:
            st.write("Dado que el residuo es 1, la función se define por tramos lineales:")
            st.latex(datos['formula_latex'])
            st.write("Calculamos los límites laterales evaluando en el tramo correspondiente:")
            st.latex(rf"\lim_{{x \to {datos['a']}^-}} f(x) = \lim_{{x \to {datos['a']}^-}} (x + {res['cuerpo'][1]}) = {datos['a']} + {res['cuerpo'][1]} = {datos['lim_izq_exacto']}")
            st.latex(rf"\lim_{{x \to {datos['a']}^+}} f(x) = \lim_{{x \to {datos['a']}^+}} (x + {res['cuerpo'][3]}) = {datos['a']} + {res['cuerpo'][3]} = {datos['lim_der_exacto']}")
            st.markdown(rf"""
            Dado que los límites laterales son finitos pero distintos:
            $$\lim_{{x \to {datos['a']}^-}} f(x) \neq \lim_{{x \to {datos['a']}^+}} f(x)$$
            El límite bilateral $\lim_{{x \to {datos['a']}}} f(x)$ **no existe**.
            El valor de la función en el punto es:
            $$f({datos['a']}) = {datos['a']} + {res['cuerpo'][3]} = {datos['fa_exacto']}$$
            Como los límites laterales existen pero son diferentes, corresponde a una **Discontinuidad de Salto (Finito)**.
            El tamaño del salto es:
            $$\text{{Salto}} = |{datos['lim_der_exacto']} - {datos['lim_izq_exacto']}| = {abs(datos['lim_der_exacto'] - datos['lim_izq_exacto'])}$$
            """)
        elif datos['residuo'] == 2:
            st.write("Dado que el residuo es 2, la función presenta una asíntota vertical:")
            num_val = int(res['cuerpo'][4]) + 1
            st.latex(rf"f(x) = \frac{{{num_val}}}{{x - {datos['a']}}}")
            st.write("Calculamos los límites laterales analizando el signo del denominador:")
            st.latex(rf"\lim_{{x \to {datos['a']}^-}} \frac{{{num_val}}}{{x - {datos['a']}}} = -\infty")
            st.latex(rf"\lim_{{x \to {datos['a']}^+}} \frac{{{num_val}}}{{x - {datos['a']}}} = +\infty")
            st.markdown(rf"""
            Dado que los límites laterales tienden a infinito, la recta $x = {datos['a']}$ is una **asíntota vertical**.
            La función en el punto no está definida:
            $$f({datos['a']}) = \frac{{{num_val}}}{{0}} \quad (\text{{Indefinido}})$$
            Por lo tanto, la función presenta una **Discontinuidad Infinita (Asintótica)**.
            """)
