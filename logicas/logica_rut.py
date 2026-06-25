def validar_rut(rut_str):
    rut_limpio = rut_str.replace(".", "").replace("-", "").upper().strip()

    if len(rut_limpio) < 2:
        return False, None, "RUT demasiado corto. Debe tener al menos un dígito y el verificador."

    cuerpo_crudo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    if not cuerpo_crudo.isdigit():
        return False, None, "El cuerpo del RUT debe contener solo números."

    if len(cuerpo_crudo) < 7 or len(cuerpo_crudo) > 8:
        return False, None, f"El cuerpo del RUT debe tener entre 7 y 8 dígitos (se ingresaron {len(cuerpo_crudo)})."

    if dv_ingresado not in "0123456789K":
        return False, None, "El dígito verificador debe ser un número del 0 al 9, o la letra K."

    cuerpo = cuerpo_crudo.zfill(8)
    cuerpo_invertido = cuerpo_crudo[::-1]

    multiplicadores = [2, 3, 4, 5, 6, 7]
    suma = 0
    pasos = []

    for i, digito in enumerate(cuerpo_invertido):
        mult = multiplicadores[i % 6]
        prod = int(digito) * mult
        suma += prod
        pasos.append({'digito': int(digito), 'mult': mult, 'prod': prod})

    mod11 = suma % 11
    dv_calculado_num = 11 - mod11

    if dv_calculado_num == 11:
        dv_esperado = '0'
        v_val = 11
        regla = "Como 11 − (suma mod 11) = 11, el DV es 0."
    elif dv_calculado_num == 10:
        dv_esperado = 'K'
        v_val = 10
        regla = "Como 11 − (suma mod 11) = 10, el DV es K."
    else:
        dv_esperado = str(dv_calculado_num)
        v_val = dv_calculado_num
        regla = f"Como 11 − (suma mod 11) = {dv_calculado_num}, el DV es {dv_esperado}."

    es_valido = (dv_esperado == dv_ingresado)

    res = {
        'cuerpo': cuerpo,
        'cuerpo_crudo': cuerpo_crudo,
        'dv_ingresado': dv_ingresado,
        'invertido': cuerpo_invertido,
        'pasos': pasos,
        'suma': suma,
        'mod11': mod11,
        'dv_calculado_num': dv_calculado_num,
        'dv_esperado': dv_esperado,
        'v_val': v_val,
        'regla': regla
    }
    return es_valido, res, None
