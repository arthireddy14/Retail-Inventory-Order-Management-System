from supabase import Client

class OrderDAO:
    def __init__(self, sb: Client):
        self._sb = sb

    # -------------------- Create Order --------------------
    def create_order(self, customer_id: int, items: list[dict]) -> dict:
        # Calculate total amount and check stock
        total_amount = 0
        for item in items:
            prod = self._sb.table("products").select("*").eq("product_id", item["prod_id"]).execute().data
            if not prod:
                raise ValueError(f"Product {item['prod_id']} not found")
            prod = prod[0]
            if prod["stock"] < item["quantity"]:
                raise ValueError(f"Insufficient stock for product {prod['name']}")
            total_amount += prod["price"] * item["quantity"]

        # Insert order
        order_resp = self._sb.table("orders").insert({
            "customer_id": customer_id,
            "total_amount": total_amount,
            "status": "PLACED"
        }).execute()

        if not order_resp.data:
            raise ValueError("Failed to create order")

        order_id = order_resp.data[0]["order_id"]

        # Insert order_items & deduct stock
        for item in items:
            self._sb.table("order_items").insert({
                "order_id": order_id,
                "product_id": item["prod_id"],
                "quantity": item["quantity"]
            }).execute()
            # Deduct stock
            self._sb.table("products").update({
                "stock": self._sb.table("products").select("stock").eq("product_id", item["prod_id"]).execute().data[0]["stock"] - item["quantity"]
            }).eq("product_id", item["prod_id"]).execute()

        return self.get_order_by_id(order_id)

    # -------------------- Fetch Order --------------------
    def get_order_by_id(self, order_id: int) -> dict:
        order = self._sb.table("orders").select("*").eq("order_id", order_id).execute().data
        if not order:
            return {}
        order = order[0]

        # Fetch customer info
        customer = self._sb.table("customers").select("*").eq("customer_id", order["customer_id"]).execute().data[0]

        # Fetch order items with product info
        order_items = self._sb.table("order_items").select("*").eq("order_id", order_id).execute().data
        for i in order_items:
            prod = self._sb.table("products").select("*").eq("product_id", i["product_id"]).execute().data[0]
            i["product_name"] = prod["name"]
            i["product_price"] = prod["price"]

        order["customer"] = customer
        order["items"] = order_items
        return order

    # -------------------- List Orders by Customer --------------------
    def list_orders_by_customer(self, customer_id: int) -> list[dict]:
        orders = self._sb.table("orders").select("*").eq("customer_id", customer_id).execute().data
        return [self.get_order_by_id(o["order_id"]) for o in orders]

    # -------------------- Cancel Order --------------------
    def cancel_order(self, order_id: int) -> dict:
        order = self._sb.table("orders").select("*").eq("order_id", order_id).execute().data
        if not order:
            raise ValueError("Order not found")
        order = order[0]

        if order["status"] != "PLACED":
            raise ValueError("Only orders with status PLACED can be cancelled")

        # Restore stock
        order_items = self._sb.table("order_items").select("*").eq("order_id", order_id).execute().data
        for i in order_items:
            prod = self._sb.table("products").select("*").eq("product_id", i["product_id"]).execute().data[0]
            self._sb.table("products").update({
                "stock": prod["stock"] + i["quantity"]
            }).eq("product_id", i["product_id"]).execute()

        # Update order status
        self._sb.table("orders").update({"status": "CANCELLED"}).eq("order_id", order_id).execute()

        return self.get_order_by_id(order_id)

    # -------------------- Complete Order --------------------
    def complete_order(self, order_id: int) -> dict:
        self._sb.table("orders").update({"status": "COMPLETED"}).eq("order_id", order_id).execute()
        return self.get_order_by_id(order_id)
