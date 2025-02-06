import calendar


def contar_dias_sabados_domingos(mes: int, anio: int) -> dict:
    # Validar si el año es bisiesto
    es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    # Obtener el número de días en el mes
    num_dias = calendar.monthrange(anio, mes)[1]

    # Contadores para sábados y domingos
    sabados = 0
    domingos = 0

    # Contar sábados y domingos en el mes dado
    for dia in range(1, num_dias + 1):
        dia_semana = calendar.weekday(anio, mes, dia)
        if dia_semana == 5:  # Sábado
            sabados += 1
        elif dia_semana == 6:  # Domingo
            domingos += 1

    data = {
        'num_dias': num_dias,
        'sabados': sabados,
        'domingos': domingos,
        'es_bisiesto': es_bisiesto
    }
    return data
