from typing import Optional,List,Dict
# Create a new customer with details → name, email, phone, city.
# Validate that email must be unique.
# If email already exists, show an error.
# Update a customer’s phone or city.
# Delete a customer:
# Allow deletion only if the customer has no orders.
# If orders exist, block deletion with an error message.
# List all customers.
# Search customer by email or city.

class CustomerDAO:
    # def  __init__(self,name:str,email:str,phone:int,city:str):
    #     self.name=name
    #     self.email=email
    #     self.phone=phone
    #     self.city=city
    # def to_dict(self):
    #     return{
    #         "name":self.name,
    #         "email":self.email,
    #         "phone":self.phone,
    #         "city":self.city
    #     }
    def __init__(self,sb):
        self._sb=sb
    def add_customer(self,name:str,email:str,phone:str,city:str)->Optional[Dict]:
        existing=self.get_byemail(email)
        if existing:
            raise Exception (f" Email {email} already exists")
        else:
            payload={"name":name,"email":email,"phone":phone,"city":city}
            self._sb.table("customers").insert(payload).execute()
            resp=self._sb.table("customers").select("*").eq("email",email).limit(1).execute()
            return resp.data[0] if resp.data else None
    def get_byemail(self,email:str)->Optional[Dict]:
        resp=self._sb.table("customers").select("*").eq("email",email).limit(1).execute()
        return resp.data[0] if resp.data else None
    def serach_cus(self,email:str|None=None,city:str|None=None)->List[Dict]:
            query=self._sb.table("customers").select("*")
            if email is not None:
                query=query.eq("email",email)
            if city is not None:
                query=query.eq("city",city)
            resp=query.execute()
            return resp.data
    def list_all(self)->List[Dict]:
        resp=self._sb.table("customers").select("*").execute()
        return resp.data
    def delete_cus(self, cust_id: int) -> None:
        """
        Delete a customer only if they have no orders.
        """
        # Check if orders exist
        resp = self._sb.table("orders").select("*").eq("cust_id", cust_id).limit(1).execute()
        if resp.data:
            raise Exception("Cannot delete customer with existing orders")

        self._sb.table("customers").delete().eq("cust_id", cust_id).execute()   
            
    # def update_cus(self,cust_id:int,phone:str| None=None,city:str|None=None)->Optional[Dict]:
    #     update_details={}
    #     if phone is not None:
    #         update_details["phone"]=phone
    #     if city is not None:
    #         update_details["city"]=city
    #     if not update_details:
    #         return None
    #     self._sb.table("customers").update(update_details).eq("cust_id",cust_id).execute()
    #     resp=self._sb.table("customers").select("*").eq("cust_id",cust_id).limit(1).execute()
    #     return resp.data[0] if resp.data else None
    def update_customer(self, cust_id: int, data: dict):
        resp = self._sb.table("customers").update(data).eq("cust_id", cust_id).execute()
        if resp.data:
            return resp.data[0]
        return {}

    def get_by_id(self, cust_id: int) -> dict:
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).execute()
        if resp.data:
            return resp.data[0]
        return {}

    