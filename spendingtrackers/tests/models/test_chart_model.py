"""Unit Tests for the Chart Model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from spendingtrackers.models import User, Chart

class ChartTest(TestCase):

    # Set up a valid Chart data input.
    def setUp(self):
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            username = 'johndoe@example.org',
            currency = "£",
            pin = "123",
        )

        self.chart = Chart(
            name = 'Chart1',
            start_date = '2023-12-12',
            responsible = self.user,
            week_number = '10',
            finish_date = '2024-12-12',
        )

    def test_valid_user(self):
        self._assert_user_is_valid()


    # Functions:
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _assert_chart_is_valid(self):
        try:
            self.chart.full_clean()
        except ValidationError:
            self.fail("Test chart should be valid")

    def _assert_chart_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.chart.full_clean()


    # Name Tests:
    def test_name_can_be_200_characters_long(self):
        self.chart.name = 'x'*200
        self._assert_chart_is_valid()

    def test_name_cannot_be_over_200_characters_long(self):
        self.chart.name = 'x'*201
        self._assert_chart_is_invalid()


    # Start Date Tests:
    def test_start_date_cannot_be_blank(self):
        self.chart.start_date = ''
        self._assert_chart_is_invalid()


    # Finish Date Tests:
    def test_finish_date_cannot_be_blank(self):
        self.chart.finish_date = ''
        self._assert_chart_is_invalid()


    # Week Number Tests:
    def test_week_number_can_be_blank(self):
        self.chart.week_number = ''
        self._assert_chart_is_valid()

    def test_week_number_can_be_2_characters_long(self):
        self.chart.week_number = '12'
        self._assert_chart_is_valid()

    def test_week_number_cannot_be_over_2_characters_long(self):
        self.chart.week_number = '121'
        self._assert_chart_is_invalid()


    # str Method Tests:
    def test_str_method_can_return_name(self):
        show_name = 'Chart1'
        self.assertEqual(str(self.chart), show_name)
