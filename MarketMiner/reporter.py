import json

import MarketMiner.scrape as scrape


""" Guarda y lee archivos json para ejecutar reports de
según los datos del archivo json
"""
class ReportManager:
    def __init__(self, ruta:str):
        self.ruta = ruta # Ruta del archivo json
        self.data:list[dict] = None # Datos del archivo json
        self.reports:list[Report] = []
        self.read()
    

    def read(self):
        try:
            with open(self.ruta, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            self._update_reports()
            return self.data
        except FileNotFoundError:
            print("Creando archivo")
            with open(self.ruta, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=4)
            return None

        except Exception as e:
            print(f'Error al leer el archivo: {e}')
            return None

    def write(self, data:list[dict], update=True):
        try:
            with open(self.ruta, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            if update:
                self.data = data
                self._update_reports()
            return True
        except Exception as e:
            print(f'Error al escribir el archivo: {e}')
            return False
    
    # Escribe la información actual en el archivo json
    def update_file(self):
        self.write(self.data, update=False)

    def _update_reports(self):
        self.reports = []
        for item in self.data:
            self.reports.append(Report(item))
    
    def add(self, data:dict):
        self.data.append(data)
        self.update_file()
        self._update_reports()

    def clear_file(self):
        self.write([])
        self.data = []
        self.reports = []

    def run(self):
        # se pueden implementar hilos para ejecutar los reportes más rápido
        for report in self.reports:
            report.run()
            
        
    def __getitem__(self, index:int):
        return self.reports[index]
    def get(self, index:int, key:str=None):
        if key:
            return self.reports[index][key]
        return self.reports[index]
    
    # Cambia los datos de un reporte y actualiza el archivo json
    def set_by_dict(self, index:int, data:dict, update_file=True):
        self[index].set_data(data)
        if update_file:
            self.data[index] = data
            self.update_file()
    
    def set_by_key(self, index:int, key:str, value, update_file=True):
        data = self[index].data # obtener datos guardados en el Report
        data[key] = value # Cambiar el valor de la clave
        self[index].set_data(data) # Actualizar los datos del Report

        if update_file:
            self.data[index] = data # Actualizar los datos del archivo json
            self.update_file()



    def print(self):
        print(json.dumps(self.data, indent=4))



class Report:
    def __init__(self, data:dict):
        self.data = data
        self.ecommerce = None
        self.set_data()

    # Actualiza los datos del reporte, si no se ingresan los datos, se reutilizan los datos anteriores
    def set_data(self, data:dict=None):
        if data:
            self.data = data
        self.compute()


    def compute(self):
        self.set_ecommerce()
        self.name = self.data['name']
        self.query = self.data['query']
        self.product = self.data['product']
        self.reportPath = self.data['reportPath']

        
    def set_ecommerce(self):
        try:
            self.ecommerce = getattr(scrape, self.data['class'])() # Instancia de la clase

        except Exception as e:
            print(f'Error al crear el ecommerce: {e}')
            return False
    
    def run(self):
        if self.query:
            self.ecommerce.search_products(self.query)
        elif self.product:
            self.ecommerce.get_product_by_link(self.product)
        else:
            print("No hay datos para ejecutar el reporte")
            return False
        self.ecommerce.make_report(self.reportPath)
        self.ecommerce.clean_up()
        return True
        
    def __getitem__(self, key:str):
        return self.data[key]