import plotly.graph_objects as go
from utilidades import formato_num

def generar_conica(cuerpo, dv, v):
    d = [int(x) for x in cuerpo]
    A = (d[0] + d[1]) / v
    B = (d[2] + d[3]) / v
    C = -(d[4] + d[5])
    D = -(d[6] + d[7])
    E = d[0] + d[2] + d[4] + d[6]

    registros = [
        f"Valor de v asignado: {v} (DV = {dv})",
        f"A = ({d[0]} + {d[1]}) / {v} = {formato_num(A)}",
        f"B = ({d[2]} + {d[3]}) / {v} = {formato_num(B)}",
        f"C = -({d[4]} + {d[5]}) = {C}",
        f"D = -({d[6]} + {d[7]}) = {D}",
        f"E = {d[0]} + {d[2]} + {d[4]} + {d[6]} = {E}"
    ]

    # Prioridad 1: parábola (tiene mayor precedencia sobre los demás ajustes)
    if (d[4] + d[5]) % 3 == 0:
        if d[6] % 2 == 0:
            B = 0
            registros.append(
                f"Ajuste (prioridad 1 - parábola): d5+d6 = {d[4]+d[5]} es múltiplo de 3 "
                f"y d7 = {d[6]} es par → B = 0 (Parábola de eje vertical)."
            )
        else:
            A = 0
            registros.append(
                f"Ajuste (prioridad 1 - parábola): d5+d6 = {d[4]+d[5]} es múltiplo de 3 "
                f"y d7 = {d[6]} es impar → A = 0 (Parábola de eje horizontal)."
            )
    else:
        # Prioridad 2: hipérbola (solo si no hay parábola)
        if d[7] % 2 != 0:
            B = -B
            registros.append(
                f"Ajuste (prioridad 2 - hipérbola): d8 = {d[7]} es impar "
                f"→ B cambia de signo, B = {formato_num(B)}."
            )

        # Prioridad 3: circunferencia (solo si no hay parábola; puede combinarse con hipérbola,
        # pero si d1=d2 se impone B=A, el resultado final es una circunferencia)
        if d[0] == d[1]:
            B = A
            registros.append(
                f"Ajuste (prioridad 3 - circunferencia): d1 = d2 = {d[0]} "
                f"→ se impone B = A = {formato_num(B)}."
            )

    if A == 0 or B == 0:
        tipo_conica = 'Parábola'
    elif A == B:
        tipo_conica = 'Circunferencia'
    elif A * B > 0:
        tipo_conica = 'Elipse'
    else:
        tipo_conica = 'Hipérbola'

    return {
        'A': A, 'B': B, 'C': C, 'D': D, 'E': E,
        'registros': registros, 'tipo_conica': tipo_conica
    }

def calcular_elementos_conica(A, B, C, D, E):
    if A == 0 or B == 0:
        tipo = 'Parábola'
    elif A == B:
        tipo = 'Circunferencia'
    elif A * B > 0:
        tipo = 'Elipse'
    else:
        tipo = 'Hipérbola'

    elementos = {
        'tipo': tipo,
        'centro_o_vertice': (0.0, 0.0),
        'focos': [],
        'vertices': [],
        'ejes_directriz_asintotas': [],
        'degenerada': None  # None = caso normal; si no, contiene el mensaje a mostrar
    }

    # 1. PARÁBOLA
    if tipo == 'Parábola':
        if A == 0:  # B y^2 + C x + D y + E = 0 -> (y - k)^2 = 4p(x - h)
            k = -D / (2 * B) if B != 0 else 0.0
            F_prima = -E + (D**2) / (4 * B) if B != 0 else -E
            h = F_prima / C if C != 0 else 0.0
            p = -C / (4 * B) if B != 0 else 0.0

            elementos['centro_o_vertice'] = (h, k)
            elementos['vertices'] = [(h, k)]
            elementos['focos'] = [(h + p, k)]
            elementos['h'] = h
            elementos['k'] = k
            elementos['p'] = p
            elementos['es_horizontal'] = True

            elementos['ejes_directriz_asintotas'] = [
                {
                    'tipo': 'Eje de simetría',
                    'eq_latex': f"y = {formato_num(k)}",
                    'val': k,
                    'orientacion': 'H'
                },
                {
                    'tipo': 'Directriz',
                    'eq_latex': f"x = {formato_num(h - p)}",
                    'val': h - p,
                    'orientacion': 'V'
                }
            ]
        else:  # A x^2 + C x + D y + E = 0 -> (x - h)^2 = 4p(y - k)
            h = -C / (2 * A) if A != 0 else 0.0
            F_prima = -E + (C**2) / (4 * A) if A != 0 else -E
            k = F_prima / D if D != 0 else 0.0
            p = -D / (4 * A) if A != 0 else 0.0

            elementos['centro_o_vertice'] = (h, k)
            elementos['vertices'] = [(h, k)]
            elementos['focos'] = [(h, k + p)]
            elementos['h'] = h
            elementos['k'] = k
            elementos['p'] = p
            elementos['es_horizontal'] = False

            elementos['ejes_directriz_asintotas'] = [
                {
                    'tipo': 'Eje de simetría',
                    'eq_latex': f"x = {formato_num(h)}",
                    'val': h,
                    'orientacion': 'V'
                },
                {
                    'tipo': 'Directriz',
                    'eq_latex': f"y = {formato_num(k - p)}",
                    'val': k - p,
                    'orientacion': 'H'
                }
            ]

    # 2. CIRCUNFERENCIA
    elif tipo == 'Circunferencia':
        h = -C / (2 * A) if A != 0 else 0.0
        k = -D / (2 * A) if A != 0 else 0.0
        r2 = -E/A + (C**2)/(4*A**2) + (D**2)/(4*A**2) if A != 0 else 0.0

        elementos['h'] = h
        elementos['k'] = k
        elementos['r2'] = r2
        elementos['centro_o_vertice'] = (h, k)

        if r2 < 0:
            elementos['degenerada'] = (
                f"Circunferencia imaginaria: R² = {formato_num(r2)} < 0, "
                "por lo tanto la ecuación no tiene puntos reales asociados."
            )
            elementos['r'] = 0.0
        elif r2 == 0:
            elementos['degenerada'] = (
                "Circunferencia degenerada: R² = 0, por lo tanto la ecuación "
                "representa un único punto (el centro) y no una curva."
            )
            elementos['r'] = 0.0
            elementos['focos'] = [(h, k)]
        else:
            r = r2 ** 0.5
            elementos['r'] = r
            elementos['vertices'] = [(h + r, k), (h - r, k), (h, k + r), (h, k - r)]
            elementos['focos'] = [(h, k)]

    # 3. ELIPSE
    elif tipo == 'Elipse':
        h = -C / (2 * A) if A != 0 else 0.0
        k = -D / (2 * B) if B != 0 else 0.0
        LadoDerecho = -E + (C**2)/(4*A) + (D**2)/(4*B)

        F_A = LadoDerecho / A if A != 0 else 0.0
        F_B = LadoDerecho / B if B != 0 else 0.0

        elementos['h'] = h
        elementos['k'] = k
        elementos['centro_o_vertice'] = (h, k)

        if LadoDerecho == 0:
            elementos['degenerada'] = (
                "Elipse degenerada: el lado derecho de la ecuación canónica es 0, "
                "por lo tanto la ecuación representa un único punto (el centro) y no una curva."
            )
        elif F_A < 0:
            # Como A y B tienen el mismo signo en una elipse, F_A y F_B comparten signo
            elementos['degenerada'] = (
                f"Elipse imaginaria: al dividir el lado derecho por A y B se obtienen valores "
                f"negativos (F_A = {formato_num(F_A)}, F_B = {formato_num(F_B)}), "
                "por lo tanto la ecuación no tiene puntos reales asociados."
            )
        else:
            F_A_abs = F_A
            F_B_abs = F_B

            if F_A_abs >= F_B_abs:  # Elipse horizontal
                a = F_A_abs ** 0.5
                b = F_B_abs ** 0.5
                c = max(0.0, F_A_abs - F_B_abs) ** 0.5

                elementos['vertices'] = [
                    (h - a, k), (h + a, k),
                    (h, k - b), (h, k + b)
                ]
                elementos['focos'] = [(h - c, k), (h + c, k)]
                elementos['a'] = a
                elementos['b'] = b
                elementos['c'] = c
                elementos['es_horizontal'] = True

                elementos['ejes_directriz_asintotas'] = [
                    {
                        'tipo': 'Eje mayor',
                        'eq_latex': f"y = {formato_num(k)}",
                        'val': k,
                        'orientacion': 'H'
                    },
                    {
                        'tipo': 'Eje menor',
                        'eq_latex': f"x = {formato_num(h)}",
                        'val': h,
                        'orientacion': 'V'
                    }
                ]
            else:  # Elipse vertical
                a = F_B_abs ** 0.5
                b = F_A_abs ** 0.5
                c = max(0.0, F_B_abs - F_A_abs) ** 0.5

                elementos['vertices'] = [
                    (h, k - a), (h, k + a),
                    (h - b, k), (h + b, k)
                ]
                elementos['focos'] = [(h, k - c), (h, k + c)]
                elementos['a'] = a
                elementos['b'] = b
                elementos['c'] = c
                elementos['es_horizontal'] = False

                elementos['ejes_directriz_asintotas'] = [
                    {
                        'tipo': 'Eje mayor',
                        'eq_latex': f"x = {formato_num(h)}",
                        'val': h,
                        'orientacion': 'V'
                    },
                    {
                        'tipo': 'Eje menor',
                        'eq_latex': f"y = {formato_num(k)}",
                        'val': k,
                        'orientacion': 'H'
                    }
                ]

    # 4. HIPÉRBOLA
    elif tipo == 'Hipérbola':
        h = -C / (2 * A) if A != 0 else 0.0
        k = -D / (2 * B) if B != 0 else 0.0
        LadoDerecho = -E + (C**2)/(4*A) + (D**2)/(4*B)

        F_A = LadoDerecho / A if A != 0 else 0.0
        F_B = LadoDerecho / B if B != 0 else 0.0

        if F_A > 0:  # Hipérbola horizontal
            a = F_A ** 0.5
            b = abs(F_B) ** 0.5
            c = (a**2 + b**2) ** 0.5

            elementos['centro_o_vertice'] = (h, k)
            elementos['vertices'] = [(h - a, k), (h + a, k)]
            elementos['focos'] = [(h - c, k), (h + c, k)]
            elementos['h'] = h
            elementos['k'] = k
            elementos['a'] = a
            elementos['b'] = b
            elementos['c'] = c
            elementos['es_horizontal'] = True

            pend = b / a if a != 0 else 0.0
            elementos['ejes_directriz_asintotas'] = [
                {
                    'tipo': 'Eje transverso',
                    'eq_latex': f"y = {formato_num(k)}",
                    'val': k,
                    'orientacion': 'H'
                },
                {
                    'tipo': 'Eje conjugado',
                    'eq_latex': f"x = {formato_num(h)}",
                    'val': h,
                    'orientacion': 'V'
                },
                {
                    'tipo': 'Asíntota 1',
                    'eq_latex': f"y - {formato_num(k)} = {formato_num(pend)}(x - {formato_num(h)})",
                    'pend': pend,
                    'signo': 1,
                    'orientacion': 'A'
                },
                {
                    'tipo': 'Asíntota 2',
                    'eq_latex': f"y - {formato_num(k)} = -{formato_num(pend)}(x - {formato_num(h)})",
                    'pend': pend,
                    'signo': -1,
                    'orientacion': 'A'
                }
            ]
        else:  # Hipérbola vertical
            a = F_B ** 0.5 if F_B > 0 else 0.0
            b = abs(F_A) ** 0.5
            c = (a**2 + b**2) ** 0.5

            elementos['centro_o_vertice'] = (h, k)
            elementos['vertices'] = [(h, k - a), (h, k + a)]
            elementos['focos'] = [(h, k - c), (h, k + c)]
            elementos['h'] = h
            elementos['k'] = k
            elementos['a'] = a
            elementos['b'] = b
            elementos['c'] = c
            elementos['es_horizontal'] = False

            pend = a / b if b != 0 else 0.0
            elementos['ejes_directriz_asintotas'] = [
                {
                    'tipo': 'Eje transverso',
                    'eq_latex': f"x = {formato_num(h)}",
                    'val': h,
                    'orientacion': 'V'
                },
                {
                    'tipo': 'Eje conjugado',
                    'eq_latex': f"y = {formato_num(k)}",
                    'val': k,
                    'orientacion': 'H'
                },
                {
                    'tipo': 'Asíntota 1',
                    'eq_latex': f"y - {formato_num(k)} = {formato_num(pend)}(x - {formato_num(h)})",
                    'pend': pend,
                    'signo': 1,
                    'orientacion': 'A'
                },
                {
                    'tipo': 'Asíntota 2',
                    'eq_latex': f"y - {formato_num(k)} = -{formato_num(pend)}(x - {formato_num(h)})",
                    'pend': pend,
                    'signo': -1,
                    'orientacion': 'A'
                }
            ]

    return elementos

def graficar_conica(A, B, C, D, E, mostrar_elementos=True):
    elementos = calcular_elementos_conica(A, B, C, D, E)
    cx, cy = elementos['centro_o_vertice']
    tipo_conica = elementos['tipo']

    # Determinar rango dinámico para que la curva sea visible
    rango = 15
    if elementos.get('degenerada') is None:
        if tipo_conica == 'Circunferencia':
            r = elementos.get('r', 0.0)
            if r > 0:
                rango = max(15, r * 1.3)
        elif tipo_conica == 'Elipse':
            a = elementos.get('a', 0.0)
            b = elementos.get('b', 0.0)
            rango = max(15, max(a, b) * 1.3)
        elif tipo_conica == 'Hipérbola':
            a = elementos.get('a', 0.0)
            b = elementos.get('b', 0.0)
            rango = max(15, max(a, b) * 1.5)
        elif tipo_conica == 'Parábola':
            p = abs(elementos.get('p', 0.0))
            if p > 0:
                rango = max(15, p * 4.0)

    pasos = 200
    x = [cx - rango + (2 * rango * i / pasos) for i in range(pasos + 1)]
    y = [cy - rango + (2 * rango * i / pasos) for i in range(pasos + 1)]

    Z = []
    for yi in y:
        fila = []
        for xi in x:
            z_val = A*(xi**2) + B*(yi**2) + C*xi + D*yi + E
            fila.append(z_val)
        Z.append(fila)

    figura = go.Figure()

    figura.add_trace(go.Contour(
        z=Z, x=x, y=y,
        contours=dict(start=0, end=0, size=2, coloring='lines'),
        line_width=3.5, line_color='#3b82f6',
        hoverinfo='none',
        showlegend=False
    ))

    figura.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#3b82f6', width=3.5),
        name='Cónica'
    ))

    if mostrar_elementos:
        h, k = elementos['centro_o_vertice']

        label_centro = 'Vértice (V)' if tipo_conica == 'Parábola' else 'Centro (C)'
        figura.add_trace(go.Scatter(
            x=[h], y=[k],
            mode='markers+text',
            marker=dict(size=12, color='#f59e0b', symbol='circle', line=dict(color='#ffffff', width=1)),
            text=[f" {label_centro}"],
            textposition="top right",
            name=label_centro
        ))

        if elementos['focos']:
            fx = [f[0] for f in elementos['focos']]
            fy = [f[1] for f in elementos['focos']]
            labels_focos = [" F"] if len(elementos['focos']) == 1 else [" F1", " F2"]
            figura.add_trace(go.Scatter(
                x=fx, y=fy,
                mode='markers+text',
                marker=dict(size=10, color='#10b981', symbol='diamond', line=dict(color='#ffffff', width=1)),
                text=labels_focos,
                textposition="bottom center",
                name='Foco(s)'
            ))

        if elementos['vertices'] and tipo_conica != 'Parábola':
            vx = [v[0] for v in elementos['vertices']]
            vy = [v[1] for v in elementos['vertices']]

            if tipo_conica == 'Circunferencia':
                labels_vert = [" V1", " V2", " V3", " V4"]
            elif tipo_conica == 'Elipse':
                labels_vert = [" V1 (P)", " V2 (P)", " B1 (S)", " B2 (S)"]
            else:
                labels_vert = [" V1", " V2"]

            figura.add_trace(go.Scatter(
                x=vx, y=vy,
                mode='markers+text',
                marker=dict(size=10, color='#ec4899', symbol='cross', line=dict(color='#ffffff', width=1)),
                text=labels_vert,
                textposition="middle right",
                name='Vértices'
            ))

        for ea in elementos['ejes_directriz_asintotas']:
            tipo_ea = ea['tipo']
            if ea['orientacion'] == 'H':
                val_y = ea['val']
                figura.add_trace(go.Scatter(
                    x=[cx - rango, cx + rango], y=[val_y, val_y],
                    mode='lines',
                    line=dict(dash='dash', color='#64748b', width=1.5),
                    name=tipo_ea
                ))
            elif ea['orientacion'] == 'V':
                val_x = ea['val']
                figura.add_trace(go.Scatter(
                    x=[val_x, val_x], y=[cy - rango, cy + rango],
                    mode='lines',
                    line=dict(dash='dash', color='#64748b', width=1.5),
                    name=tipo_ea
                ))
            elif ea['orientacion'] == 'A':
                pend = ea['pend']
                signo = ea['signo']
                y_asint = [k + signo * pend * (xi - h) for xi in x]
                figura.add_trace(go.Scatter(
                    x=x, y=y_asint,
                    mode='lines',
                    line=dict(dash='dot', color='#ef4444', width=1.5),
                    name=tipo_ea
                ))

    # Para la circunferencia, forzar escala igual en ambos ejes para que se vea circular
    yaxis_config = dict(
        zeroline=True, gridcolor='#334155', zerolinecolor='#94a3b8',
        range=[cy - rango, cy + rango]
    )
    if tipo_conica == 'Circunferencia':
        yaxis_config['scaleanchor'] = 'x'
        yaxis_config['scaleratio'] = 1

    figura.update_layout(
        title="Representación Gráfica de la Cónica y Elementos Geométricos",
        xaxis_title="Eje X", yaxis_title="Eje Y",
        width=700, height=650,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        xaxis=dict(zeroline=True, gridcolor='#334155', zerolinecolor='#94a3b8', range=[cx - rango, cx + rango]),
        yaxis=yaxis_config,
        showlegend=True
    )
    return figura
