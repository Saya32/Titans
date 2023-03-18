from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import Category, User, Transaction, Achievement
from ...helpers import update_achievements, set_achievements, get_achievements

class AchievementTest(TestCase):
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.category1 = Category(
            user=self.user,
            name="New",
            budget=40,
            start_date = '2023-12-12',
            end_date = '2024-12-12',
        )
        self.category1.save()

        self.category2 = Category(
            user=self.user,
            name="New2",
            budget=40,
            start_date = '2023-12-12',
            end_date = '2024-12-12',
        )
        self.category2.save()

        self.category3 = Category(
            user=self.user,
            name="New3",
            budget=40,
            start_date = '2023-12-12',
            end_date = '2024-12-12',
        )
        self.category3.save()

        self.category4 = Category(
            user=self.user,
            name="New4",
            budget=40,
            start_date = '2023-12-12',
            end_date = '2024-12-12',
        )
        self.category4.save()

        self.category5 = Category(
            user=self.user,
            name="New5",
            budget=40,
            start_date = '2023-12-12',
            end_date = '2024-12-12',
        )
        self.category5.save()

        set_achievements(self.user)
        update_achievements(self.user)


    def new_user_unlocked(self):
        achievements = get_achievements(self.user)
        self.assertTrue(achievements[0].unlocked)

    def test_5_categories_unlocked(self):
        achievements = get_achievements(self.user)
        self.assertTrue(achievements[1].unlocked)
