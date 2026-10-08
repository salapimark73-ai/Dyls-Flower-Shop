from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Flower


class FlowerInventoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='flowerkeeper',
            password='test-password-123',
        )
        self.client.force_login(self.user)

    def test_create_form_saves_a_flower(self):
        response = self.client.post(reverse('flower-create'), {
            'flower_name': 'Peach Rose',
            'flower_type': 'Rose',
            'price': '12.50',
            'quantity': '8',
            'color': 'Peach',
            'description': 'A soft garden rose.',
        })

        self.assertRedirects(response, reverse('index'))
        flower = Flower.objects.get()
        self.assertEqual(flower.flower_name, 'Peach Rose')
        self.assertEqual(flower.price, Decimal('12.50'))

    def test_invalid_negative_quantity_is_not_saved(self):
        response = self.client.post(reverse('flower-create'), {
            'flower_name': 'Invalid flower',
            'flower_type': 'Other',
            'price': '5.00',
            'quantity': '-1',
            'color': 'Green',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quantity cannot be negative.')
        self.assertEqual(Flower.objects.count(), 0)

    def test_delete_requires_post(self):
        flower = Flower.objects.create(
            flower_name='Tulip',
            flower_type='Tulip',
            price='4.00',
            quantity=3,
            color='Pink',
        )

        response = self.client.get(reverse('flower-delete', args=[flower.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete this flower?')
        self.assertTrue(Flower.objects.filter(pk=flower.product_id).exists())

        response = self.client.post(reverse('flower-delete', args=[flower.product_id]))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Flower.objects.filter(pk=flower.product_id).exists())

    def test_search_finds_saved_flowers(self):
        Flower.objects.create(
            flower_name='Peach Rose',
            flower_type='Rose',
            price='12.50',
            quantity=8,
            color='Peach',
            description='A soft garden rose.',
        )

        response = self.client.get(reverse('index'), {'q': 'peach'})

        self.assertContains(response, 'Peach Rose')
        self.assertEqual(len(response.context['products']), 1)

    def test_search_finds_flowers_by_type(self):
        Flower.objects.create(
            flower_name='Garden Star',
            flower_type='Orchid',
            price='18.00',
            quantity=2,
            color='White',
        )

        response = self.client.get(reverse('index'), {'q': 'orchid'})

        self.assertContains(response, 'Garden Star')
        self.assertEqual(len(response.context['products']), 1)

    def test_profile_shows_account_and_logout(self):
        response = self.client.get(reverse('profile'))

        self.assertContains(response, 'flowerkeeper')
        self.assertContains(response, reverse('logout'))

    def test_dashboard_redirects_anonymous_users_to_login(self):
        self.client.logout()

        response = self.client.get(reverse('index'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('index')}",
        )

    def test_login_and_logout(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'flowerkeeper',
            'password': 'test-password-123',
        })

        self.assertRedirects(response, reverse('index'))
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_create_account_signs_user_in(self):
        self.client.logout()

        response = self.client.post(reverse('create-account'), {
            'username': 'newkeeper',
            'password1': 'RoseGarden!42',
            'password2': 'RoseGarden!42',
        })

        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(
            get_user_model().objects.filter(username='newkeeper').exists()
        )

    def test_login_links_to_create_account_page(self):
        self.client.logout()

        login_response = self.client.get(reverse('login'))
        account_response = self.client.get(reverse('create-account'))

        self.assertContains(login_response, reverse('create-account'))
        self.assertContains(account_response, 'Create your account')
