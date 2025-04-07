from typing import List, Tuple
from products import Product

class Store:
    """This class represents a store that holds and manages a list of products."""

    def __init__(self, products: List[Product]):
        """Initialize the store with a list of products"""
        if not isinstance(products, list):
            raise TypeError("Expected a list of products.")
        for product in products:
            if not isinstance(product, Product):
                raise TypeError("All items must be Product objects.")
        self.products = products

    def add_product(self, product: Product) -> None:
        """Add a product to the store"""
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """Remove a product from products list"""
        if product not in self.products:
            raise ValueError("Product not found in the list.")
        self.products.remove(product)

    def get_total_quantity(self) -> float:
        """Returns the sum of all Products."""
        total = 0
        for product in self.products:
            total += product.quantity
        return total

    def get_all_products(self) -> List[Product]:
        """Returns a list of all active products"""
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list: List[Tuple[Product, float]]) -> float:
        """Create a list with tuple (Product and quantity) and return the total price"""
        if not isinstance(shopping_list, list):
            raise TypeError("Expected shopping_list to be a list.")

        for item in shopping_list:
            if not (
                isinstance(item, tuple) and
                len(item) == 2 and
                isinstance(item[0], Product) and
                isinstance(item[1], (int, float))
            ):
                raise ValueError("Each item in shopping_list must be a tuple of (Product, quantity).")

        total = 0
        for product, quantity in shopping_list:
            try:
                total += product.buy(quantity)
            except ValueError as e:
                raise ValueError(f"Error ordering product {product.name}: {e}") from e
        return total
