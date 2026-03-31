Feature: Shop logic testing

  Scenario: Adding zero amount of product
    Given An empty shopping cart
    And A product "Apple" with price 10 and stock 100
    When I try to add 0 items of "Apple" to the cart
    Then I should get an error

  Scenario: Adding exactly all available stock
    Given An empty shopping cart
    And A product "Laptop" with price 1000 and stock 5
    When I add product "Laptop" to the cart in amount 5
    Then Product is added successfully

  Scenario: Calculate total price for multiple products
    Given An empty shopping cart
    And A product "Phone" with price 500 and stock 10
    And A product "Case" with price 20 and stock 50
    When I add product "Phone" to the cart in amount 1
    And I add product "Case" to the cart in amount 2
    Then The total price should be 540

  Scenario: Remove product from cart
    Given An empty shopping cart
    And A product "Watch" with price 100 and stock 10
    When I add product "Watch" to the cart in amount 1
    And I remove product "Watch" from the cart
    Then The cart should be empty

  Scenario: Stock decreases after placing order
    Given An empty shopping cart
    And A product "SSD" with price 80 and stock 10
    When I add product "SSD" to the cart in amount 3
    And I place the order
    Then The product "SSD" should have 7 items left

  Scenario: Attempt to buy more than available
    Given A product "Monitor" with price 200 and stock 2
    When I try to buy 3 items of "Monitor"
    Then I should get an error

  Scenario: Empty cart after order submission
    Given An empty shopping cart
    And A product "RAM" with price 50 and stock 5
    When I add product "RAM" to the cart in amount 1
    And I place the order
    Then The cart should be empty

  Scenario: Adding negative amount of product
    Given A product "Keyboard" with price 30 and stock 10
    When I try to add -5 items of "Keyboard" to the cart
    Then I should get an error

  Scenario: Check if product is available
    Given A product "Mouse" with price 15 and stock 1
    Then The product "Mouse" should be available for amount 1
    And The product "Mouse" should not be available for amount 2

  Scenario: Adding the same product twice updates amount
    Given An empty shopping cart
    And A product "Cable" with price 5 and stock 10
    When I add product "Cable" to the cart in amount 2
    And I add product "Cable" to the cart in amount 3
    Then The total price should be 25