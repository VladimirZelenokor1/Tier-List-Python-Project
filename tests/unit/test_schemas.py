import unittest
from pydantic import ValidationError
from backend.schemas import (
    UserCreate,
    UserResponse,
    ItemCreate,
    Item,
    TierListItem,
    TemplateCreate,
    Template,
    TierList
)


class SchemasTestCase(unittest.TestCase):

    def test_user_create_valid(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        user = UserCreate(**data)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.password, "password123")

    def test_user_create_invalid_email(self):
        data = {
            "name": "John Doe",
            "email": "invalid_email",
            "password": "password123"
        }
        with self.assertRaises(ValidationError):
            UserCreate(**data)

    def test_user_response_valid(self):
        data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        }
        user = UserResponse(**data)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")

    def test_item_create_valid(self):
        data = {
            "name": "Item 1",
            "description": "Description of Item 1",
            "price": 10,
            "picture": b"image_data"
        }
        item = ItemCreate(**data)
        self.assertEqual(item.name, "Item 1")
        self.assertEqual(item.description, "Description of Item 1")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.picture, b"image_data")

    def test_item_valid(self):
        data = {
            "name": "Item 1",
            "description": "Description of Item 1",
            "price": 10,
            "picture": b"image_data",
            "id": 1
        }
        item = Item(**data)
        self.assertEqual(item.name, "Item 1")
        self.assertEqual(item.description, "Description of Item 1")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.picture, b"image_data")
        self.assertEqual(item.id, 1)

    def test_tier_list_item_valid(self):
        data = {
            "item_id": 1,
            "tier": "Tier 1"
        }
        tier_list_item = TierListItem(**data)
        self.assertEqual(tier_list_item.item_id, 1)
        self.assertEqual(tier_list_item.tier, "Tier 1")

    def test_template_create_valid(self):
        data = {
            "name": "Template 1",
            "picture": b"image_data",
            "items": [1, 2, 3]
        }
        template_create = TemplateCreate(**data)
        self.assertEqual(template_create.name, "Template 1")
        self.assertEqual(template_create.picture, b"image_data")
        self.assertEqual(template_create.items, [1, 2, 3])

    def test_template_valid(self):
        data = {
            "id": 1,
            "name": "Template 1",
            "picture": b"image_data",
            "items": []
        }
        template = Template(**data)
        self.assertEqual(template.id, 1)
        self.assertEqual(template.name, "Template 1")
        self.assertEqual(template.picture, b"image_data")
        self.assertEqual(template.items, [])

    def test_tier_list_valid(self):
        data = {
            "id": 1,
            "template": Template(id=1,
                                 name="Template 1",
                                 picture=b"image_data"),
            "items": []
        }
        tier_list = TierList(**data)
        self.assertEqual(tier_list.id, 1)
        self.assertEqual(tier_list.template.id, 1)
        self.assertEqual(tier_list.template.name, "Template 1")
        self.assertEqual(tier_list.template.picture, b"image_data")
        self.assertEqual(tier_list.items, [])


if __name__ == '__main__':
    unittest.main()
