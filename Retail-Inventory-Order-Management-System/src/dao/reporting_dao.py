from src.config import get_supabase
class ReportingDAO:
    def __init__(self):
        self.sb=get_supabase()
        pass
    def top_selling_products(self, limit: int = 5) -> List[Dict]:
        """
        Returns top products by total quantity sold.
        """
        resp = self.sb.table("order_items") \
            .select("prod_id, sum(quantity) as total_qty") \
            .group("prod_id") \
            .order("total_qty", desc=True) \
            .limit(limit) \
            .execute()
        data = resp.data or []

        # Optionally, fetch product names
        for d in data:
            prod_resp = self.sb.table("products1").select("name").eq("prod_id", d["prod_id"]).limit(1).execute()
            d["name"] = prod_resp.data[0]["name"] if prod_resp.data else None
        return data

    def total_revenue_last_month(self) -> float:
        """
        Calculate total revenue in the last month.
        """
        today = datetime.today()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        resp = self.sb.table("orders") \
            .select("total_amount") \
            .gte("created_at", first_day_last_month) \
            .lte("created_at", last_day_last_month) \
            .execute()

        data = resp.data or []
        return sum(d["total_amount"] for d in data)

    def total_orders_per_customer(self) -> List[Dict]:
        """
        Returns total orders placed by each customer.
        """
        resp = self.sb.table("orders") \
            .select("customer_id, count(order_id) as total_orders") \
            .group("customer_id") \
            .execute()
        data = resp.data or []

        # Add customer names
        for d in data:
            cust_resp = self.sb.table("customers").select("name").eq("customer_id", d["customer_id"]).limit(1).execute()
            d["name"] = cust_resp.data[0]["name"] if cust_resp.data else None
        return data

    def frequent_customers(self, min_orders: int = 2) -> List[Dict]:
        """
        Returns customers with more than `min_orders` orders.
        """
        orders = self.total_orders_per_customer()
        return [o for o in orders if o["total_orders"] > min_orders]