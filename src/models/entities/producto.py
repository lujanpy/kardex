class Producto():

    def __init__(self, codigo, nombre, descripcion, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        
    
        
        
    def to_json(self):
        return{
            "codigo":self.codigo,
            "nombre":self.nombre,
            "descripcion":self.descripcion,
            "precio":self.precio,
            "stock":self.stock
        }
