from service import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.test import (override_settings, TransactionTestCase, Client,
    RequestFactory, )
from django.contrib.sites.shortcuts import get_current_site

from station.models import Color, New
from station.views import color_list

class SitesTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        site = Site(id=1, domain='station-example.com', name='Station')
        site.save()
        self.site_new = Site(
            id=2,
            domain='station-new.com',
            name='New station'
        )
        self.site_new.save()
        self.factory = RequestFactory()

    def test_site_manager(self):
        # test that site manager does not return a deleted Site object.
        s = Site.objects.get_current()
        self.assertIsInstance(s, Site)
        s.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Site.objects.get_current()

    def test_get_current_site(self):
        # current site shouldn't change after create new Site object.
        # import pdb; pdb.set_trace()
        current = Site.objects.get_current()
        self.assertEqual(current.name, 'Station')
        self.assertEqual(current.domain, 'station-example.com')

        current_new = Site.objects.get_current()
        self.assertEqual(current.name, current_new.name)
        self.assertEqual(current.domain, current_new.domain)

    def test_create_new(self):
        # test is create a new only for one site
        # and doesn't exist in other site.
        current_site = Site.objects.get_current()
        self.assertEqual(current_site.new_set.count(), 0)

        new = New.objects.create(title='Hello World', site=current_site)
        new_1 = New.objects.create(
            title='Hello World Test 1',
            site=current_site
        )
        new_2 = New.objects.create(
            title='Hello World Test 2',
            site=self.site_new
        )

        news_in_site = current_site.new_set.all()
        self.assertEqual(news_in_site.count(), 2)
        self.assertIn(new, news_in_site)
        self.assertIn(new_1, news_in_site)
        self.assertNotIn(new_2, news_in_site)
        self.assertIn(new_2, self.site_new.new_set.all())

    def test_create_color(self):
        # test is create a color for many sites
        # check than this color exist in all sites
        color = Color.objects.create(name='Red', shade="Printer's Magenta")
        current_site = Site.objects.get_current()
        another_site = Site.objects.get(id=2)
        color.sites.add(another_site, current_site)
        self.assertIn(color, current_site.color_set.all())
        self.assertIn(color, another_site.color_set.all())

    def test_remove_site_from_color(self):
        # test is check that the color doesn't have a Site object
        # after removing this Site object
        color = Color.objects.create(name='Red', shade="Printer's Magenta")
        current_site = Site.objects.get_current()
        another_site = Site.objects.get(id=2)
        color.sites.add(another_site, current_site)
        self.assertEqual(color.sites.count(), 2)

        another_site.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Site.objects.get(id=2)
        self.assertEqual(Site.objects.count(), 1)
        self.assertIn(color, current_site.color_set.all())
        self.assertEqual(color.sites.count(), 1)

    def test_current_site_from_request(self):
        # test is check than the request returns a current site
        # Create an instance of a GET request.
        request = self.factory.get('/test')
        site = get_current_site(request)
        self.assertEqual(site.domain, 'station-example.com')
        self.assertEqual(site.name, 'Station')
        self.assertEqual(request.get_full_path(), '/test')

    def test_current_site_manager(self):
        # test that CurrentSiteManager returns queries 
        # to include only objects associated with the current Site
        current_site = Site.objects.get_current()
        self.assertEqual(current_site.new_set.count(), 0)
        another_site = Site.objects.get(id=2)

        new = New.objects.create(title='Hello World', site=current_site)
        new_1 = New.objects.create(
            title='Hello World Test 1',
            site=current_site
        )
        new_2 = New.objects.create(
            title='Hello World Test 2',
            site=self.site_new
        )
        color = Color.objects.create(name='Red', shade="Printer's Magenta")
        color_1 = Color.objects.create(name='Blue', shade="Printer's Blue")
        color_2 = Color.objects.create(name='Black', shade="Printer's Black")
        color.sites.add(another_site, current_site)
        color_1.sites.add(current_site)
        color_2.sites.add(another_site)
        news = New.on_site.all()
        colors = Color.on_site.all()
        self.assertEqual(news.count(), 2)
        self.assertEqual(colors.count(), 2)
        self.assertIn(new, news)
        self.assertIn(new_1, news)
        self.assertNotIn(new_2, news)
        self.assertIn(color, colors)
        self.assertIn(color_1, colors)
        self.assertNotIn(color_2, colors)
    
    def test_get_current_response_colors_view(self):
        # returns current response
        # view is got request from different sites
        # color-list/ endpoint should returns all colors for selected site
        current_site = Site.objects.get_current()
        another_site = Site.objects.get(id=2)
        color = Color.objects.create(name='Red', shade="Printer's Magenta")
        color_1 = Color.objects.create(name='Blue', shade="Printer's Blue")
        color_2 = Color.objects.create(name='Black', shade="Printer's Black")
        color.sites.add(another_site, current_site)
        color_1.sites.add(current_site)
        color_2.sites.add(another_site)
        response = self.client.get(
            '/color-list', SERVER_NAME='station-example.com')
        expected_response = {
            '1': 'Red',
            '2': 'Blue',
        }
        self.assertEqual(response.json(), expected_response)
        response = self.client.get(
            '/color-list', SERVER_NAME='station-new.com')
        expected_response = {
            '1': 'Red',
            '3': 'Black',
        }
        self.assertEqual(response.json(), expected_response)

    def test_get_current_response_news_view(self):
        # new-list/ endpoint should returns all news for selected site
        current_site = Site.objects.get_current()
        another_site = Site.objects.get(id=2)
        New.objects.create(title='Hello World', site=current_site)
        New.objects.create(title='Hello World Test 1', site=current_site)
        New.objects.create(title='Hello World Test 2', site=self.site_new)
        response = self.client.get(
            '/new-list', SERVER_NAME='station-example.com')
        expected_response = {
            '1': 'Hello World',
            '2': 'Hello World Test 1',
        }
        self.assertEqual(response.json(), expected_response)
        response = self.client.get('/new-list', SERVER_NAME='station-new.com')
        expected_response = {'3': 'Hello World Test 2'}
        self.assertEqual(response.json(), expected_response)

    def test_get_empty_response(self):
        # returns empty response if News and Colors don't exist in Site object
        current_site = Site.objects.get_current()
        another_site = Site.objects.get(id=2)
        server_name = 'station-example.com'
        response = self.client.get('/color-list', SERVER_NAME=server_name)
        self.assertEqual(response.json(), {})
        response = self.client.get('/new-list', SERVER_NAME=server_name)
        self.assertEqual(response.json(), {})
        server_name = 'station-new.com'
        response = self.client.get('/color-list', SERVER_NAME=server_name)
        self.assertEqual(response.json(), {})
        response = self.client.get('/new-list', SERVER_NAME=server_name)
        self.assertEqual(response.json(), {})
