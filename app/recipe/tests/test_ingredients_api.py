from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDINENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """
    Test the publiciy available ingredients API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that  login is required to acess the endpoint
        """
        res = self.client.get(INGREDINENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """
    Test ingredients can be retrived by authorized user
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_imgredient_test(self):
        """
        Test retriving a list of ingredients
        """
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDINENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """
        Test that ingredients for the authenticated user are returned
        """

        user2 = get_user_model().object.create_user(
            'other@user.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')

        ingredient = Ingredient.objects.create(
            user=self.user, name='Tumeric')

        res = self.client.get(INGREDINENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)