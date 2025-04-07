class Product:
    """This class represents a product with name, price, quantity, and active status."""

    def __init__(self, name: str, price: float = 0.0, quantity: int = 0): #Constructor
        """Create a new product and check if the values are valid"""

        # check for string and not empty
        if not isinstance(name, str) or not name.strip():
            raise TypeError("Name must be a non-empty string.")

        # check for int or float and greater than 0
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be greater than 0.")

        #check for int and greater than 0
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def set_quantity(self, quantity: float) -> None:
        """Set a new quantity for the product. Deactivate it if quantity is 0."""
        if not isinstance(quantity, (int, float)):
            raise TypeError("Quantity must be a non-negative number.")
        if quantity < 0:
            raise ValueError("Quantity must be a non-negative number.")
        self.quantity = quantity
        if quantity == 0:
            self.deactivate()

    def activate(self) -> None:
        """Set the product as active."""
        self.active = True

    def deactivate(self) -> None:
        """Set the product as not active."""
        self.active = False

    def get_quantity(self) -> float:
        """Return the current quantity of the product."""
        return self.quantity

    def is_active(self) -> bool:
        """Return True if the product is active, otherwise False."""
        return self.active

    def show(self) -> str:
        """Return a string that shows the product details."""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity} (Active: {self.active})"

    def buy(self, quantity: float) -> float:
        """Buy a number of items. Update stock and return total price."""

        # Check if requested quantity is a positive number
        if not isinstance(quantity, (int, float)):
            raise TypeError("Quantity to buy must be a number.")

        if quantity <= 0:
            raise ValueError("Quantity to buy must be bigger than 0")

        # Check if enough items are in stock
        if quantity > self.quantity:
            raise ValueError("Not enough parts in stock to complete purchase.")

        # Subtract bought quantity (triggers deactivation automatically if quantity becomes 0)
        self.set_quantity(self.quantity - quantity)
        return quantity * self.price
