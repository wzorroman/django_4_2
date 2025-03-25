from django.test import TestCase
import datetime

from ...utils.dates import calculate_date_info


def test_fechas_validas_1():
    """Prueba con fechas válidas y verifica los resultados."""
    fecha_inicio = '2025-01-15'
    fecha_fin = '2025-01-30'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 16
    assert resultados['full_months'] == 0  # No hay meses completos
    assert resultados['saturdays'] == 2
    assert resultados['sundays'] == 2


def test_fechas_validas_2():
    """Prueba con fechas válidas y verifica los resultados."""
    fecha_inicio = '2025-02-01'
    fecha_fin = '2025-02-28'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 28
    assert resultados['full_months'] == 1
    assert resultados['saturdays'] == 4
    assert resultados['sundays'] == 4


def test_fechas_validas_3():
    """Prueba con fechas válidas y verifica los resultados."""
    fecha_inicio = '2025-02-21'
    fecha_fin = '2025-03-07'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 15
    assert resultados['full_months'] == 0
    assert resultados['saturdays'] == 2
    assert resultados['sundays'] == 2


def test_fechas_validas_4():
    """Prueba con fechas válidas y verifica los resultados."""
    fecha_inicio = '2025-04-12'
    fecha_fin = '2025-05-03'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 22
    assert resultados['full_months'] == 0
    assert resultados['saturdays'] == 4
    assert resultados['sundays'] == 3


def test_fechas_validas_5():
    """Prueba con fechas válidas y verifica los resultados."""
    fecha_inicio = '2025-01-15'
    fecha_fin = '2025-02-08'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 25
    assert resultados['full_months'] == 0  # No hay meses completos
    assert resultados['saturdays'] == 4
    assert resultados['sundays'] == 3


def test_fechas_mismo_dia():
    """Prueba cuando las fechas de inicio y fin son el mismo día."""
    fecha_inicio = '2024-03-10'
    fecha_fin = '2024-03-10'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)

    assert resultados['total_days'] == 1
    assert resultados['full_months'] == 0
    assert resultados['saturdays'] == 0 if datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date().weekday() != 5 else 1
    assert resultados['sundays'] == 0 if datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date().weekday() != 6 else 1


def test_fechas_inicio_fin_mes():
    """Prueba con fechas que son inicio y fin de mes."""
    fecha_inicio = '2024-05-01'
    fecha_fin = '2024-07-31'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 92
    assert resultados['full_months'] == 3
    assert resultados['saturdays'] == 13
    assert resultados['sundays'] == 13


def test_fecha_inicio_posterior():
    """Prueba cuando la fecha de inicio es posterior a la fecha de fin."""
    fecha_inicio = '2024-08-15'
    fecha_fin = '2024-08-01'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados is None  # Debería retornar None por el error


def test_formato_fecha_incorrecto():
    """Prueba con un formato de fecha incorrecto."""
    fecha_inicio = '15-09-2024'
    fecha_fin = '2024-09-30'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados is None  # Debería retornar None por el error


def test_anio_nuevo():
    """Prueba que cruza el año nuevo."""
    fecha_inicio = '2023-12-20'
    fecha_fin = '2024-01-10'
    resultados = calculate_date_info(fecha_inicio, fecha_fin)
    assert resultados['total_days'] == 22
    assert resultados['full_months'] == 0
    assert resultados['saturdays'] == 3
    assert resultados['sundays'] == 3
