# from typing import List, Dict

 
# class ProductError(Exception):
#     pass
# class Product:
#     def __init__(self,name:str,sku:str,price:float,stock: int=0,category:str =None):
#         if price<=0:
#             raise ProductError("Price shold be greater than 0")
        
#         self.__name=name
#         self._sku=sku
#         self._price=price
#         self.__stock=stock
#         self.__category=category
#     def todict(self)->dict:
#         return{
#             "name":self.__name,
#             "sku":self._sku,
#             "price":self._price,
#             "stock":self.__stock,
#             "category":self.__category
#         }
        
#         pass
# class ProductService:
#     def __init__(self,pd1:ProductDAO):
#         self.pd1=pd1
#         pass
#     def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
#         """
#         Validate and insert a new product.
#         Raises ProductError on validation failure.
#         """
#         product=Product(name,sku,price,stock,category)
#         return self.pd1.create_product(product)
#         # pd1=ProductDAO()
#         # if price <= 0:
#         #     raise ProductError("Price must be greater than 0")
#         # existing = pd1.get_product_by_sku(sku)
#         # if existing:
#         #     raise ProductError(f"SKU already exists: {sku}")
#         # return pd1.create_product(name, sku, price, stock, category)
 
#     def restock_product(prod_id: int, delta: int) -> Dict:
#         if delta <= 0:
#             raise ProductError("Delta must be positive")
#         pd1=ProductDAO()
#         p = pd1.get_product_by_id(prod_id)
#         if not p:
#             raise ProductError("Product not found")
#         new_stock = (p.get("stock") or 0) + delta
#         return pd1.update_product(prod_id, {"stock": new_stock})
 
#     def get_low_stock(threshold: int = 5) -> List[Dict]:
#         pd1=ProductDAO()
#         allp = pd1.list_products(limit=1000)
#         return [p for p in allp if (p.get("stock") or 0) <= threshold]

from typing import List, Dict,Optional
# import src.dao.product_dao as product_dao
from src.dao.product_dao import ProductDAO
 
class ProductError(Exception):
    pass
class Product:
    def __init__(self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None, prod_id: Optional[int] = None):
        self.id = prod_id
        self.name = name
        self.sku = sku
        self.price = price
        self.stock = stock
        self.category = category

    def restock(self, delta: int):
        if delta <= 0:
            raise ValueError("Delta must be positive")
        self.stock += delta

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
        }


class ProductService:
    def add_product(self, product: Product) -> dict:
        if product.price <= 0:
            raise ProductError("Price must be greater than 0")
        existing = ProductDAO.get_by_sku(product.sku)
        if existing:
            raise ProductError(f"SKU already exists: {product.sku}")
        return ProductDAO.create(product)

    def restock_product(self, prod_id: int, delta: int) -> dict:
        p = ProductDAO.get_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")

        product = Product(**p)
        product.restock(delta)
        return ProductDAO.update(prod_id, {"stock": product.stock})

    def get_low_stock(self, threshold: int = 5) -> List[dict]:
        all_products = ProductDAO.list_all()
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]





 