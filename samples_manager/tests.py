from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import *
# Create your tests here.


class UserCreateTest(TestCase):

    def create_user(self, email="ina.gotse@gmail.com"):
        return Users.objects.create(email=email)

    def test_user_creation(self):
        w = self.create_user()
        self.assertTrue(isinstance(w, Users))
        self.assertEqual(w.__str__(), w.email)


    def test_user_list_view(self):
        w = self.create_user()
        url = reverse("samples_manager:users_list")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(w.email, resp.content)


class PassiveCustomCategoriesCreateTest(TestCase):

    def create_PassiveCustomCategories(self, passive_category_type="passive irradiation", passive_irradiation_area="25x25",passive_modus_operandi= "bla bla" ):
        return PassiveCustomCategories.objects.create(passive_category_type=passive_category_type, passive_irradiation_area= passive_irradiation_area,passive_modus_operandi= passive_modus_operandi)

    def test_PassiveCustomCategories_creation(self):
        w = self.create_PassiveCustomCategories()
        self.assertTrue(isinstance(w, PassiveCustomCategories))
        self.assertEqual(w.__str__(), w.passive_category_type)


class ActiveCategoriesCreateTest(TestCase):

    def create_ActiveCategories(self, active_category_type="active irradiation", active_irradiation_area="25x25",active_modus_operandi= "bla bla" ):
        return ActiveCategories.objects.create(active_category_type=active_category_type, active_irradiation_area= active_irradiation_area,active_modus_operandi= active_modus_operandi)
 
    def test_ActiveCategories_creation(self):
        w = self.create_ActiveCategories()
        self.assertTrue(isinstance(w, ActiveCategories))
        self.assertEqual(w.__str__(), w.active_category_type)


class ReqFluencesCreateTest(TestCase):

    def create_ReqFluences(self, req_fluence="2e12"):
        return ReqFluences.objects.create(req_fluence=req_fluence)
 
    def test_ReqFluences_creation(self):
        w = self.create_ReqFluences()
        self.assertTrue(isinstance(w, ReqFluences))
        self.assertEqual(w.__str__(), w.req_fluence)