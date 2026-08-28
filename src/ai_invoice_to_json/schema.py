import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CustomerDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contact_name: str = Field(description="Customer's contact name")
    address: str = Field(description="Customer address")
    city: str = Field(description="City")
    postal_code: Optional[str] = Field(default=None, description="Postal Code")
    country: str = Field(description="Country")
    phone: str = Field(description="Phone Number")
    fax: Optional[str] = Field(default=None, description="Fax Number")


class ProductDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: str = Field(description="Product ID")
    product_name: str = Field(description="Product Name")
    quantity: int = Field(description="Product ordered quantity")
    unit_price: Decimal = Field(
        description="Product unit price", decimal_places=2, max_digits=50
    )


class Invoice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    currency: Optional[str] = Field(
        default=None, description="ISO currency code, e.g. USD, EUR"
    )
    order_id: str = Field(description="Invoice's Order ID")
    customer_id: str = Field(description="Customer's ID")
    order_date: datetime.date = Field(description="Order date format:yyyy-mm-dd")
    customer_details: CustomerDetails = Field(description="Customer details model")
    products: list[ProductDetails] = Field(
        description="List of ordered product details"
    )
    total_price: Decimal = Field(
        description="Total price of ordered products", decimal_places=2, max_digits=50
    )

    # TODO: Better total price validation for real scenario rounding-related issues (taxes, discounts,..)
    @model_validator(mode="after")
    def validate_total_price(self):
        actual_total_price = sum([p.quantity * p.unit_price for p in self.products])
        if actual_total_price != self.total_price:
            raise ValueError(
                f"Total price incorrect! Expecting: {self.total_price}, received {actual_total_price}"
            )
        return self
