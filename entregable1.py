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

class Unidad(metaclass = ABCMeta):
	def __init__(self, id_combate: str, clave: int):
		self.id_combate = id_combate
		self.clave = clave

	@abstractmethod
	def devuelveInfo(self):
		pass

class Nave(Unidad):
	def __init__(self, id_combate: str, clave: int, nombre: str):
		super().__init__(id_combate, clave)

		self.nombre = nombre
		self.catalogo = {}

	def adquirirRepuestos(self, nombreRepuesto: str, cantidad: int):
		if nombreRepuesto in self.catalogo:
			self.catalogo[nombreRepuesto] += cantidad #Añadimos al stock ya existente en caso de que una nave ya tenga stock
		else:
			self.catalogo[nombreRepuesto] = cantidad

		print(f"Stock de la nave {self.nombre} actualizada: {self.catalogo[nombreRepuesto]}x '{nombreRepuesto}'.")	

class CazaEstelar(Nave):
	def __init__(self, id_combate:str, clave:int, nombre:str, dotacion: int):
		super().__init__(id_combate, clave, nombre)

		self.dotacion = dotacion

	def devuelveInfo(self):
		return f"Caza estelar: {self.nombre}, ID: {self.id_combate}, Clave: {self.clave}, Dotación: {self.dotacion}"
	
class NaveEstelar(Nave):
	def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion: int, pasaje: int, clase: Clase):
		super().__init__(id_combate, clave, nombre)

		self.tripulacion = tripulacion
		self.pasaje = pasaje
		self.clase = clase

	def devuelveInfo(self):
		return f"Nave Estelar: {self.nombre}, ID: {self.id_combate}, Clave: {self.clave}, Tripulación: {self.tripulacion}, Pasaje: {self.pasaje}, Clase: {self.clase}"
	
class EstacionEspacial(Nave):
	def __init__(self, id_combate:str, clave: int, nombre: str, tripulacion: int, pasaje: int, ubicacion: Ubicacion):
		super().__init__(id_combate, clave, nombre)

		self.tripulacion = tripulacion
		self.pasaje = pasaje
		self.ubicacion = ubicacion

	def devuelveInfo(self):
		return f"Estación Espacial: {self.nombre}, ID: {self.id_combate}, Clave: {self.clave}, Tripulación: {self.tripulacion}, Pasaje: {self.pasaje}, Ubicación: {self.ubicacion.name}"	

class Almacen():
	def __init__(self, nombre: str, localizacion: str):
		self.nombre = nombre
		self.localizacion = localizacion
		self.catalogo = {}

	def devuelveAlmacen(self):
		return f"Nombre: {self.nombre}, Localización: {self.localizacion}, Catálogo: {self.catalogo}"

	def anadirRepuesto(self, nuevo_repuesto):
		# Este método va dentro de la clase Almacen
		nombre_pieza = nuevo_repuesto.getNombre()
		# 1. Comprobamos si la pieza ya existe en el catálogo
		if nombre_pieza in self.catalogo:
            # Si existe, recuperamos la pieza antigua y le sumamos la cantidad de la nueva
			pieza_existente = self.catalogo[nombre_pieza]
			cantidad_a_sumar = nuevo_repuesto.getCantidad()
			
			pieza_existente.modificarCantidad(cantidad_a_sumar)
			print(f"[+] Stock actualizado: '{nombre_pieza}' ahora tiene {pieza_existente.getCantidad()} unidades en {self.nombre}.")
            
		else:
            # 2. Si no existe, la añadimos como una pieza totalmente nueva
			self.catalogo[nombre_pieza] = nuevo_repuesto
			print(f"[+] Repuesto '{nombre_pieza}' registrado por primera vez en {self.nombre}.")

	def buscarRepuesto(self, nombre_repuesto: str):
		if nombre_repuesto not in self.catalogo:
            # Lanzamos excepción si no existe
			raise RepuestoNoEncontradoError(f"El repuesto '{nombre_repuesto}' no se encuentra en el almacén '{self.nombre}'.")
		return self.catalogo[nombre_repuesto]
		
	def obtenerInventario(self):
		if len(self.catalogo) == 0:
			return "El almacén se encuentra vacío"
		else:
			for pieza in self.catalogo.values():
				print(pieza.getInfoRepuesto())

class MiImperio():
	def __init__(self):
		self.naves = []
		self.almacenes = []

	def anadirNave(self, nuevaNave: Nave):
		self.naves.append(nuevaNave)

	def consultarNaves(self):
		if not self.naves:
			print("No existen naves todavía")
		else:
			for nave in self.naves:
				print(nave.devuelveInfo())

	def anadirAlmacen(self, nuevoAlmacen: Almacen):
		self.almacenes.append(nuevoAlmacen)
		print(f"{nuevoAlmacen.nombre} añadido al Imperio")

	def consultarAlmacen(self, nombre:str):
		for almacen in self.almacenes:
			if (nombre == almacen.nombre):
				return almacen
		return f"El almacén {almacen} no ha sido encontrado"
			
	def listarStock(self):
		for almacen in self.almacenes:
			almacen.obtenerInventario()

	def anadirStock(self, nombre_almacen: str, repuesto: Repuesto):
        # Primero buscamos si el almacén existe en nuestro sistema
		almacen = self.consultarAlmacen(nombre_almacen)
        
		if almacen:
            # Si el almacén existe 
			almacen.anadirRepuesto(repuesto)
		else:
			print(f"Error: No se puede añadir stock. El almacén '{nombre_almacen}' no existe.")

	def sacarStock(self, nombre_almacen: str, nombre_pieza: str, cantidad: int):
		almacen = self.consultarAlmacen(nombre_almacen)
		if almacen:
			pieza = almacen.buscarRepuesto(nombre_pieza)
			
			if pieza and pieza.getCantidad() >= cantidad:
				pieza.modificarCantidad(-cantidad)
				print(f"Se han retirado {cantidad} unidades de {nombre_pieza}")
				return True
			else:
				print(f"Error: Stock insuficiente o pieza no encontrada en {nombre_almacen}")
				return False
		return False

	def transferirRepuestoANave(self, nombre_nave: str, nombre_almacen: str, nombre_pieza: str, cantidad: int):
        # TRATAMIENTO DE EXCEPCIONES MEDIANTE TRY-EXCEPT
		try:
            # 1. Buscamos el almacén
			almacen_destino = next((a for a in self.almacenes if a.nombre == nombre_almacen), None)
			if not almacen_destino:
				raise ValueError(f"El almacén '{nombre_almacen}' no existe.")

            # 2. Buscamos la nave
			nave_destino = next((n for n in self.naves if n.nombre == nombre_nave), None)
			if not nave_destino:
				raise ValueError(f"La nave '{nombre_nave}' no existe.")

            # 3. Intentamos buscar y restar la pieza (puede lanzar excepciones)
			pieza = almacen_destino.buscarRepuesto(nombre_pieza)
			pieza.modificarCantidad(-cantidad)
            
            # 4. Si todo va bien, se lo damos a la nave
			nave_destino.adquirirRepuestos(nombre_pieza, cantidad)
			print(f"Transferencia de {cantidad}x '{nombre_pieza}' completada con éxito.")
			
		except RepuestoNoEncontradoError as e:
			print(f"{e}")
		except StockInsuficienteError as e:
			print(f"{e}")
		except ValueError as e:
			print(f"{e}")

if __name__ == "__main__":
    print(" INICIANDO SISTEMA DE MANTENIMIENTO MI IMPERIO")

    # 1. Instanciación correcta de clases
    sistema = MiImperio()
    almacen_principal = Almacen("Almacen Central", "Estrella de la Muerte")
    sistema.anadirAlmacen(almacen_principal)

    caza = CazaEstelar("TIE-01", 1234, "Caza Interceptor", 1)
    sistema.anadirNave(caza)

    print("\n[INFO] Naves y almacenes instanciados correctamente.")
    print(caza.devuelveInfo())

    # 2. Añadimos stock inicial
    motor = Repuesto("Motor Hiperimpulsor", "Kuat", 5, 1000)
    sistema.anadirStock("Almacen Central", motor)
    almacen_principal.obtenerInventario()

    print("\n--- PRUEBAS DE EXCEPCIONES ---")
    # 3. Prueba Exitosa
    print("\nIntento 1: Transferir 2 motores al Caza (Debería funcionar)")
    sistema.transferirRepuestoANave("Caza Interceptor", "Almacen Central", "Motor Hiperimpulsor", 2)

    # 4. Prueba Excepción 1: Stock Insuficiente
    print("\nIntento 2: Transferir 10 motores al Caza (Debería fallar por stock)")
    sistema.transferirRepuestoANave("Caza Interceptor", "Almacen Central", "Motor Hiperimpulsor", 10)

    # 5. Prueba Excepción 2: Repuesto No Encontrado
    print("\nIntento 3: Transferir un 'Panel Solar' (Debería fallar por no existir)")
    sistema.transferirRepuestoANave("Caza Interceptor", "Almacen Central", "Panel Solar", 1)