# # src/cli/main.py
# import argparse
# import json
# from src.services.product_service import Product,ProductService,ProductError
# from src.dao.product_dao import ProductDAO 
# from src.dao.order_dao import OrderDAO
 
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()  # load .env variables

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

sb = create_client(url, key)


import argparse
import json
from src.services.product_service import ProductService,Product
from src.dao.product_dao import ProductDAO
from src.services.customer_service import CustomerService
from src.dao.customer_dao import CustomerDAO
from src.dao.order_dao import OrderDAO
from src.services.order_service import OrderService

dao=ProductDAO()
service=ProductService()
customer_dao = CustomerDAO(sb)
customer_service = CustomerService(customer_dao)
order_dao=OrderDAO(sb)
order_service=OrderService(order_dao)


 
def cmd_product_add(args):
    try:
        p = service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

 
def cmd_product_list(args):
    # ps = product_dao.list_products(limit=100)
    ps=dao.list(limit=100)
    print(json.dumps(ps, indent=2, default=str))
 
def cmd_customer_add(args):
    try:
        # c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
        c = customer_service.add_cust(args.name, args.email, args.phone, args.city)

        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_customer_list(args):
    try:
        customers = customer_service.list_cust()
        print(json.dumps(customers, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# def cmd_customer_get(args):
#     try:
#         c = customer_service.serach_cust(email=args.email,city=args.city)
#         print(json.dumps(c, indent=2, default=str))
#     except Exception as e:
#         print("Error:", e)
def cmd_customer_get(args):
    try:
        c = customer_service.get_customer(args.id)
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


# def cmd_customer_update(args):
#     try:
#         c = customer_service.update_cust(
#             args.id, args.name, args.email, args.phone, args.city
#         )
#         print("Updated customer:")
#         print(json.dumps(c, indent=2, default=str))
#     except Exception as e:
#         print("Error:", e)
def cmd_customer_update(args):
    try:
        c = customer_service.update_cust(
            cust_id=args.id,
            name=args.name,
            email=args.email,
            phone=args.phone,
            city=args.city
        )
        print("Updated customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


def cmd_customer_delete(args):
    try:
        customer_service.delete_cust(args.id)
        print(f"Customer {args.id} deleted successfully")
    except Exception as e:
        print("Error:", e)

 
# def cmd_order_create(args):
#     # items provided as prod_id:qty strings
#     items = []
#     for item in args.item:
#         try:
#             pid, qty = item.split(":")
#             items.append({"prod_id": int(pid), "quantity": int(qty)})
#         except Exception:
#             print("Invalid item format:", item)
#             return
#     try:
#         ord = order_service.create_order(args.customer, items)
#         print("Order created:")
#         print(json.dumps(ord, indent=2, default=str))
#     except Exception as e:
#         print("Error:", e)
 
# def cmd_order_show(args):
#     try:
#         o = order_service.get_order_details(args.order)
#         print(json.dumps(o, indent=2, default=str))
#     except Exception as e:
#         print("Error:", e)
 
# def cmd_order_cancel(args):
#     try:
#         o = order_service.cancel_order(args.order)
#         print("Order cancelled (updated):")
#         print(json.dumps(o, indent=2, default=str))
#     except Exception as e:
#         print("Error:", e)
def cmd_order_create(args):
    items = []
    for item in args.item:
        pid, qty = item.split(":")
        items.append({"prod_id": int(pid), "quantity": int(qty)})
    res = order_service.create_order(args.customer, items)
    print(json.dumps(res, indent=2, default=str))

def cmd_order_show(args):
    res = order_service.get_order_details(args.order)
    print(json.dumps(res, indent=2, default=str))

def cmd_order_cancel(args):
    res = order_service.cancel_order(args.order)
    print(json.dumps(res, indent=2, default=str))

def cmd_order_complete(args):
    res = order_service.complete_order(args.order)
    print(json.dumps(res, indent=2, default=str))

 
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")
 
    # product add/list
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
 
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)
 
    # customer add
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)


    # list
    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    # get
    getc = pcust_sub.add_parser("get")
    getc.add_argument("--id", type=int, required=True)
    getc.set_defaults(func=cmd_customer_get)

    # update
    updc = pcust_sub.add_parser("update")
    updc.add_argument("--id", type=int, required=True)
    updc.add_argument("--name")
    updc.add_argument("--email")
    updc.add_argument("--phone")
    updc.add_argument("--city")
    updc.set_defaults(func=cmd_customer_update)

    # delete
    delc = pcust_sub.add_parser("delete")
    delc.add_argument("--id", type=int, required=True)
    delc.set_defaults(func=cmd_customer_delete)

 
    # order
    # porder = sub.add_parser("order")
    # porder_sub = porder.add_subparsers(dest="action")
 
    # createo = porder_sub.add_parser("create")
    # createo.add_argument("--customer", type=int, required=True)
    # createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    # createo.set_defaults(func=cmd_order_create)
 
    # showo = porder_sub.add_parser("show")
    # showo.add_argument("--order", type=int, required=True)
    # showo.set_defaults(func=cmd_order_show)
 
    # cano = porder_sub.add_parser("cancel")
    # cano.add_argument("--order", type=int, required=True)
    # cano.set_defaults(func=cmd_order_cancel)
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty")
    createo.set_defaults(func=cmd_order_create)

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    cancelo = porder_sub.add_parser("cancel")
    cancelo.add_argument("--order", type=int, required=True)
    cancelo.set_defaults(func=cmd_order_cancel)

    completeo = porder_sub.add_parser("complete")
    completeo.add_argument("--order", type=int, required=True)
    completeo.set_defaults(func=cmd_order_complete)

 
    return parser
 
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)
 
if __name__ == "__main__":
    main()
 
