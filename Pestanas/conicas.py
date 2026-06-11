import streamlit as st
from logicas.logica_conicas import generar_conica, graficar_conica, calcular_elementos_conica
from utilidades import (
    formato_num,
    formato_signo,
    formato_primer_signo,
    comparar_valores,
    validar_puntos_desordenados
)

def renderizar_pestana_conica(res):
    conica = generar_conica(res['cuerpo'], res['dv_ingresado'], res['v_val'])
    A, B, C, D, E = conica['A'], conica['B'], conica['C'], conica['D'], conica['E']
    
    st.header("1. Construcción de la Ecuación General")
    st.code("\n".join(conica['registros']))
    eq_general = f"{formato_primer_signo(A)}x^2 {formato_signo(B)}y^2 {formato_signo(C)}x {formato_signo(D)}y {formato_signo(E)} = 0"
    st.latex(eq_general)
    
    st.header("2. Clasificación de la Cónica")
    st.success(f"**Tipo Determinado:** {conica['tipo_conica']}")
    
    st.header("3. Transformación a Forma Canónica")
    if conica['tipo_conica'] == 'Parábola':
        if A == 0:
            k = -D / (2 * B)
            F_prima = -E + D**2 / (4 * B)
            h = F_prima / C
            
            st.latex(rf"{formato_primer_signo(B)}(y^2 {formato_signo(D/B)}y) = {formato_signo(-C)}x {formato_signo(-E)}")
            st.latex(rf"{formato_primer_signo(B)}(y {formato_signo(-k)})^2 = {formato_signo(-C)}x {formato_signo(-E)} + {formato_num(D**2/(4*B))}")
            st.info("Forma Canónica:")
            st.latex(rf"(y {formato_signo(-k)})^2 = {formato_num(-C/B)} (x {formato_signo(-h)})")
            
            st.header("4. Inversa: Canónica a General")
            st.latex(rf"(y {formato_signo(-k)})^2 = {formato_num(-C/B)} (x {formato_signo(-h)})")
            st.latex(rf"y^2 {formato_signo(-2*k)}y + {formato_num(k*k)} = {formato_num(-C/B)}x {formato_signo((-C/B)*-h)}")
            st.latex(rf"{formato_primer_signo(B)}y^2 {formato_signo(C)}x {formato_signo(B*-2*k)}y {formato_signo(B*k*k - (-C)*-h)} = 0")

        else:
            h = -C / (2 * A)
            F_prima = -E + C**2 / (4 * A)
            k = F_prima / D
            
            st.latex(rf"{formato_primer_signo(A)}(x^2 {formato_signo(C/A)}x) = {formato_signo(-D)}y {formato_signo(-E)}")
            st.latex(rf"{formato_primer_signo(A)}(x {formato_signo(-h)})^2 = {formato_signo(-D)}y {formato_signo(-E)} + {formato_num(C**2/(4*A))}")
            st.info("Forma Canónica:")
            st.latex(rf"(x {formato_signo(-h)})^2 = {formato_num(-D/A)} (y {formato_signo(-k)})")
            
            st.header("4. Inversa: Canónica a General")
            st.latex(rf"(x {formato_signo(-h)})^2 = {formato_num(-D/A)} (y {formato_signo(-k)})")
            st.latex(rf"x^2 {formato_signo(-2*h)}x + {formato_num(h*h)} = {formato_num(-D/A)}y {formato_signo((-D/A)*-k)}")
            st.latex(rf"{formato_primer_signo(A)}x^2 {formato_signo(D)}y {formato_signo(A*-2*h)}x {formato_signo(A*h*h - (-D)*-k)} = 0")
    else:
        h = -C / (2 * A)
        k = -D / (2 * B)
        LadoDerecho = -E + C**2 / (4 * A) + D**2 / (4 * B)
        
        F_A = LadoDerecho / A
        F_B = LadoDerecho / B
        
        st.latex(rf"{formato_primer_signo(A)}(x^2 {formato_signo(C/A)}x) {formato_signo(B)}(y^2 {formato_signo(D/B)}y) = {-E}")
        st.latex(rf"{formato_primer_signo(A)}(x {formato_signo(-h)})^2 {formato_signo(B)}(y {formato_signo(-k)})^2 = {-E} + {formato_num(C**2/(4*A))} + {formato_num(D**2/(4*B))}")
        st.info("Forma Canónica:")
        st.latex(rf"\frac{{(x {formato_signo(-h)})^2}}{{{formato_num(F_A)}}} + \frac{{(y {formato_signo(-k)})^2}}{{{formato_num(F_B)}}} = 1")
        
        st.header("4. Inversa: Canónica a General")
        st.latex(rf"{formato_primer_signo(A)}(x {formato_signo(-h)})^2 {formato_signo(B)}(y {formato_signo(-k)})^2 = {formato_num(LadoDerecho)}")
        st.latex(rf"{formato_primer_signo(A)}(x^2 {formato_signo(-2*h)}x + {formato_num(h**2)}) {formato_signo(B)}(y^2 {formato_signo(-2*k)}y + {formato_num(k**2)}) = {formato_num(LadoDerecho)}")
        st.latex(rf"{formato_primer_signo(A)}x^2 {formato_signo(B)}y^2 {formato_signo(A*-2*h)}x {formato_signo(B*-2*k)}y {formato_signo(A*h**2 + B*k**2 - LadoDerecho)} = 0")
    
    st.header("5. Gráfica y Evaluación de Elementos")
    elementos = calcular_elementos_conica(A, B, C, D, E)
    tipo_conica = elementos['tipo']
    
    mostrar_elementos = st.checkbox("Mostrar ayuda visual (elementos geométricos principales en el gráfico)", value=True)
    
    col_graph, col_eval = st.columns([1.1, 1.0])
    
    with col_graph:
        figura = graficar_conica(A, B, C, D, E, mostrar_elementos=mostrar_elementos)
        st.plotly_chart(figura, use_container_width=True)
        
    with col_eval:
        st.subheader("Evaluación de Elementos Geométricos")
        st.write("Completa los elementos de la cónica basándote en la ecuación y en el gráfico:")
        
        if tipo_conica == 'Circunferencia':
            user_h = st.text_input("Centro h (coordenada x):", key="c_h")
            user_k = st.text_input("Centro k (coordenada y):", key="c_k")
            user_r = st.text_input("Radio R:", key="c_r")
            user_r2 = st.text_input("Radio al cuadrado R²:", key="c_r2")
            
            st.markdown("#### Validación en tiempo real:")
            sh = comparar_valores(user_h, elementos['h'])
            sk = comparar_valores(user_k, elementos['k'])
            sr = comparar_valores(user_r, elementos['r'])
            sr2 = comparar_valores(user_r2, elementos['r2'])
            
            st.write(f"- **Centro h:** {sh}")
            st.write(f"- **Centro k:** {sk}")
            st.write(f"- **Radio R:** {sr}")
            st.write(f"- **Radio R²:** {sr2}")
            
        elif tipo_conica == 'Parábola':
            user_h = st.text_input("Vértice h (coordenada x):", key="p_h")
            user_k = st.text_input("Vértice k (coordenada y):", key="p_k")
            user_p = st.text_input("Parámetro p (distancia focal con signo):", key="p_p")
            user_fx = st.text_input("Foco coordenada x:", key="p_fx")
            user_fy = st.text_input("Foco coordenada y:", key="p_fy")
            
            st.write("**Directriz:**")
            user_dir_val = st.text_input("Valor constante de la directriz (ej: si es y = 3, ingresa 3):", key="p_dir_val")
            user_dir_ori = st.selectbox("Orientación de la directriz:", ["", "Horizontal (y = constante)", "Vertical (x = constante)"], key="p_dir_ori")
            
            st.write("**Eje de Simetría:**")
            user_eje_val = st.text_input("Valor constante del eje de simetría:", key="p_eje_val")
            user_eje_ori = st.selectbox("Orientación del eje de simetría:", ["", "Horizontal (y = constante)", "Vertical (x = constante)"], key="p_eje_ori")
            
            real_eje = elementos['ejes_directriz_asintotas'][0]
            real_dir = elementos['ejes_directriz_asintotas'][1]
            
            st.markdown("#### Validación en tiempo real:")
            sh = comparar_valores(user_h, elementos['h'])
            sk = comparar_valores(user_k, elementos['k'])
            sp = comparar_valores(user_p, elementos['p'])
            sfx = comparar_valores(user_fx, elementos['focos'][0][0])
            sfy = comparar_valores(user_fy, elementos['focos'][0][1])
            sdir_val = comparar_valores(user_dir_val, real_dir['val'])
            seje_val = comparar_valores(user_eje_val, real_eje['val'])
            
            dir_ori_exacta = "Vertical (x = constante)" if real_dir['orientacion'] == 'V' else "Horizontal (y = constante)"
            eje_ori_exacto = "Vertical (x = constante)" if real_eje['orientacion'] == 'V' else "Horizontal (y = constante)"
            
            sdir_ori = "✅ Correcto" if user_dir_ori == dir_ori_exacta else ("⚠️ Vacío" if not user_dir_ori else "❌ Incorrecto")
            seje_ori = "✅ Correcto" if user_eje_ori == eje_ori_exacto else ("⚠️ Vacío" if not user_eje_ori else "❌ Incorrecto")
            
            st.write(f"- **Vértice:** h: {sh} | k: {sk}")
            st.write(f"- **Parámetro p:** {sp}")
            st.write(f"- **Foco:** x: {sfx} | y: {sfy}")
            st.write(f"- **Directriz:** Valor: {sdir_val} | Orientación: {sdir_ori}")
            st.write(f"- **Eje de Simetría:** Valor: {seje_val} | Orientación: {seje_ori}")
            
        elif tipo_conica == 'Elipse':
            user_h = st.text_input("Centro h (coordenada x):", key="e_h")
            user_k = st.text_input("Centro k (coordenada y):", key="e_k")
            user_a = st.text_input("Semieje mayor a:", key="e_a")
            user_b = st.text_input("Semieje menor b:", key="e_b")
            user_c = st.text_input("Semidistancia focal c:", key="e_c")
            
            st.write("**Focos:**")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                user_f1x = st.text_input("Foco 1 x:", key="e_f1x")
                user_f1y = st.text_input("Foco 1 y:", key="e_f1y")
            with col_f2:
                user_f2x = st.text_input("Foco 2 x:", key="e_f2x")
                user_f2y = st.text_input("Foco 2 y:", key="e_f2y")
                
            st.write("**Vértices Principales:**")
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                user_v1x = st.text_input("Vértice 1 x:", key="e_v1x")
                user_v1y = st.text_input("Vértice 1 y:", key="e_v1y")
            with col_v2:
                user_v2x = st.text_input("Vértice 2 x:", key="e_v2x")
                user_v2y = st.text_input("Vértice 2 y:", key="e_v2y")
                
            st.markdown("#### Validación en tiempo real:")
            sh = comparar_valores(user_h, elementos['h'])
            sk = comparar_valores(user_k, elementos['k'])
            sa = comparar_valores(user_a, elementos['a'])
            sb = comparar_valores(user_b, elementos['b'])
            sc = comparar_valores(user_c, elementos['c'])
            
            sf1, sf2 = validar_puntos_desordenados(user_f1x, user_f1y, user_f2x, user_f2y, elementos['focos'][0], elementos['focos'][1])
            sv1, sv2 = validar_puntos_desordenados(user_v1x, user_v1y, user_v2x, user_v2y, elementos['vertices'][0], elementos['vertices'][1])
            
            st.write(f"- **Centro:** h: {sh} | k: {sk}")
            st.write(f"- **Semiejes:** a: {sa} | b: {sb}")
            st.write(f"- **Semidistancia focal c:** {sc}")
            st.write(f"- **Focos:** Foco 1: {sf1} | Foco 2: {sf2}")
            st.write(f"- **Vértices Principales:** Vértice 1: {sv1} | Vértice 2: {sv2}")
            
        elif tipo_conica == 'Hipérbola':
            user_h = st.text_input("Centro h (coordenada x):", key="h_h")
            user_k = st.text_input("Centro k (coordenada y):", key="h_k")
            user_a = st.text_input("Semieje real a:", key="h_a")
            user_b = st.text_input("Semieje imaginario b:", key="h_b")
            user_c = st.text_input("Semidistancia focal c:", key="h_c")
            user_m = st.text_input("Pendiente de las asíntotas (m = valor positivo):", key="h_m")
            
            st.write("**Focos:**")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                user_f1x = st.text_input("Foco 1 x:", key="h_f1x")
                user_f1y = st.text_input("Foco 1 y:", key="h_f1y")
            with col_f2:
                user_f2x = st.text_input("Foco 2 x:", key="h_f2x")
                user_f2y = st.text_input("Foco 2 y:", key="h_f2y")
                
            st.write("**Vértices:**")
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                user_v1x = st.text_input("Vértice 1 x:", key="h_v1x")
                user_v1y = st.text_input("Vértice 1 y:", key="h_v1y")
            with col_v2:
                user_v2x = st.text_input("Vértice 2 x:", key="h_v2x")
                user_v2y = st.text_input("Vértice 2 y:", key="h_v2y")
                
            real_m = elementos['ejes_directriz_asintotas'][2]['pend']
            
            st.markdown("#### Validación en tiempo real:")
            sh = comparar_valores(user_h, elementos['h'])
            sk = comparar_valores(user_k, elementos['k'])
            sa = comparar_valores(user_a, elementos['a'])
            sb = comparar_valores(user_b, elementos['b'])
            sc = comparar_valores(user_c, elementos['c'])
            sm = comparar_valores(user_m, real_m)
            
            sf1, sf2 = validar_puntos_desordenados(user_f1x, user_f1y, user_f2x, user_f2y, elementos['focos'][0], elementos['focos'][1])
            sv1, sv2 = validar_puntos_desordenados(user_v1x, user_v1y, user_v2x, user_v2y, elementos['vertices'][0], elementos['vertices'][1])
            
            st.write(f"- **Centro:** h: {sh} | k: {sk}")
            st.write(f"- **Semiejes:** a: {sa} | b: {sb}")
            st.write(f"- **Semidistancia focal c:** {sc}")
            st.write(f"- **Pendiente de Asíntotas:** {sm}")
            st.write(f"- **Focos:** Foco 1: {sf1} | Foco 2: {sf2}")
            st.write(f"- **Vértices:** Vértice 1: {sv1} | Vértice 2: {sv2}")

    with st.expander("Revelar Solución Detallada y Procedimiento Matemático"):
        st.subheader("Desarrollo de Elementos Geométricos")
        st.write(f"**Tipo de Cónica:** {tipo_conica}")
        
        if tipo_conica == 'Circunferencia':
            st.write("Ecuación Canónica:")
            st.latex(rf"(x - {formato_num(elementos['h'])})^2 + (y - {formato_num(elementos['k'])})^2 = {formato_num(elementos['r2'])}")
            st.markdown(f"""
            - **Centro $C(h, k)$:** $h = -C/(2A) = {formato_num(elementos['h'])}$, $k = -D/(2A) = {formato_num(elementos['k'])}$
            - **Radio $R$:** $\\sqrt{{{formato_num(elementos['r2'])}}} = {formato_num(elementos['r'])}$
            """)
        elif tipo_conica == 'Parábola':
            if elementos['es_horizontal']:
                st.write("Ecuación Canónica (Parábola Horizontal):")
                st.latex(rf"(y - {formato_num(elementos['k'])})^2 = {formato_num(4*elementos['p'])} (x - {formato_num(elementos['h'])})")
                st.markdown(f"""
                - **Vértice $V(h, k)$:** $V({formato_num(elementos['h'])}, {formato_num(elementos['k'])})$
                - **Parámetro $p$:** $-C/(4B) = {formato_num(elementos['p'])}$
                - **Foco $F(h + p, k)$:** $F({formato_num(elementos['focos'][0][0])}, {formato_num(elementos['focos'][0][1])})$
                - **Directriz:** $x = h - p \\implies x = {formato_num(elementos['h'] - elementos['p'])}$
                - **Eje de Simetría:** $y = k \\implies y = {formato_num(elementos['k'])}$
                """)
            else:
                st.write("Ecuación Canónica (Parábola Vertical):")
                st.latex(rf"(x - {formato_num(elementos['h'])})^2 = {formato_num(4*elementos['p'])} (y - {formato_num(elementos['k'])})")
                st.markdown(f"""
                - **Vértice $V(h, k)$:** $V({formato_num(elementos['h'])}, {formato_num(elementos['k'])})$
                - **Parámetro $p$:** $-D/(4A) = {formato_num(elementos['p'])}$
                - **Foco $F(h, k + p)$:** $F({formato_num(elementos['focos'][0][0])}, {formato_num(elementos['focos'][0][1])})$
                - **Directriz:** $y = k - p \\implies y = {formato_num(elementos['k'] - elementos['p'])}$
                - **Eje de Simetría:** $x = h \\implies x = {formato_num(elementos['h'])}$
                """)
        elif tipo_conica == 'Elipse':
            orient_str = "Horizontal" if elementos['es_horizontal'] else "Vertical"
            st.write(f"Ecuación Canónica (Elipse {orient_str}):")
            st.latex(rf"\frac{{(x - {formato_num(elementos['h'])})^2}}{{{formato_num(F_A)}}} + \frac{{(y - {formato_num(elementos['k'])})^2}}{{{formato_num(F_B)}}} = 1")
            st.markdown(f"""
            - **Centro $C(h, k)$:** $C({formato_num(elementos['h'])}, {formato_num(elementos['k'])})$
            - **Semieje mayor $a$:** ${formato_num(elementos['a'])}$
            - **Semieje menor $b$:** ${formato_num(elementos['b'])}$
            - **Semidistancia focal $c = \\sqrt{{a^2 - b^2}}$:** $\\sqrt{{{formato_num(elementos['a']**2)} - {formato_num(elementos['b']**2)}}} = {formato_num(elementos['c'])}$
            - **Focos:** $F_1({formato_num(elementos['focos'][0][0])}, {formato_num(elementos['focos'][0][1])})$ y $F_2({formato_num(elementos['focos'][1][0])}, {formato_num(elementos['focos'][1][1])})$
            - **Vértices Principales:** $V_1({formato_num(elementos['vertices'][0][0])}, {formato_num(elementos['vertices'][0][1])})$ y $V_2({formato_num(elementos['vertices'][1][0])}, {formato_num(elementos['vertices'][1][1])})$
            """)
        elif tipo_conica == 'Hipérbola':
            orient_str = "Horizontal" if elementos['es_horizontal'] else "Vertical"
            st.write(f"Ecuación Canónica (Hipérbola {orient_str}):")
            if elementos['es_horizontal']:
                st.latex(rf"\frac{{(x - {formato_num(elementos['h'])})^2}}{{{formato_num(elementos['a']**2)}}} - \frac{{(y - {formato_num(elementos['k'])})^2}}{{{formato_num(elementos['b']**2)}}} = 1")
            else:
                st.latex(rf"\frac{{(y - {formato_num(elementos['k'])})^2}}{{{formato_num(elementos['a']**2)}}} - \frac{{(x - {formato_num(elementos['h'])})^2}}{{{formato_num(elementos['b']**2)}}} = 1")
            st.markdown(f"""
            - **Centro $C(h, k)$:** $C({formato_num(elementos['h'])}, {formato_num(elementos['k'])})$
            - **Semieje real $a$:** ${formato_num(elementos['a'])}$
            - **Semieje imaginario $b$:** ${formato_num(elementos['b'])}$
            - **Semidistancia focal $c = \\sqrt{{a^2 + b^2}}$:** $\\sqrt{{{formato_num(elementos['a']**2)} + {formato_num(elementos['b']**2)}}} = {formato_num(elementos['c'])}$
            - **Asíntotas:** $y - k = \\pm \\frac{{a}}{{b}}(x - h)$ o $\\pm \\frac{{b}}{{a}}(x - h) \\implies$ Pendiente $m = {formato_num(real_m)}$
            - **Focos:** $F_1({formato_num(elementos['focos'][0][0])}, {formato_num(elementos['focos'][0][1])})$ y $F_2({formato_num(elementos['focos'][1][0])}, {formato_num(elementos['focos'][1][1])})$
            - **Vértices:** $V_1({formato_num(elementos['vertices'][0][0])}, {formato_num(elementos['vertices'][0][1])})$ y $V_2({formato_num(elementos['vertices'][1][0])}, {formato_num(elementos['vertices'][1][1])})$
            """)
