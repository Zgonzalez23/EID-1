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
    
    st.header("5. Gráfica en el Plano Cartesiano")
    figura = graficar_conica(A, B, C, D, E)
    st.plotly_chart(figura, use_container_width=True)

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
    st.write("Complete los siguientes campos basándose en el análisis de límites laterales:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Límite por la izquierda (lim x -> a-):", key="lim_izq")
        st.text_input("Conclusión sobre la existencia del límite:", key="conc_lim")
        st.text_input("Conclusión sobre continuidad:", key="conc_cont")
    with col2:
        st.text_input("Límite por la derecha (lim x -> a+):", key="lim_der")
        st.text_input("Valor de la función en el punto f(a):", key="val_fa")
        st.text_input("Tipo de discontinuidad:", key="tipo_disc")
        
    st.text_area("Justificación escrita del comportamiento observado:", key="justificacion")

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
