import json
import unittest

from glucose_levels_server import application

application.testing = True


class TestGlucoseLevelsServer(unittest.TestCase):
    """
    Usually there should be tests for every independent function but in the interest of time these are skipped.
    """
    def test_get_levels_by_user_id_expected_response(self):

        # Usually would have more test cases such as wildly varying DB data to make sure we get all those test cases.
        with application.test_client() as client:

            # My strong opinion is that live databases should NEVER be used in unittests
            # But this is an offline SQlite database so will not mock out for now...

            response = client.get('/api/v1/levels/', data=json.dumps({"user_id": "bruce_wayne"}))
            expected_response = [{"timestamp": "18-02-2021 10:57", "glucose_level": 89},
                                 {"timestamp": "18-02-2021 11:12", "glucose_level": 90},
                                 {"timestamp": "18-02-2021 11:27", "glucose_level": 91},
                                 {"timestamp": "18-02-2021 11:42", "glucose_level": 92}]

            self.assertEqual(expected_response, json.loads(response.data))

    def test_get_levels_by_user_id_invalid_user_id(self):

        with application.test_client() as client:

            # Checking that the basic validation is working...
            response = client.get('/api/v1/levels/', data=json.dumps({"user_id": None}))
            self.assertEqual(response.status_code, 400)
            response = client.get('/api/v1/levels/', data=json.dumps({}))
            self.assertEqual(response.status_code, 400)
            response = client.get('/api/v1/levels/', data=json.dumps({"user": None}))
            self.assertEqual(response.status_code, 400)

    def test_get_levels_by_recording_id_invalid_id(self):

        with application.test_client() as client:

            # Checking that the basic validation is working...
            response = client.get('/api/v1/levels/SelinaKyle')
            self.assertEqual(response.status_code, 400)

            # Should be getting an error if nothing is found.
            response = client.get('/api/v1/levels/10000000000')
            self.assertEqual(response.status_code, 404)

    def test_get_levels_by_recording_id_expected_request(self):

        with application.test_client() as client:

            # We expect data from the fake bruce wayne data...
            response = client.get('/api/v1/levels/1')
            self.assertEqual(json.loads(response.data), [1,
                                                         "bruce_wayne",
                                                         "18-02-2021 10:57",
                                                         89,
                                                         "1D48A10E-DDFB-4888-8158-026F08814833",
                                                         "Batmobile Sensor",
                                                         "0"])


if __name__ == '__main__':
    unittest.main()
