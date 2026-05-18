def formato_num(n):
    return int(n) if float(n).is_integer() else round(n, 4)

def formato_signo(n):
    return f"+ {formato_num(n)}" if n >= 0 else f"- {formato_num(abs(n))}"

def formato_primer_signo(n):
    return f"{formato_num(n)}" if n >= 0 else f"- {formato_num(abs(n))}"
