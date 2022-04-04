from fastapi import APIRouter
from typing import List

from fastapi.exceptions import HTTPException

router = APIRouter()

from pydantic import BaseModel


class Item(BaseModel):
    item: str
    itemCategory: str
    quantity: int
    price: float


def tax_computation(value: int, category: str):
    '''
    Computes the taxes depending on category of commodities and their cost
    :param value: int
    :param category: str
    :return: taxes
    '''
    try:
        if category == 'Medicine':
            taxes = (value * 5) / 100
        elif category == 'Imported':
            taxes = (value * 18) / 100
        elif category == 'Book':
            taxes = 0
        elif category == 'Food':
            taxes = (value * 5) / 100
        elif category == 'Clothes':
            if value > 1000:
                taxes = 50 + ((value - 1000) * 12) / 100
            else:
                taxes = (value * 5) / 100
        elif category == 'Music':
            taxes = (value * 3) / 100
        else:
            return (None, "irrelevant category!")

    except Exception as exc:
        return (None, exc)

    return ("success", taxes)



@router.post("/compute_bill", tags=["all_in_one"])
async def compute_bill(item: List[Item]):
    '''
    Computes the total_cost and taxes depending on category of commodities and their cost
    :param item:
    :return:
    '''
    total_cost = 0
    total_tax = 0
    for every_item in item:
        every_item = dict(every_item)
        taxes = tax_computation(value=(every_item['quantity'] * every_item['price']),
                                category=every_item['itemCategory'])
        if taxes[0] is None:
            raise HTTPException(status_code=404, detail="Item Category not found")
        total_tax += taxes[1]
        total_cost += (every_item['quantity'] * every_item['price'])

    # Additionally, a 5% discount is applied by the store if the bill exceeds 2000INR.
    if total_cost > 2000:
        total_cost = (total_cost * 95) / 100

    return {"total_tax": total_tax, "total_cost": total_cost}
