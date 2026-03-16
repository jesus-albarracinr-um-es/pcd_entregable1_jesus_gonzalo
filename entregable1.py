#En primer lugar, crearemos unas clases para definir los dos tipos de errores que podemos obtener durante los procesos existentes en Mi MiImperio
#Además, importaremos las librerías necesarias para hacer la enumeración de Clase y Ubicación
#A su vez importaremos las librerías para hacer la clase abstracta
from enum import Enum
from abc import ABCMeta, abstractmethod

class StockInsuficienteError(Exception):
    """Excepción lanzada cuando se intenta sacar más stock del disponible."""
    pass

class RepuestoNoEncontradoError(Exception):
    """Excepción lanzada cuando se busca un repuesto que no existe en el catálogo."""
    pass

class Clase(Enum):
	EJECUTOR = 0
	ECLIPSE = 1
	SOBERANO = 2

class Ubicacion(Enum):
	ENDOR = 0
	CUMULO_RAIMOS = 1
	NEBULOSA_KALIIDA = 2

class Repuesto():
	def __init__(self, nombre: str, proveedor: str, cantidad:int, precio: int): #Pondremos la opción de que inicialmente se puedan introducir una cantidad al añadir un nuevo producto
		self.nombre = nombre
		self.proveedor = proveedor
		self.cantidad = cantidad
		self.precio = precio
	
	def getInfoRepuesto(self):
		return f"Nombre: {self.nombre}, Proveedor: {self.proveedor}, Cantidad: {self.cantidad}, Precio: {self.precio}"

	def getCantidad(self):
		return self.cantidad
			
	def modificarCantidad(self, cantidad: int):
		if cantidad < 0 and abs(cantidad) > self.cantidad: 
			raise StockInsuficienteError(f"No hay suficiente stock del repuesto {self.nombre}. Cantidad actual en almacén ")
		self.cantidad += cantidad
		print(f"La cantidad del producto {self.nombre} ha sido modificada de {self.cantidad} unidades a {self.cantidad + cantidad} unidades.")

	def setCantidad(self, nuevaCantidad: int):
		self.cantidad = nuevaCantidad

	def getNombre(self):
		return self.nombre

