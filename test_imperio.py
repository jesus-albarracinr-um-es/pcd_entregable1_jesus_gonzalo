import pytest
# Importamos las clases y excepciones desde nuestro archivo principal entregable1.py
from entregable1 import (
    Repuesto, CazaEstelar, Almacen, MiImperio, 
    StockInsuficienteError, RepuestoNoEncontradoError
)

# Las fixtures nos permiten crear un estado base (naves, almacenes) 
# que se reinicia limpio para cada test, ahorrando código repetitivo.
@pytest.fixture
def sistema_base():
    sistema = MiImperio()
    almacen = Almacen("Almacen Central", "Estrella de la Muerte")
    caza = CazaEstelar("TIE-01", 1234, "Caza Interceptor", 1)
    
    sistema.anadirAlmacen(almacen)
    sistema.anadirNave(caza)
    
    return sistema, almacen, caza

# TESTS DE INSTANCIACIÓN

def test_creacion_repuesto():
    """Comprueba que un repuesto se inicializa con los valores correctos."""
    motor = Repuesto("Motor Hiperimpulsor", "Kuat", 5, 1000)
    assert motor.getNombre() == "Motor Hiperimpulsor"
    assert motor.getCantidad() == 5

def test_anadir_stock_almacen(sistema_base):
    """Comprueba que se añade stock correctamente a un almacén."""
    sistema, almacen, caza = sistema_base
    motor = Repuesto("Motor Hiperimpulsor", "Kuat", 10, 1000)
    
    almacen.anadirRepuesto(motor)
    pieza_recuperada = almacen.buscarRepuesto("Motor Hiperimpulsor")
    
    assert pieza_recuperada.getCantidad() == 10

def test_transferencia_exitosa(sistema_base):
    """Prueba el flujo completo de transferir una pieza de un almacén a una nave."""
    sistema, almacen, caza = sistema_base
    motor = Repuesto("Motor Hiperimpulsor", "Kuat", 10, 1000)
    almacen.anadirRepuesto(motor)
    
    # Realizamos la transferencia
    sistema.transferirRepuestoANave("Caza Interceptor", "Almacen Central", "Motor Hiperimpulsor", 2)
    
    # Comprobamos que el stock bajó en el almacén
    assert almacen.buscarRepuesto("Motor Hiperimpulsor").getCantidad() == 8
    # Comprobamos que la nave ahora tiene la pieza
    assert caza.catalogo["Motor Hiperimpulsor"] == 2

# --- TESTS DE EXCEPCIONES ---

def test_excepcion_repuesto_no_encontrado(sistema_base):
    """Verifica que salta la excepción correcta si buscamos una pieza que no existe."""
    sistema, almacen, caza = sistema_base
    
    with pytest.raises(RepuestoNoEncontradoError):
        almacen.buscarRepuesto("Panel Solar Inexistente")

def test_excepcion_stock_insuficiente():
    """Verifica que salta la excepción si intentamos sacar más stock del que hay."""
    motor = Repuesto("Motor Hiperimpulsor", "Kuat", 5, 1000)
    
    with pytest.raises(StockInsuficienteError):
        # Intentamos restar 10 cuando solo hay 5
        motor.modificarCantidad(-10)