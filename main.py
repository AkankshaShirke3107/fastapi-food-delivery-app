from fastapi import FastAPI, Query, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ------------------ DATA ------------------

menu = [
    {"id": 1, "name": "Pizza", "price": 250, "category": "Food", "is_available": True},
    {"id": 2, "name": "Burger", "price": 150, "category": "Food", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Pasta", "price": 200, "category": "Food", "is_available": False},
    {"id": 5, "name": "Ice Cream", "price": 100, "category": "Dessert", "is_available": True},
    {"id": 6, "name": "Sandwich", "price": 120, "category": "Food", "is_available": True}
]

orders = []
cart = []
order_counter = 1

# ------------------ MODELS ------------------

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=20)
    delivery_address: str = Field(min_length=5)
    order_type: str = "delivery"


class NewMenuItem(BaseModel):
    name: str = Field(min_length=2)
    price: int = Field(gt=0)
    category: str = Field(min_length=2)
    is_available: bool = True


class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


# ------------------ HELPERS ------------------

def find_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_total(price, quantity, order_type="delivery"):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total


# ------------------ DAY 1 ------------------

@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}


@app.get("/menu")
def get_menu():
    return {"items": menu, "total": len(menu)}


@app.get("/menu/summary")
def summary():
    available = [i for i in menu if i["is_available"]]
    unavailable = [i for i in menu if not i["is_available"]]
    categories = list(set([i["category"] for i in menu]))

    return {
        "total": len(menu),
        "available": len(available),
        "unavailable": len(unavailable),
        "categories": categories
    }


@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# ------------------ DAY 2 ------------------

@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_item(order.item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    if not item["is_available"]:
        raise HTTPException(400, "Item not available")

    total = calculate_total(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order


# ------------------ DAY 3 ------------------

@app.get("/menu/filter")
def filter_menu(category: Optional[str] = None,
                max_price: Optional[int] = None,
                is_available: Optional[bool] = None):

    result = menu

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return {"items": result, "count": len(result)}


# ------------------ DAY 4 CRUD ------------------

@app.post("/menu")
def add_item(item: NewMenuItem, response: Response):
    for i in menu:
        if i["name"].lower() == item.name.lower():
            raise HTTPException(400, "Item already exists")

    new_item = item.dict()
    new_item["id"] = len(menu) + 1

    menu.append(new_item)
    response.status_code = 201
    return new_item


@app.put("/menu/{item_id}")
def update_item(item_id: int,
                price: Optional[int] = None,
                is_available: Optional[bool] = None):

    item = find_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item


@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    menu.remove(item)
    return {"message": "Deleted successfully"}


# ------------------ DAY 5 CART ------------------

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    if not item["is_available"]:
        raise HTTPException(400, "Item not available")

    cart.append({"item": item, "quantity": quantity})
    return cart


@app.get("/cart")
def view_cart():
    total = sum(i["item"]["price"] * i["quantity"] for i in cart)
    return {"cart": cart, "total": total}


@app.delete("/cart/{item_id}")
def remove_cart(item_id: int):
    for c in cart:
        if c["item"]["id"] == item_id:
            cart.remove(c)
            return {"message": "Removed"}
    raise HTTPException(404, "Item not in cart")


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):
    global order_counter

    if not cart:
        raise HTTPException(400, "Cart is empty")

    total = sum(i["item"]["price"] * i["quantity"] for i in cart)

    new_order = {
        "order_id": order_counter,
        "customer": data.customer_name,
        "total": total
    }

    orders.append(new_order)
    cart.clear()
    order_counter += 1

    response.status_code = 201
    return new_order


# ------------------ DAY 6 ADVANCED ------------------

@app.get("/menu/search")
def search(keyword: str):
    result = [i for i in menu if keyword.lower() in i["name"].lower()]
    return {"results": result, "total_found": len(result)}


@app.get("/menu/sort")
def sort_menu(order: str = "asc"):
    return sorted(menu, key=lambda x: x["price"], reverse=(order == "desc"))


@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    total_pages = (len(menu) + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": menu[start:start + limit]
    }


@app.get("/menu/browse")
def browse(keyword: Optional[str] = None,
           order: str = "asc",
           page: int = 1,
           limit: int = 2):

    result = menu

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    result = sorted(result, key=lambda x: x["price"], reverse=(order == "desc"))

    start = (page - 1) * limit
    return result[start:start + limit]