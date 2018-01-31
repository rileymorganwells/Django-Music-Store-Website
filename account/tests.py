from django.test import TestCase
from account import models as amod

class UserModelTest(TestCase):

    fixtures = ['data.yaml']

    def setUp(self):
        self.user1 =
        self.u1 = amod.User()
        self.u1.first_name = 'Marge'
        self.u1.last_name = 'Simpson'
        self.u1.email = 'marge@simpsons.com'
        #u1.password = 'password' # WRONG WRONG WRONG
        self.u1.set_password('password')
        # ... more fields
        self.u1.save()
        self.u2 = amod.User.objects.get(email='homer@simpsons.com')

    def test_user_create_save_load(self):
        '''Tests round trip of User model data to/from database'''
        u2 = amod.User.objects.get(email='marge@simpsons.com')
        self.assertEquals(self.u1.first_name, u2.first_name)
        self.assertEquals(self.u1.last_name, u2.last_name)
        self.assertEquals(self.u1.email, u2.email)
        self.assertEquals(self.u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))

    def test_add_groups_check_permissions(self):
        '''Add groups to a user and check permissions'''
        for p in Permission.objects.all():
            print(p.content_type.app_label + "." + p.codename)

        p1 = Permission()
        p1.name = 'Change product price'
        p1.codename = 'change_product_price'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()
        self.u1.user_permissions.add(p1)

        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()
        g1.permissions.add(g1)
        g1.save()
        self.u1.groups.add(g1)

        self.assertTrue(self.u1.has_perm('auth.delete_group'))
