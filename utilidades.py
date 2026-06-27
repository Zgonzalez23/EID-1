def formato_num(n):
    return int(n) if float(n).is_integer() else round(n, 4)

def formato_signo(n):
    return f"+ {formato_num(n)}" if n >= 0 else f"- {formato_num(abs(n))}"

def formato_primer_signo(n):
    return f"{formato_num(n)}" if n >= 0 else f"- {formato_num(abs(n))}"

def comparar_valores(input_str, real_val, tolerancia=0.05):
    input_clean = input_str.strip().lower().replace(" ", "")
    if not input_clean:
        return "Vacío"
    try:
        val = float(input_clean.replace(",", "."))
        if abs(val - real_val) < tolerancia:
            return "Correcto"
        return "Incorrecto"
    except ValueError:
        return "Formato inválido"

def validar_puntos_desordenados(u1_x, u1_y, u2_x, u2_y, r1, r2, tol=0.05):
    if not u1_x.strip() or not u1_y.strip() or not u2_x.strip() or not u2_y.strip():
        return "Vacío", "Vacío"
    try:
        ux1 = float(u1_x.replace(",", "."))
        uy1 = float(u1_y.replace(",", "."))
        ux2 = float(u2_x.replace(",", "."))
        uy2 = float(u2_y.replace(",", "."))
        
        rx1, ry1 = r1
        rx2, ry2 = r2
        
        # Escenario A: P1 -> R1 y P2 -> R2
        errA1 = abs(ux1 - rx1) + abs(uy1 - ry1)
        errA2 = abs(ux2 - rx2) + abs(uy2 - ry2)
        
        # Escenario B: P1 -> R2 y P2 -> R1
        errB1 = abs(ux1 - rx2) + abs(uy1 - ry2)
        errB2 = abs(ux2 - rx1) + abs(uy2 - ry1)
        
        if (errA1 < tol and errA2 < tol) or (errB1 < tol and errB2 < tol):
            return "Correcto", "Correcto"
        else:
            # Validar de forma independiente para guiar al estudiante
            d1_r1 = abs(ux1 - rx1) + abs(uy1 - ry1)
            d1_r2 = abs(ux1 - rx2) + abs(uy1 - ry2)
            d2_r1 = abs(ux2 - rx1) + abs(uy2 - ry1)
            d2_r2 = abs(ux2 - rx2) + abs(uy2 - ry2)
            
            s1 = "Correcto" if min(d1_r1, d1_r2) < tol else "Incorrecto"
            s2 = "Correcto" if min(d2_r1, d2_r2) < tol else "Incorrecto"
            return s1, s2
    except ValueError:
        return "Formato inválido", "Formato inválido"

def comparar_limite(input_str, exact_val, tolerancia=0.05):
    input_clean = input_str.strip().lower().replace(" ", "")
    if not input_clean:
        return "Vacío"
        
    if exact_val == "-infinito":
        if input_clean in ["-infinito", "-inf", "-oo", r"-\infty", r"-\inf"]:
            return "Correcto"
        return "Incorrecto"
        
    elif exact_val == "+infinito":
        if input_clean in ["+infinito", "+inf", "+oo", "infinito", "inf", "oo", r"+\infty", r"\infty", r"+\inf"]:
            return "Correcto"
        return "Incorrecto"
        
    else:
        try:
            val = float(input_clean.replace(",", "."))
            if abs(val - exact_val) < tolerancia:
                return "Correcto"
            return "Incorrecto"
        except ValueError:
            return "Formato inválido"
