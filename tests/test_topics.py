import unittest
from flask_testing import TestCase
from app import app
import json


class TopicsTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_that_topics_are_returned(self):
        response = self.client.get('/')
        data = json.loads(response.data.decode())
        self.assert200(response)
        self.assertEqual(data['status'], 'success', msg='Status should be success')
        self.assertListEqual(data['topics'],
                             ['news', 'business', 'counties', 'sports',
                              'blogs & opinion', 'life and style', 'videos',
                              'photos'],
                             msg='List is incorrect')
        self.assertTrue(isinstance(data['topics'], list), msg='Topics is not a list')

    def test_that_topic_data_is_returned(self):
        response = self.client.get('/topics?topic=news')
        data = json.loads(response.data.decode())
        self.assert200(response)
        self.assertEqual('success', data['status'], msg='request not successful for topic ')
        self.assertTrue(isinstance(data['data'][0], object), msg='not an object')


if __name__ == '__main__':
    unittest.main()
