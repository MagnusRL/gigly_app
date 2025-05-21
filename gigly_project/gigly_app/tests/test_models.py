from django.test import TestCase
from gigly_app.models import User, Task, Application

class TestUserModel(TestCase):
    def test_create_buyer_and_seller(self):
        buyer = User.objects.create_user(email="buyer@test.com", password="123", is_buyer=True)
        seller = User.objects.create_user(email="seller@test.com", password="123", is_seller=True)
        self.assertTrue(buyer.is_buyer)
        self.assertTrue(seller.is_seller)
        self.assertEqual(str(buyer), "buyer@test.com")

class TestTaskModel(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(email="buyer@test.com", password="123", is_buyer=True)

    def test_create_task(self):
        task = Task.objects.create(
            buyer=self.buyer,
            title="Test Task",
            description="Clean something",
            category="Cleaning",
            location="Oslo",
            price=150
        )
        self.assertEqual(str(task), "Test Task")

class TestApplicationModel(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(email="buyer@test.com", password="123", is_buyer=True)
        self.seller = User.objects.create_user(email="seller@test.com", password="123", is_seller=True)
        self.task = Task.objects.create(
            buyer=self.buyer,
            title="Test Task",
            description="Fix bike",
            category="Repair",
            location="Bergen",
            price=300
        )

    def test_create_application(self):
        app = Application.objects.create(
            task=self.task,
            seller=self.seller,
            message="I’ll do it"
        )
        self.assertEqual(app.status, "pending")
        self.assertEqual(str(app), "seller@test.com applies to Test Task")