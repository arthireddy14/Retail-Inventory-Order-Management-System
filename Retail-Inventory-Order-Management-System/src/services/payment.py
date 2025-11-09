from src.config import get_supabase
from typing import List,Dict,Optional
class PaymentError:
    pass
class Payment:
    def __init__(self,order_id:int,amount:float,status:str,pay_mode:str):
        self.order_id=order_id
        self.amount=amount
        self.status=status
        self.pay_mode=pay_mode
        pass
    def to_dict(self)->dict:
        return {
            "order_id":self.order_id,
            "amount":self.amount,
            "staus":self.status,
            "pay_mode":self.pay_mode
        }
class PaymentDAO:
    def __init__(self):
        self.sb=get_supabase()
        pass
    def create_payment(self,payment:"Payment")->dict:
        resp=self.sb.table("payments").insert(payment.to_dict).execute()
        return resp.data[0] if resp.data else None  
    def make_payment(self):
        resp=self.sb.table("payments").update({
            'status':paid,
            'method':method,
            'order_id':order_id
        }) 
        return resp.data[0] if resp.data else None   
    def refund_payment(self): 
        resp=self.sb.table("payments").update({
            "status":pending,
            "method":method,
            "customer_id":customer_id
        })