
#Se realiza llamado de las funciones para ser usadas en el Menu.

from Brillo import init_brillo
from Volumen import init_volumen
from Tareas import init_Tareas
class Menu:

    def __init__(self) :
        self.funciones = {}
        self.current_function = None
    
    def add_function(self,name_function,funct):
        self.funciones[name_function] = funct

    
    def init_function(self):
        if self.current_function:
            print(f"Iniciando ejecucion funcion")
            self.current_function()
        else:
            print("No existe ninguna funcion seleccionada")    
        
    def show_list_menu(self):
        print('Lista de funciones disponibles')
        for i,name_function in enumerate(self.funciones.keys(),start=1):
            print(f'{i}. Funcion {name_function}')

    def select_function(self):
       enumerate_list = list(self.funciones.keys())
       option_selected = int(input("Seleccione la funcion a ejectar: "))
       self.current_function = self.funciones[enumerate_list[option_selected-1]]
       


menu = Menu()
menu.add_function("brillito",init_brillo)
menu.add_function("volumen",init_volumen)
menu.add_function("Control de vista",init_Tareas)
menu.show_list_menu()
menu.select_function()
menu.init_function()


