from products import Product
from store import Store
# setup initial stock of inventory0704
product_list = [ Product("MacBook Air M2", price=1450, quantity=100),
                 Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 Product("Google Pixel 7", price=500, quantity=500)
               ]
best_buy = Store(product_list)

def start(store: Store) -> None:
    """
    Start the store program.
    Shows a menu with options to view products, total quantity,
    make an order, or quit the program.
    """
    while True:
        print("\nPlease choose an option:")
        print("1. List of all products in the store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Enter your choice number (1-4): ")

        if choice not in["1", "2", "3", "4"]:
            print("Invalid input. Please enter a number from 1 to 4.")
            continue

        if choice == "1":
            # show all products including inactive ones
            for product in store.products:
                print(product.show())

        elif choice == "2":
            # Display total quantity of all products
            print("Total quantity in store:", store.get_total_quantity())

        elif choice == "3":
            # Allow user to make an order one by one
            order_list = []  # Collect (Product, quantity) tuples

            while True:
                planned_quantities = {}
                for prod, qty in order_list:
                    planned_quantities[prod] = planned_quantities.get(prod, 0) + qty

                # Show all products including inactive ones
                print("\nAvailable products:")
                products_for_order = store.products  # include all products
                for index, product in enumerate(products_for_order, start=1):
                    planned = planned_quantities.get(product, 0)
                    available = product.get_quantity() - planned
                    if available <= 0:
                        product.deactivate()
                    print(f"{index}. {product.name} (Quantity available: {available}, Active: {product.is_active()})")

                # Check if all products are unavailable
                if all(product.get_quantity() - planned_quantities.get(product, 0) <= 0 for product in products_for_order):
                    if order_list:
                        # process the order immediately
                        try:
                            total = store.order(order_list)
                            print("\nOrder successful! Summary:")
                            print(f"{'Product':30} {'Unit Price':>12} {'Quantity':>10} {'Subtotal':>12}")
                            for product, quantity in order_list:
                                subtotal = product.price * quantity
                                print(f"{product.name:30} {product.price:12} €{quantity:10} {subtotal:12} €")
                            print("-" * 70)
                            print(f"{'Total':>54} {total:12} €")
                        except Exception as e:
                            raise RuntimeError("Order failed") from e
                    else:
                        print("No products are available for ordering at this time.")
                    break

                # choose product index
                index_input = input("Enter the product number you want to order (or 'q' to cancel): ").strip()
                if index_input.lower() == 'q':
                    print("Order cancelled.")
                    break
                if not index_input.isdigit():
                    print("Invalid input. Please enter a valid number.")
                    continue

                index = int(index_input)
                if index < 1 or index > len(products_for_order):
                    print("Product index out of range.")
                    continue

                selected_product = products_for_order[index - 1]

                if selected_product.get_quantity() <= 0 or not selected_product.is_active():
                    print(f"Sorry, {selected_product.name} is not available.")
                    continue

                # choose quantity
                while True:
                    if not selected_product.is_active():
                        print(f"The product '{selected_product.name}' is inactive and cannot be ordered.")
                        continue

                    planned = planned_quantities.get(selected_product, 0)
                    available = selected_product.get_quantity() - planned
                    quantity_input = input(f"Enter quantity for {selected_product.name} "
                                           f"(or 'q' to cancel): ").strip()
                    if quantity_input.lower() == "q":
                        print("Order cancelled.")
                        return
                    if not quantity_input.isdigit():
                        print("Invalid quantity. Please enter a number.")
                        continue

                    quantity = int(quantity_input)

                    if quantity > available:
                        print(f"Not enough quantity in stock. Maximum available is {available}. "
                              f"Please enter a smaller amount.")
                        continue

                    break  # valid quantity

                order_list.append((selected_product, quantity))

                # Ask if the user wants to add another product
                another_product = input("Would you like to add another product? (y/n): ").strip().lower()
                if another_product == 'n':
                    # process the order
                    try:
                        total = store.order(order_list)
                        print("\nOrder successful! Summary:")
                        print(f"{'Product':30} {'Unit Price':>12} {'Quantity':>10} {'Subtotal':>12}")
                        for product, quantity in order_list:
                            subtotal = product.price * quantity
                            print(f"{product.name:30} {product.price:12} €{quantity:10} "
                                  f"{subtotal:12} €")
                        print("-" * 70)
                        print(f"{'Total':>54} {total:12} €")
                    except Exception as e:
                        raise RuntimeError("Order failed") from e
                    break

        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    """ 
    Main entry point of the program. 
    Starts the store program and handles keyboard interruption.
    """
    try:
        start(best_buy)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")