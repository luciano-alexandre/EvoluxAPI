import unittest
from app import app_web


class TestAPI(unittest.TestCase):

    # Tests whether the '/' route does not exist.
    def test_get_home(self):
        app = app_web.test_client()
        response = app.get('/')
        self.assertEqual(404, response.status_code)

    #Tests if the '/ index' route does not exist.
    def test_get_index(self):
        app = app_web.test_client()
        response = app.get('/index')
        self.assertEqual(404, response.status_code)

    #Tests if the '/ number' route does not exist.
    def test_get_number_index(self):
        app = app_web.test_client()
        response = app.get('/number')
        self.assertEqual(404, response.status_code)

    # Tests if the '/login' route does not exist.
    def test_get_login_route(self):
        app = app_web.test_client()
        response = app.get('/login?username=admin&pass=admin')
        self.assertEqual(404, response.status_code)

    # Tests the route for authentication using the get verb
    def test_get_login(self):
        app = app_web.test_client()
        response = app.get('/authentication/login?username=admin&pass=admin')
        self.assertEqual(200, response.status_code)

    # Tests the route for authentication using the post verb
    def test_post_login(self):
        app = app_web.test_client()
        response = app.get('/authentication/login?username=admin&pass=admin')
        self.assertEqual(200, response.status_code)

    # Tests the route for authentication using the put verb
    def test_put_login(self):
        app = app_web.test_client()
        response = app.put('/authentication/login?username=admin&pass=admin')
        self.assertEqual(405, response.status_code)

    # Tests if the '/logout' route does not exist.
    def test_get_logout_route(self):
        app = app_web.test_client()
        response = app.get('/logout')
        self.assertEqual(404, response.status_code)

    # Tests the route for logout using the get verb
    def test_get_logout(self):
        app = app_web.test_client()
        response = app.get('/authentication/logout')
        self.assertEqual(200, response.status_code)

    # Tests the route for logout using the post verb
    def test_post_logout(self):
        app = app_web.test_client()
        response = app.post('/authentication/logout')
        self.assertEqual(200, response.status_code)

    # Tests the route for logout using the put verb
    def test_put_logout(self):
        app = app_web.test_client()
        response = app.put('/authentication/logout')
        self.assertEqual(405, response.status_code)

    # Tests the route for listing all numbers, using the get method, it exists and is protected with authentication.
    def test_get_all_numbers_index_not_autentication(self):
        app = app_web.test_client()
        response = app.get('/number/getAllNumbers')
        self.assertEqual(401, response.status_code)

    # Tests the route for listing all numbers, using the post method, there is.
    def test_post_all_numbers_index_not_autentication(self):
        app = app_web.test_client()
        response = app.post('/number/getAllNumbers')
        self.assertEqual(405, response.status_code)

    # Tests whether the search route for a number exists without passing the search identifier.
    def test_get_one_number_not_param_not_autentication(self):
        app = app_web.test_client()
        response = app.get('/number/getNumberById')
        self.assertEqual(404, response.status_code)

    # Tests whether the route to search for a number exists, using the get method, and is protected with authentication.
    def test_get_one_number_not_autentication(self):
        app = app_web.test_client()
        response = app.get('/number/getNumberById/1')
        self.assertEqual(401, response.status_code)

    # Tests whether the route to search for a number exists, using the post method, and is protected with authentication.
    def test_post_one_number_not_autentication(self):
        app = app_web.test_client()
        response = app.post('/number/getNumberById/1')
        self.assertEqual(405, response.status_code)

    # Tests whether the route for registering a new number exists, using the post method, and is protected with authentication.
    def test_post_number_add_not_parameters(self):
        app = app_web.test_client()
        response = app.post('/number/addNumber?value=558491234-4321&monthyPrice=0.03&setupPrice=3.40&currency=U$')
        self.assertEqual(401, response.status_code)

    # Tests whether the route for registering a new number exists, using the get method.
    def test_get_number_add_not_parameters(self):
        app = app_web.test_client()
        response = app.get('/number/addNumber?value=558491234-4321&monthyPrice=0.03&setupPrice=3.40&currency=U$')
        self.assertEqual(405, response.status_code)

    # Tests whether the route to delete a number exists without passing the identifier of the number to be deleted.
    def test_delete_number_not_autentication(self):
        app = app_web.test_client()
        response = app.delete('/number/deleteNumber')
        self.assertEqual(404, response.status_code)

    # Tests whether the route to delete a number exists, using the get method, and is protected by authentication.
    def test_get_delete_number_not_autentication(self):
        app = app_web.test_client()
        response = app.get('/number/deleteNumber/1')
        self.assertEqual(401, response.status_code)

    # Tests whether the route to delete a number exists, using the delete method, and is protected by authentication.
    def test_delete_number_not_autentication(self):
        app = app_web.test_client()
        response = app.delete('/number/deleteNumber/1')
        self.assertEqual(401, response.status_code)

    # Tests whether the route to delete a number exists, using the put method.
    def test_put_delete_number_not_autentication(self):
        app = app_web.test_client()
        response = app.put('/number/deleteNumber/1')
        self.assertEqual(405, response.status_code)

    # Tests if the route to edit a number exists even without passing the identifier of the number to be edited.
    def test_post_edit_number_not_param_not_autentication(self):
        app = app_web.test_client()
        response = app.post('/number/editNumber')
        self.assertEqual(404, response.status_code)

    # Tests whether the route to edit a number exists, using the post method, and is protected by authentication.
    def test_post_edit_number_not_autentication(self):
        app = app_web.test_client()
        response = app.post('/number/editNumber/1?value=558491234-4321&monthyPrice=0.03&setupPrice=3.40&currency=U$')
        self.assertEqual(401, response.status_code)

    # Tests whether the route to edit a number exists, using the put method, and is protected by authentication.
    def test_put_edit_number_not_autentication(self):
        app = app_web.test_client()
        response = app.put('/number/editNumber/1?value=558491234-4321&monthyPrice=0.03&setupPrice=3.40&currency=U$')
        self.assertEqual(401, response.status_code)

    # Tests whether the route to edit a number exists, using the get method, and is protected by authentication.
    def test_get_edit_number_not_autentication(self):
        app = app_web.test_client()
        response = app.get('/number/editNumber/1?value=558491234-4321&monthyPrice=0.03&setupPrice=3.40&currency=U$')
        self.assertEqual(405, response.status_code)

if __name__ == '__main__':
    unittest.main()