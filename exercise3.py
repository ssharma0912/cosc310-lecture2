"""Exercise 3: Enforce a business rule.

Extend your Cart so invalid operations are rejected by the CART.

  ValueError        when qty < 1
  OutOfStockError   when the item's "available" field is False
  KeyError          when removing an item that is not in the cart

Then demonstrate each one with try/except.
"""

from exercise1 import load_menu


class OutOfStockError(Exception):
    """Raised when a customer tries to order an item that is unavailable."""
    pass


class Cart:
    def __init__(self) -> None:
        self.lines: list[dict] = []

    def add_item(self, item: dict, qty: int = 1) -> None:
        # TODO: validate FIRST, then mutate.
        #   if qty < 1:                 raise ValueError(...)
        #   if not item["available"]:   raise OutOfStockError(...)
        if qty < 1:
            raise ValueError(f"Quantity must be at least 1, got {qty}.")
        if not item.get("available", True):
            raise OutOfStockError(f"Item '{item['name']}' is currently out of stock.")

        for line in self.lines:
            if line["item_id"] == item["id"]:
                line["qty"] += qty
                return

        self.lines.append({
            "item_id": item["id"],
            "name": item["name"],
            "price": item["price"],
            "qty": qty,
        })

    def remove_item(self, item_id: int) -> None:
        for line in self.lines:
            if line["item_id"] == item_id:
                self.lines.remove(line)
                return
        
        raise KeyError(f"Item ID {item_id} is not in the cart.")
        
    def total(self) -> float:
        return round(sum(line["price"] * line["qty"] for line in self.lines), 2)

    def __repr__(self) -> str:
        return f"<Cart {len(self.lines)} items, ${self.total():.2f}>"


if __name__ == "__main__":
    menu = load_menu()
    gyoza = menu[1]           # available
    miso = menu[3]            # NOT available

    cart = Cart()

    # TODO: demonstrate each rejection with try/except and a readable message.
    # Example:
    # try:
    #     cart.add_item(gyoza, 0)
    # except ValueError as e:
    #     print(f"Rejected: {e}")

    # ValueError
    try:
        cart.add_item(gyoza, 0)
    except ValueError as e:
        print(f"Rejected: {e}")

    # OutOfStockError
    try:
        cart.add_item(miso, 1)
    except OutOfStockError as e:
        print(f"Rejected: {e}")

    # KeyError
    try:
        cart.remove_item(999)
    except KeyError as e:
        print(f"Rejected: {e}")