import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class Product:
    name: str
    description: str = ""
    price: float = 0.0
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative.")

    def to_dict(self):
        """Converts the Product object to a dictionary, with datetimes as ISO strings."""
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Product object from a dictionary, with ISO strings for datetimes."""
        return cls(
            uuid=data.get("uuid", str(uuid.uuid4())),
            name=data["name"], # Name is required
            description=data.get("description", ""),
            price=float(data.get("price", 0.0)),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(timezone.utc),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.now(timezone.utc),
        )

if __name__ == '__main__':
    # Example Usage:
    try:
        # Create a new product
        product1 = Product(name="Super Gadget", description="A very useful gadget.", price=29.99)
        print("Created Product 1 (dict):", product1.to_dict())

        # Create another product with minimal info
        product2 = Product(name="Basic Widget")
        print("Created Product 2 (dict):", product2.to_dict())

        # Simulate loading from a dict (e.g., from JSON)
        product1_data_for_storage = product1.to_dict()
        loaded_product1 = Product.from_dict(product1_data_for_storage)
        print("Loaded Product 1 (object):", loaded_product1)
        print("Loaded Product 1 (name):", loaded_product1.name)
        print("Loaded Product 1 matches original:", loaded_product1.uuid == product1.uuid)

        # Example of a product with a negative price (should raise ValueError)
        # product_invalid = Product(name="Bad Price Item", price=-5.00)
        # print(product_invalid)

    except ValueError as e:
        print(f"Error: {e}")
