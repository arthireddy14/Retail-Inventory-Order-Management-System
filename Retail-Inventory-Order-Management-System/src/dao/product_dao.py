# # src/dao/product_dao.py
# from typing import Optional, List, Dict
# from src.config import get_supabase
# # from src.services.product_service import Product

# class ProductDAO:
#     def __init__(self):
#         self._sb=get_supabase()
#         pass
#     def _sb():
#         return get_supabase()
 
#     def create_product(self,product:"Product") -> Optional[Dict]:
#         """
#     Insert a product and return the inserted row (two-step: insert then select by unique sku).
#     """
#         payload = {"name": name, "sku": sku, "price": price, "stock": stock}
#         if category is not None:
#             payload["category"] = category
 
#     # Insert (no select chaining)
#         _sb().table("products1").insert(payload).execute()
 
#     # Fetch inserted row by unique column (sku)
#         resp = _sb().table("products1").select("*").eq("sku", sku).limit(1).execute()
#         return resp.data[0] if resp.data else None
 
#     def get_product_by_id(prod_id: int) -> Optional[Dict]:
#         resp = _sb().table("products1").select("*").eq("prod_id", prod_id).limit(1).execute()
#         return resp.data[0] if resp.data else None
 
#     def get_product_by_sku(sku: str) -> Optional[Dict]:
#         resp = _sb().table("products1").select("*").eq("sku", sku).limit(1).execute()
#         return resp.data[0] if resp.data else None
 
#     def update_product(prod_id: int, fields: Dict) -> Optional[Dict]:
#         """
#     Update and then return the updated row (two-step).
#     """
#         _sb().table("products1").update(fields).eq("prod_id", prod_id).execute()
#         resp = _sb().table("products1").select("*").eq("prod_id", prod_id).limit(1).execute()
#         return resp.data[0] if resp.data else None
 
#     def delete_product(prod_id: int) -> Optional[Dict]:
#     # fetch row before delete (so we can return it)
#         resp_before = _sb().table("products1").select("*").eq("prod_id", prod_id).limit(1).execute()
#         row = resp_before.data[0] if resp_before.data else None
#         _sb().table("products1").delete().eq("prod_id", prod_id).execute()
#         return row
 
#     def list_products(limit: int = 100, category: str | None = None) -> List[Dict]:
#         q = _sb().table("products1").select("*").order("prod_id", desc=False).limit(limit)
#         if category:
#             q = q.eq("category", category)
#         resp = q.execute()
#         return resp.data or []

from typing import Optional, List, Dict
from src.config import get_supabase
 
class ProductDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
        """
        Insert a product and return the inserted row.
        """
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category is not None:
            payload["category"] = category

        # Insert
        self._sb.table("products1").insert(payload).execute()

        # Fetch inserted row by unique SKU
        resp = self._sb.table("products1").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = self._sb.table("products1").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self._sb.table("products1").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update and return the updated row.
        """
        self._sb.table("products1").update(fields).eq("prod_id", prod_id).execute()
        resp = self._sb.table("products1").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete(self, prod_id: int) -> Optional[Dict]:
        """
        Delete a product and return the deleted row.
        """
        resp_before = self._sb.table("products1").select("*").eq("prod_id", prod_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("products1").delete().eq("prod_id", prod_id).execute()
        return row

    def list(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self._sb.table("products1").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []




 
 