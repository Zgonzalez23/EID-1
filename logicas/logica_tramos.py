import plotly.graph_objects as go
from utilidades import formato_num

def generar_datos_tramos(cuerpo, dv):
    d = [int(x) for x in cuerpo]
    a = d[2]  # a = d3 (índice 2)
    d8 = d[7] # d8
    
    residuo = d8 % 3
    
    tabla_x = [a - 1, a - 0.1, a - 0.01, a - 0.001, a + 0.001, a + 0.01, a + 0.1, a + 1]
    tabla_valores = []

    def crear_fila_tabla(x, valor):
        return {
            'x': formato_num(x),
            'f(x)': formato_num(valor),
            'lado': 'izquierda' if x < a else 'derecha',
            'distancia a': formato_num(abs(x - a))
        }
    
    if residuo == 0:
        caso = "Discontinuidad removible"
        regla = f"Como d8 ({d8}) es múltiplo de 3, se genera una función racional con factor común."
        d1 = d[0]
        formula_latex = rf"f(x) = \frac{{(x - {a})(x + {d1})}}{{x - {a}}}"
        
        # Valores exactos para validación
        lim_izq_exacto = a + d1
        lim_der_exacto = a + d1
        lim_bilateral_existe = "Sí, existe"
        fa_existe = "No existe / Indefinido"
        fa_exacto = None
        tipo_discontinuidad = "Removible (Evitable)"
        
        # Valores
        for x in tabla_x:
            val = x + d1  # (x-a)(x+d1)/(x-a) = x+d1 for x!=a
            tabla_valores.append(crear_fila_tabla(x, val))
            
        # Grafico
        x_izq = [a - 5 + (5 * i / 100) for i in range(100)]
        x_der = [a + 0.01 + (5 * i / 100) for i in range(100)]
        y_izq = [x + d1 for x in x_izq]
        y_der = [x + d1 for x in x_der]
        
        figura = go.Figure()
        figura.add_trace(go.Scatter(x=x_izq, y=y_izq, mode='lines', line=dict(color='#3b82f6', width=3)))
        figura.add_trace(go.Scatter(x=x_der, y=y_der, mode='lines', line=dict(color='#3b82f6', width=3)))
        # Hueco
        figura.add_trace(go.Scatter(x=[a], y=[a + d1], mode='markers', marker=dict(color='rgba(0,0,0,0)', size=10, line=dict(color='#3b82f6', width=2))))
        
    elif residuo == 1:
        caso = "Discontinuidad de salto"
        regla = f"Como d8 ({d8}) deja residuo 1 al dividirse por 3, se generan dos tramos lineales con comportamiento distinto."
        d2 = d[1]
        d4 = d[3]
        formula_latex = rf"f(x) = \begin{{cases}} x + {d2}, & \text{{si }} x < {a} \\ x + {d4}, & \text{{si }} x \geq {a} \end{{cases}}"
        
        # Valores exactos para validación
        lim_izq_exacto = a + d2
        lim_der_exacto = a + d4
        lim_bilateral_existe = "No, no existe"
        fa_existe = "Existe"
        fa_exacto = a + d4
        tipo_discontinuidad = "Salto (Finito)"
        
        # Valores
        for x in tabla_x:
            if x < a:
                val = x + d2
            else:
                val = x + d4
            tabla_valores.append(crear_fila_tabla(x, val))
            
        # Grafico
        x_izq = [a - 5 + (5 * i / 100) for i in range(100)]
        x_der = [a + (5 * i / 100) for i in range(101)]
        y_izq = [x + d2 for x in x_izq]
        y_der = [x + d4 for x in x_der]
        
        figura = go.Figure()
        figura.add_trace(go.Scatter(x=x_izq, y=y_izq, mode='lines', line=dict(color='#3b82f6', width=3)))
        figura.add_trace(go.Scatter(x=x_der, y=y_der, mode='lines', line=dict(color='#ef4444', width=3)))
        # Hueco y punto lleno
        figura.add_trace(go.Scatter(x=[a], y=[a + d2], mode='markers', marker=dict(color='rgba(0,0,0,0)', size=10, line=dict(color='#3b82f6', width=2))))
        figura.add_trace(go.Scatter(x=[a], y=[a + d4], mode='markers', marker=dict(color='#ef4444', size=10)))

    else:
        caso = "Discontinuidad infinita"
        regla = f"Como d8 ({d8}) deja residuo 2 al dividirse por 3, se genera una función racional con asíntota vertical."
        d5 = d[4]
        num = d5 + 1
        formula_latex = rf"f(x) = \frac{{{num}}}{{x - {a}}}"
        
        # Valores exactos para validación
        lim_izq_exacto = "-infinito"
        lim_der_exacto = "+infinito"
        lim_bilateral_existe = "No, no existe"
        fa_existe = "No existe / Indefinido"
        fa_exacto = None
        tipo_discontinuidad = "Infinita (Asintótica)"
        
        # Valores
        for x in tabla_x:
            val = num / (x - a)
            tabla_valores.append(crear_fila_tabla(x, val))
            
        # Grafico
        x_izq = [a - 5 + (4.9 * i / 100) for i in range(101)]
        x_der = [a + 0.1 + (4.9 * i / 100) for i in range(101)]
        y_izq = [num / (x - a) for x in x_izq]
        y_der = [num / (x - a) for x in x_der]
        
        figura = go.Figure()
        figura.add_trace(go.Scatter(x=x_izq, y=y_izq, mode='lines', line=dict(color='#3b82f6', width=3)))
        figura.add_trace(go.Scatter(x=x_der, y=y_der, mode='lines', line=dict(color='#3b82f6', width=3)))
        # Asintota
        figura.add_vline(x=a, line_width=2, line_dash="dash", line_color="#94a3b8")

    figura.update_layout(
        title="Gráfica de la Función por Tramos",
        xaxis_title="Eje X", yaxis_title="Eje Y",
        width=700, height=500,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        xaxis=dict(zeroline=True, gridcolor='#334155', zerolinecolor='#94a3b8'),
        yaxis=dict(zeroline=True, gridcolor='#334155', zerolinecolor='#94a3b8', range=[-20, 20]),
        showlegend=False
    )
    
    return {
        'a': a,
        'd8': d8,
        'residuo': residuo,
        'caso': caso,
        'regla': regla,
        'formula_latex': formula_latex,
        'tabla_valores': tabla_valores,
        'figura': figura,
        'lim_izq_exacto': lim_izq_exacto,
        'lim_der_exacto': lim_der_exacto,
        'lim_bilateral_existe': lim_bilateral_existe,
        'fa_existe': fa_existe,
        'fa_exacto': fa_exacto,
        'tipo_discontinuidad': tipo_discontinuidad
    }
