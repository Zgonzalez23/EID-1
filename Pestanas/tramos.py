import streamlit as st
from logicas.logica_tramos import generar_datos_tramos
from utilidades import comparar_limite, comparar_valores

def renderizar_pestana_tramos(res):
    datos = generar_datos_tramos(res['cuerpo'], res['dv_ingresado'])

    st.header("Análisis de Funciones por Tramos")

    st.subheader("1. Regla de Selección del Caso")
    st.info(datos['regla'])

    col_a, col_caso = st.columns(2)
    with col_a:
        st.metric("Punto crítico de análisis", f"a = {datos['a']}")
    with col_caso:
        st.metric("Tipo de discontinuidad esperado", datos['caso'])

    st.subheader("2. Función Generada")
    st.latex(datos['formula_latex'])

    st.subheader("3. Evidencia Computacional — Tabla de valores")
    st.write(
        "La siguiente tabla muestra los valores de la función al aproximarse al punto crítico "
        f"**a = {datos['a']}** por ambos lados:"
    )
    st.table(datos['tabla_valores'])

    st.subheader("4. Representación Gráfica")
    st.plotly_chart(datos['figura'], use_container_width=True)

    st.divider()
    st.subheader("5. Análisis Matemático — Módulo de Defensa Oral")
    st.warning(
        "⚠️ Los siguientes campos deben completarse **manualmente** durante la defensa oral, "
        "demostrando comprensión del análisis de límites. No vienen pre-completados."
    )

    col1, col2 = st.columns(2)
    with col1:
        user_lim_izq = st.text_input(
            f"Límite por la izquierda — lím (x → {datos['a']}⁻) f(x):",
            key="lim_izq",
            placeholder="Ej: 5  o  -infinito"
        )
        user_conc_lim = st.selectbox(
            "Conclusión sobre la existencia del límite bilateral:",
            ["", "Sí, existe", "No, no existe"],
            key="conc_lim"
        )
        user_conc_cont = st.selectbox(
            "Conclusión sobre continuidad en x = a:",
            ["", "Sí, es continua", "No, es discontinua"],
            key="conc_cont"
        )
    with col2:
        user_lim_der = st.text_input(
            f"Límite por la derecha — lím (x → {datos['a']}⁺) f(x):",
            key="lim_der",
            placeholder="Ej: 5  o  +infinito"
        )
        user_fa_existe_sel = st.selectbox(
            "¿Existe f(a)?",
            ["", "Existe", "No existe / Indefinido"],
            key="fa_existe"
        )
        if user_fa_existe_sel == "Existe":
            user_val_fa = st.text_input("Valor de f(a):", key="val_fa_input")
        else:
            user_val_fa = ""
        user_tipo_disc = st.selectbox(
            "Tipo de discontinuidad:",
            ["", "Removible (Evitable)", "Salto (Finito)", "Infinita (Asintótica)"],
            key="tipo_disc"
        )

    user_justificacion = st.text_area(
        "Justificación escrita del comportamiento observado:",
        key="justificacion",
        height=120,
        placeholder=(
            "Ejemplo: 'El límite por la izquierda es igual al límite por la derecha, "
            "ambos valen __. Sin embargo, la función no está definida en x = a porque __ . "
            "Por lo tanto, existe una discontinuidad de tipo __ en ese punto...'"
        )
    )

    st.markdown("#### Resultados de la Validación en tiempo real:")
    status_lim_izq = comparar_limite(user_lim_izq, datos['lim_izq_exacto'])
    status_lim_der = comparar_limite(user_lim_der, datos['lim_der_exacto'])

    status_conc_lim = (
        "✅ Correcto" if user_conc_lim == datos['lim_bilateral_existe']
        else ("⚠️ Vacío" if not user_conc_lim else "❌ Incorrecto")
    )
    status_cont = (
        "✅ Correcto" if user_conc_cont == "No, es discontinua"
        else ("⚠️ Vacío" if not user_conc_cont else "❌ Incorrecto")
    )

    if not user_fa_existe_sel:
        status_fa = "⚠️ Vacío"
    elif user_fa_existe_sel == datos['fa_existe']:
        if user_fa_existe_sel == "Existe":
            status_fa = comparar_valores(user_val_fa, datos['fa_exacto'])
        else:
            status_fa = "✅ Correcto"
    else:
        status_fa = "❌ Incorrecto"

    status_disc = (
        "✅ Correcto" if user_tipo_disc == datos['tipo_discontinuidad']
        else ("⚠️ Vacío" if not user_tipo_disc else "❌ Incorrecto")
    )

    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.write(f"- **Límite por la izquierda:** {status_lim_izq}")
        st.write(f"- **Existencia del límite:** {status_conc_lim}")
        st.write(f"- **Continuidad:** {status_cont}")
    with vcol2:
        st.write(f"- **Límite por la derecha:** {status_lim_der}")
        st.write(f"- **Valor f(a):** {status_fa}")
        st.write(f"- **Tipo de discontinuidad:** {status_disc}")

    with st.expander("📖 Ver Justificación Matemática y Desarrollo Paso a Paso"):
        st.subheader("Desarrollo de Límites Paso a Paso")
        st.write(f"Análisis matemático para el punto crítico $a = {datos['a']}$:")

        if datos['residuo'] == 0:
            st.write("**Caso: Discontinuidad Removible**")
            st.write("La función es una fracción racional con un factor común que se anula en x = a:")
            st.latex(
                rf"f(x) = \frac{{(x - {datos['a']})(x + {res['cuerpo'][0]})}}{{x - {datos['a']}}}"
            )
            st.write("Simplificando para $x \\neq a$:")
            st.latex(
                rf"\lim_{{x \to {datos['a']}^-}} f(x) = "
                rf"\lim_{{x \to {datos['a']}^-}} (x + {res['cuerpo'][0]}) = "
                rf"{datos['a']} + {res['cuerpo'][0]} = {datos['lim_izq_exacto']}"
            )
            st.latex(
                rf"\lim_{{x \to {datos['a']}^+}} f(x) = "
                rf"\lim_{{x \to {datos['a']}^+}} (x + {res['cuerpo'][0]}) = "
                rf"{datos['a']} + {res['cuerpo'][0]} = {datos['lim_der_exacto']}"
            )
            st.markdown(
                rf"""
                Dado que ambos límites laterales son iguales y finitos:
                $$\lim_{{x \to {datos['a']}}} f(x) = {datos['lim_izq_exacto']}$$
                Sin embargo, la función en el punto $x = {datos['a']}$ **no está definida**:
                $$f({datos['a']}) = \frac{{0}}{{0}} \quad (\text{{Indefinido}})$$
                Como el límite existe pero la función no está definida, la discontinuidad es **Removible (Evitable)**.
                Para eliminarla, bastaría con redefinir $f({datos['a']}) = {datos['lim_izq_exacto']}$.
                """
            )

        elif datos['residuo'] == 1:
            d2 = int(res['cuerpo'][1])
            d4 = int(res['cuerpo'][3])
            st.write("**Caso: Discontinuidad de Salto**")
            st.write("La función se define por dos tramos lineales con comportamiento distinto al acercarse a x = a:")
            st.latex(datos['formula_latex'])
            st.write("Calculamos los límites laterales evaluando en el tramo correspondiente:")
            st.latex(
                rf"\lim_{{x \to {datos['a']}^-}} f(x) = "
                rf"\lim_{{x \to {datos['a']}^-}} (x + {d2}) = "
                rf"{datos['a']} + {d2} = {datos['lim_izq_exacto']}"
            )
            st.latex(
                rf"\lim_{{x \to {datos['a']}^+}} f(x) = "
                rf"\lim_{{x \to {datos['a']}^+}} (x + {d4}) = "
                rf"{datos['a']} + {d4} = {datos['lim_der_exacto']}"
            )
            st.markdown(
                rf"""
                Dado que los límites laterales son finitos pero **distintos**:
                $$\lim_{{x \to {datos['a']}^-}} f(x) = {datos['lim_izq_exacto']} \neq {datos['lim_der_exacto']} = \lim_{{x \to {datos['a']}^+}} f(x)$$
                El límite bilateral $\lim_{{x \to {datos['a']}}} f(x)$ **no existe**.
                
                El valor de la función en el punto (tramo derecho, $x \geq a$) es:
                $$f({datos['a']}) = {datos['a']} + {d4} = {datos['fa_exacto']}$$
                
                Como los límites laterales existen pero son diferentes, corresponde a una **Discontinuidad de Salto (Finito)**.
                El tamaño del salto es:
                $$|\text{{Salto}}| = |{datos['lim_der_exacto']} - {datos['lim_izq_exacto']}| = {abs(datos['lim_der_exacto'] - datos['lim_izq_exacto'])}$$
                """
            )

        elif datos['residuo'] == 2:
            num_val = int(res['cuerpo'][4]) + 1
            st.write("**Caso: Discontinuidad Infinita**")
            st.write("La función es una fracción racional cuyo denominador se anula en x = a:")
            st.latex(rf"f(x) = \frac{{{num_val}}}{{x - {datos['a']}}}")
            st.write("Analizamos el signo del denominador a cada lado del punto crítico:")
            st.latex(
                rf"\text{{Si }} x \to {datos['a']}^-: \; x - {datos['a']} \to 0^- \implies "
                rf"\frac{{{num_val}}}{{0^-}} = -\infty"
            )
            st.latex(
                rf"\text{{Si }} x \to {datos['a']}^+: \; x - {datos['a']} \to 0^+ \implies "
                rf"\frac{{{num_val}}}{{0^+}} = +\infty"
            )
            st.markdown(
                rf"""
                Por lo tanto:
                $$\lim_{{x \to {datos['a']}^-}} f(x) = -\infty \qquad \lim_{{x \to {datos['a']}^+}} f(x) = +\infty$$
                
                La función **no está definida** en $x = {datos['a']}$:
                $$f({datos['a']}) = \frac{{{num_val}}}{{0}} \quad (\text{{Indefinido}})$$
                
                La recta $x = {datos['a']}$ es una **asíntota vertical**.
                La discontinuidad corresponde a una **Discontinuidad Infinita (Asintótica)**.
                """
            )
