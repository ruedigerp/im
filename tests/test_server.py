import os
import app
import unittest


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_renders_something(self):
        rv = self.app.get('/')
        self.assertIn(b'<html>', rv.data)

    def test_body_has_class_app(self):
        rv = self.app.get('/')
        self.assertIn(b'<body class="app">', rv.data)


if __name__ == '__main__':
    unittest.main()
