"""
Tests for 'api/desc' post, get, delete methods 


#GET api/desc?abbr=GDP

#Returns:
#   {'abbr':'GDP', 'ru':'Цена нефти Brent', 'en':'Brent oil price'}

#GET api/desc?abbr=rog

#Returns:
#    {unit:'rog', en:'rate of growth to previous period', ru='темп роста к пред. периоду'}


#POST api/desc

#Payload:
#[dict(abbr='BRENT', ru='Цена нефти Brent', en='Brent oil price')
#dict(abbr='GDP', ru='Валовый внутренний продукт', en='Gross domestic product')
#dict(abbr='rog', ru='темп роста к пред. периоду', en='rate of growth to previous period')
#dict(abbr='yoy', ru='темп роста за 12 месяцев', en='year-on-year rate of growth')]

#DELETE api/desc?abbr=rog
#DELETE api/desc?abbr=BRENT

"""

# NOT TODO:
# - parametrise tests

import pytest
from flask import json

from tests.test_basic import TestCaseBase

DESC_URL = 'api/desc'

sample_post_payload = [
    dict(abbr='BRENT', ru='Цена нефти Brent', en='Brent oil price'),
    dict(abbr='GDP', ru='Валовый внутренний продукт', en='Gross domestic product'),
    dict(abbr='rog', ru='темп роста к пред. периоду', en='rate of growth to previous period'),
    dict(abbr='yoy', ru='темп роста за 12 месяцев', en='year-on-year rate of growth')
]


class Test_api_desc_GET_method(TestCaseBase):

    def test_get_method_without_params_fails(self):
        response = self.client.get(DESC_URL)
        assert response.status_code != 200

    def test_get_method_with_wrong_abbr_param_fails(self):
        params = dict(abbr='wrong_params')
        response = self.client.get(DESC_URL, query_string=params)
        assert response.status_code != 200

    @pytest.mark.xfail
    def test_get_on_valid_variable_successful_with_code_200(self):
        params = dict(abbr='GDP')
        response = self.client.get(DESC_URL, query_string=params)

        assert response.status_code == 200

    @pytest.mark.xfail
    def test_get_on_valid_variable_successful_returns_valid_data(self):
        params = dict(abbr='GDP')
        response = self.client.get(DESC_URL, query_string=params)
        data = json.loads(response.get_data().decode('utf-8'))

        assert data == {'abbr': 'GDP', 'ru': 'Цена нефти Brent', 'en': 'Brent oil price'}

    @pytest.mark.xfail
    def test_get_on_valid_variable_successful_with_code_200(self):
        params = dict(abbr='rog')
        response = self.client.get(DESC_URL, query_string=params)

        assert response.status_code == 200

    @pytest.mark.xfail
    def test_get_on_valid_variable_successful_returns_valid_data(self):
        params = dict(abbr='rog')
        response = self.client.get(DESC_URL, query_string=params)
        data = json.loads(response.get_data().decode('utf-8'))

        assert data == {'unit': 'rog', 'en': 'rate of growth to previous period',
                        'ru': 'темп роста к пред. периоду'}


class Test_api_desc_POST_method(TestCaseBase):

    def test_post_method_without_params_fails(self):
        response = self.client.post(DESC_URL)
        assert response.status_code != 200

    def test_post_method_on_broken_data_returns_error_code(self):
        response = self.client.post(DESC_URL, data="broken_data")
        assert response.status_code != 200

    @pytest.mark.xfail
    def test_post_method_on_duplicate_data_fails(self):
        upload_json = json.dumps(sample_post_payload)
        response = self.client.post(DESC_URL, data=upload_json)
        # second call
        response = self.client.post(DESC_URL, data=upload_json)
        assert response.status_code != 200

    @pytest.mark.xfail
    def test_post_method_on_new_data_successful_with_code_200(self):
        upload_json = json.dumps(sample_post_payload)
        response = self.client.post(DESC_URL, data=upload_json)
        assert response.status_code == 200

    @pytest.mark.xfail
    def test_post_method_getting_posted_successful_returns_posted_data(self):
        upload_json = json.dumps(sample_post_payload)
        self.client.post(DESC_URL, data=upload_json)

        for desc in sample_post_payload:
            response = self.client.get(DESC_URL, query_string={'abbr': desc.get('abbr')})
            assert desc == json.loads(response.get_data().decode('utf-8'))


class Test_api_desc_DELETE_method(TestCaseBase):
        
    def test_delete_method_on_empty_abbr_field_fails(self):
        params = dict(abbr='')
        response = self.client.delete(DESC_URL, query_string=params)
        assert response.status_code != 200

    @pytest.mark.xfail
    def test_delete_variable_desc_successful_with_code_200(self):
        params = dict(abbr='rog')
        response = self.client.delete(DESC_URL, query_string=params)
        assert response.status_code == 200

    @pytest.mark.xfail
    def test_delete_posted_data_successful_with_code_200(self):
        upload_json = json.dumps(sample_post_payload)
        self.client.post(DESC_URL, data=upload_json)

        for desc in sample_post_payload:
            response = self.client.delete(DESC_URL,
                                          query_string={'abbr': desc.get('abbr')})
            assert response.status_code == 200

if __name__ == '__main__': # pragma no cover
    pytest.main([__file__])
    
    
# import pytest
# import requests

# APP_URL = 'http://minikep-db.herokuapp.com'
# API_DESC_URL = f'{APP_URL}/api/desc'


# sample_post_payload = [
    # dict(head='test_BRENT', ru='Цена нефти Brent', en='Brent oil price'),
    # dict(head='test_GDP', ru='Валовый внутренний продукт', en='Gross domestic product'),
    # dict(unit='test_rog', ru='темп роста к пред. периоду', en='rate of growth to previous period'),
    # dict(unit='test_yoy', ru='темп роста за 12 месяцев', en='year-on-year rate of growth')
# ]

# @pytest.mark.webtest
# class Test_ApiDesc:
    # def teardown(self):
        # pass

    # def test_get_without_params_should_fail(self):
        # response = requests.get(API_DESC_URL)
        # assert response.status_code != 200

    # def test_post_with_valid_params_is_ok(self):
        # response = requests.post(API_DESC_URL, json=sample_post_payload)
        # assert response.status_code == 200

    # def test_posting_dublicate_data_should_fail(self):
        # response = requests.post(API_DESC_URL, json=sample_post_payload)
        # assert response.status_code != 200

    # def test_getting_posted_data_is_ok(self):
    #     for desc in sample_post_payload:
    #         response = requests.get(API_DESC_URL, params={
    #             'head': desc.get('head'),
    #             'unit': desc.get('unit')
    #         })
    #         assert desc == response.json()
    #
    # def test_deleting_posted_data_is_ok(self):
    #     for desc in sample_post_payload:
    #         response = requests.delete(API_DESC_URL, params={
    #             'head': desc.get('head'),
    #             'unit': desc.get('unit')
    #         })
    #     assert response.status_code == 200
