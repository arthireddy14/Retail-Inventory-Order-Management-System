# from src.dao.customer_dao import Customer
from typing import Optional,List,Dict
class CustomerService:
    def __init__(self,cus_dao):
        self.dao=cus_dao
    def add_cust(self,name:str,email:str,phone:str,city:str)->Optional[Dict]:
        try:
            return self.dao.add_customer(name,email,phone,city)
        except Exception as e:
            print(f"Error in adding customer ")
            return None
    def list_cust(self)->List[Dict]:
        return self.dao.list_all()
    # def update_cust(self,phone:str|None=None,city:str|None=None)->Optional[Dict]:
    #     update=self.dao.update_cus(phone,city)
    #     if update:
    #         print("Successfully updated")
    #     else:
    #         print("Nothing to update")
    #     return update
    def update_cust(self, cust_id: int, name=None, email=None, phone=None, city=None):
        update_data = {}
        if name:
            update_data["name"] = name
        if email:
            update_data["email"] = email
        if phone:
            update_data["phone"] = phone
        if city:
            update_data["city"] = city

        if not update_data:
            print("Nothing to update")
            return {}

    # call DAO
        return self.dao.update_customer(cust_id, update_data)

    def delete_cust(self,cust_id:int)->bool:
        try:
            self.dao.delete_cus(cust_id)
        except Exception as e:
            print(f"Error in deleting the customer{e}")
            return False
    def serach_cust(self,email,city)->List[Dict]:
        res=self.dao.search_cus(email=email,city=city)
        if res:
            return res
        else:
            print("Not found")
            return[]
    def get_customer(self, cust_id: int) -> dict:
        res = self.dao.get_by_id(cust_id)
        if res:
            return res
        else:
            print(f"Customer with id {cust_id} not found")
        return {}

            
    