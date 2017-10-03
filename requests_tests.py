import requests

BASE_URI = 'api/datapoints'
POST_URI = 'api/incoming'

# data = [{
    # 'name': 'BRENT',
    # 'freq': 'm',
    # 'date': '2018-01-01',
    # 'value': 42.0
# }]

payload = {'name': 'BRENT', 'freq': 'm'}
    

class TestGET():
    def test_request_response_with_valid_params():
        """Should complete successfully with OK status code"""
        response = requests.get(BASE_URI, params=payload)
        assert response.ok

    def test_getting_BRENT():
        """Should return a list with items that have the requested variable"""
        response = requests.get(BASE_URI, params=payload)
        assert response.json()[0]['name'] == 'BRENT'

    def test_request_with_empty_name():
        """Should return 400 error with empty name parameter"""
        payload = {'name': '', 'freq': 'm'}
        response = requests.get(BASE_URI, params=payload)
        assert response.status_code == 400

    def test_request_with_empty_frequency():
        """Should return 400 error with empty freq parameter"""
        payload = {'name': 'BRENT', 'freq': ''}
        response = requests.get(BASE_URI, params=payload)
        assert response.status_code == 400

    def test_getting_data_not_found():
        """Should return response with empty json"""
        payload = {'name': 'FOOBAR', 'freq': 'm'}
        response = requests.get(BASE_URI, params=payload)
        assert response.json() == {}


class TestPOST():
    def test_posting_valid_data():
        """Should return an empty JSON on success"""
        data = [{ "date": "1999-03-31", "freq": "q", "name": "INVESTMENT_bln_rub", "value": 12345.6 }]
        response = requests.post(POST_URI, data=data)
        assert response.json() == {}

    def test_posting_data_with_empty_name_field():
        """Should result in a 400 error"""
        data = [{ "date": "1999-03-31", "freq": "q", "name": "", "value": 12345.6 }]
        response = requests.post(POST_URI, data=data)
        assert response.status_code == 400
