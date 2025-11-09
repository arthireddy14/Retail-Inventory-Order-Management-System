from typing import Optional, List, Dict
from src.config import get_supabase
# class OrderError:
#     pass
# class Orderitem:
#     def __init__(self,prod_id,price,quantity):
#         self.prod_id=prod_id
#         self.price=price
#         self.quantity=quantity
#         pass
#     def to_dict(self)->dict:
#         return{
#             "product id":prod_id,
#             "price":price,
#             "quantity":quantity
#         }
# class Order:
#     def __init__(self,customer_id,items:List[items],status):
#         self.customer_id=customer_id
#         self.items=items
#         self.status=status
#         self.total=(self.quantity*self.price for item in items)
#         pass
#     def to_dict(self,item)->dict:
#         return{
#             "customer id":self.customer_id,
#             "item":List[item],
#         }
        
# class OrderDAO:
#     def __init__(self):
#         self.sb=get_supabase()
#         pass
#     def create_order(self,order:"Order")->dict:
#         order_payload=order.todict()
#         resp=self.sb.table("Order_items").insert(order_payload).execute()
#         if not resp.data:
#             raise Exception("Error")
#         for item in order.items:
#             prod_resp=self.sb.table("product1").select("*").eq("prod_id",item.product_id).limit(1).execute()
#             product = prod_resp.data[0] if prod_resp.data else None
#             if not product:
#                 raise Exception(f"Product {item.product_id} not found")
#             if product["stock"] < item.quantity:
#                 raise Exception(f"Not enough stock for product {product['name']}")
from typing import List
from src.dao.order_dao import OrderDAO
# from supabase import Client

class OrderService:
    def __init__(self, dao: OrderDAO):
        self.dao = dao

    # -------------------- Create --------------------
    def create_order(self, customer_id: int, items: List[dict]) -> dict:
        return self.dao.create_order(customer_id, items)

    # -------------------- Get Details --------------------
    def get_order_details(self, order_id: int) -> dict:
        return self.dao.get_order_by_id(order_id)

    # -------------------- List Orders --------------------
    def list_orders_of_customer(self, customer_id: int) -> List[dict]:
        return self.dao.list_orders_by_customer(customer_id)

    # -------------------- Cancel Order --------------------
    def cancel_order(self, order_id: int) -> dict:
        return self.dao.cancel_order(order_id)

    # -------------------- Complete Order --------------------
    def complete_order(self, order_id: int) -> dict:
        return self.dao.complete_order(order_id)

            
  
        