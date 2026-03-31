from behave import given, when, then
from app.eshop import Product, ShoppingCart # ЗМІНЕНО ІМПОРТ

def ensure_context_initialized(context):
    if not hasattr(context, 'products'): context.products = {}
    if not hasattr(context, 'cart'): context.cart = ShoppingCart()

@given('An empty shopping cart')
def step_impl(context):
    ensure_context_initialized(context)
    context.cart = ShoppingCart()

@given('A product "{name}" with price {price:d} and stock {stock:d}')
def step_impl(context, name, price, stock):
    ensure_context_initialized(context)
    product = Product(name, price, stock)
    context.products[name] = product

@when('I try to add {amount:d} items of "{name}" to the cart')
def step_impl(context, amount, name):
    ensure_context_initialized(context)
    try:
        context.cart.add_product(context.products[name], amount)
        context.error_occurred = False
    except (ValueError, AttributeError):
        context.error_occurred = True

@when('I add product "{name}" to the cart in amount {amount:d}')
def step_impl(context, name, amount):
    ensure_context_initialized(context)
    context.cart.add_product(context.products[name], amount)

@then('I should get an error')
def step_impl(context):
    assert getattr(context, 'error_occurred', False) is True

@then('Product is added successfully')
def step_impl(context):
    assert len(context.cart.products) > 0

@then('The total price should be {total:d}')
def step_impl(context, total):
    assert context.cart.calculate_total() == total

@when('I remove product "{name}" from the cart')
def step_impl(context, name):
    context.cart.remove_product(context.products[name])

@then('The cart should be empty')
def step_impl(context):
    assert len(context.cart.products) == 0

@when('I place the order')
def step_impl(context):
    context.cart.submit_cart_order()

@then('The product "{name}" should have {expected_stock:d} items left')
def step_impl(context, name, expected_stock):
    assert context.products[name].available_amount == expected_stock

@when('I try to buy {amount:d} items of "{name}"')
def step_impl(context, amount, name):
    ensure_context_initialized(context)
    try:
        context.products[name].buy(amount)
        context.error_occurred = False
    except ValueError:
        context.error_occurred = True

@then('The product "{name}" should be available for amount {amount:d}')
def step_impl(context, name, amount):
    ensure_context_initialized(context)
    assert context.products[name].is_available(amount) is True

@then('The product "{name}" should not be available for amount {amount:d}')
def step_impl(context, name, amount):
    ensure_context_initialized(context)
    assert context.products[name].is_available(amount) is False