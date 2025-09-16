"""
def get_name_with_age(name: str, age: int | str):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


print(get_name_with_age("john", 9))



def process_items(items:list[str]):
    for item in items:
        print(item)


from typing import Optional


def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
say_hi()

"""
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
app = FastAPI()

cash_list = [
    {"amount": 150, "shape": "paper", "currency":"usd","id": 1},
    {"amount": 1500, "shape": "paper", "currency":"eur","id": 2}
]
class Cash(BaseModel):
    amount: int
    shape : str
    currency:str
@app.get("/cash")

def get_cash():
    return cash_list

@app.post("/cash")
def add_cash(cash:Cash):
    cash_dict = cash.dict()
    cash_dict['id'] = randrange(0,1000)
    cash_list.append(cash_dict)
    return {"data":cash_list}
 