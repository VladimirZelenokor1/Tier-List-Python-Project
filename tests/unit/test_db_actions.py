import unittest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db_actions import User, Template, TierList, TierListItem, Item
from backend.db_actions import (
    get_user,
    create_user,
    create_template,
    get_all_templates,
    get_template,
    create_item,
    get_tierlist_item,
    delete_tierlist_item,
    get_item, get_tierlist,
    get_all_tierlists,
    get_tierlist_by_id,
    create_tierlist,
    rank_tierlist_item
)
from backend.schemas import UserCreate


class TestDBActions(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=engine)()

    def test_get_user(self):
        mock_session = mock.create_autospec(self.Session)

        (mock_session.query.return_value.filter.return_value
         .first).return_value = User(id=1,
                                     name='Ivan',
                                     email="test@example.com")

        result = get_user("test@example.com", mock_session)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "test@example.com")

    def test_create_user(self):
        # Mocking the self.Session class
        mock_session = mock.create_autospec(self.Session)

        user_create = UserCreate(name='Ivanov Ivan',
                                 email="test@example.com",
                                 password="password")
        result = create_user(mock_session, user_create)

        # Assert that the user was created correctly
        self.assertIsInstance(result, User)
        self.assertEqual(result.name, "Ivanov Ivan")
        self.assertEqual(result.email, "test@example.com")
        self.assertIsNotNone(result.password)

    def test_create_template(self):
        # Mocking the self.Session class
        mock_session = mock.create_autospec(self.Session)

        template_name = "Test Template"
        items = [1, 2, 3]
        picture = b"test_picture"

        # Mocking the query result
        mock_session.query.return_value.where.return_value = \
            [Item(id=1), Item(id=2), Item(id=3)]

        result = create_template(template_name, items, picture, mock_session)

        # Assert that the template was created correctly
        self.assertIsInstance(result, Template)
        self.assertEqual(result.name, template_name)
        self.assertEqual(result.picture, picture)
        self.assertEqual(len(result.items), 3)

    def test_get_all_templates(self):
        # Mocking the self.Session class
        mock_session = mock.create_autospec(self.Session)

        # Mocking the query result
        mock_session.query.return_value.all.return_value = \
            [Template(id=1, name="Template 1"),
             Template(id=2, name="Template 2")]

        result = get_all_templates(mock_session)

        # Assert that the correct templates were returned
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Template 1")
        self.assertEqual(result[1].name, "Template 2")

    def test_get_template(self):
        mock_session = mock.create_autospec(self.Session)
        (mock_session.query.return_value.filter_by
         .return_value.first).return_value = Template(id=1, name="Template 1")

        result = get_template(1, mock_session)

        # Assert that the correct templates were returned
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Template 1")

    def test_create_item(self):
        mock_session = mock.create_autospec(self.Session)

        name = "Test Item"
        description = "Test Item Descr"
        price = 100
        picture = b"test_picture"

        result = create_item(name, description, price, picture, mock_session)

        # Assert that the template was created correctly
        self.assertIsInstance(result, Item)
        self.assertEqual(result.name, name)
        self.assertEqual(result.picture, picture)

    def test_get_tierlist_item(self):
        mock_session = mock.create_autospec(self.Session)
        mock_session.query.return_value.filter.return_value.first.return_value\
            = (TierListItem(tier_list_id=1, item_id=2, tier="S"))

        result = get_tierlist_item(2, 1, mock_session)

        # Assert that the correct templates were returned
        self.assertEqual(result.tier, "S")

    def test_rank_tierlist_item_new_item(self):
        mock_session = mock.create_autospec(self.Session)
        item_id = 1
        tier_list_id = 2
        tier = "S"
        mock_session.commit.return_value = None
        mock_session.query().filter().first.return_value = None
        mock_session.add.return_value = None

        result = rank_tierlist_item(item_id,
                                    tier_list_id,
                                    tier,
                                    db=mock_session)

        self.assertEqual(result.tier, tier)

    def test_delete_tierlist_item(self):
        mock_session = mock.create_autospec(self.Session)
        item_id = 1
        tier_list_id = 1
        tier_list_item = TierListItem(item_id=item_id,
                                      tier_list_id=tier_list_id)
        mock_session.query().filter().first.return_value = tier_list_item
        mock_session.commit.return_value = None

        delete_tierlist_item(item_id, tier_list_id, db=mock_session)

        mock_session.delete.assert_called_with(tier_list_item)
        mock_session.commit.assert_called_once()

    def test_get_item(self):
        mock_session = mock.create_autospec(self.Session)
        item_id = 1
        item = Item(name="Item 1")
        mock_session.query().filter_by().first.return_value = item

        result = get_item(item_id, db=mock_session)

        self.assertEqual(result, item)

    def test_get_all_tierlists(self):
        mock_session = mock.create_autospec(self.Session)
        user_id = 1
        tier_lists = [TierList(id=1, user_id=2, template_id=3),
                      TierList(id=2, user_id=5, template_id=6)]
        mock_session.query().filter_by().all.return_value = tier_lists

        result = get_all_tierlists(user_id, db=mock_session)

        self.assertEqual(result, tier_lists)

    def test_get_tierlist(self):
        mock_session = mock.create_autospec(self.Session)
        tier_list = TierList(id=1, user_id=2, template_id=3)
        mock_session.query().filter().first.return_value = tier_list

        result = get_tierlist(3, 2, db=mock_session)

        self.assertEqual(result, tier_list)

    def test_get_tierlist_by_id(self):
        mock_session = mock.create_autospec(self.Session)
        tierlist_id = 1
        tier_list = TierList(id=1, user_id=2, template_id=3)
        mock_session.query().filter_by().first.return_value = tier_list

        result = get_tierlist_by_id(tierlist_id, db=mock_session)

        self.assertEqual(result, tier_list)

    def test_create_tierlist(self):
        mock_session = mock.create_autospec(self.Session)
        template_id = 1
        user_id = 2
        tier_list = TierList(template_id=template_id, user_id=user_id)
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        result = create_tierlist(template_id, user_id, mock_session)

        self.assertEqual(result.template_id, tier_list.template_id)
        self.assertEqual(result.user_id, tier_list.user_id)


if __name__ == '__main__':
    unittest.main()
