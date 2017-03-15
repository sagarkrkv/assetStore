# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.asset import Asset
from swagger_server.models.asset_details import AssetDetails
from swagger_server.models.error_model import ErrorModel
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestDefaultController(BaseTestCase):
    """ DefaultController integration test stubs """

    def test_add_asset(self):
        """
        Test case for add_asset


        """
        passcase = {
            "class": "dish",
            "name": "name_example",
            "type": "antenna"
        }
        asset = Asset().from_dict(passcase)
        headers = [('X-User', 'admin')]
        response = self.client.open('/api/assets',
                                    method='POST',
                                    data=json.dumps(asset),
                                    headers=headers,
                                    content_type='application/json')
        self.assert200(response, "Response body is : " +
                       response.data.decode('utf-8'))

    def test_find_asset_by_name(self):
        """
        Test case for find_asset_by_name


        """
        response = self.client.open('/api/assets/{name}'.format(name='name_example'),
                                    method='GET',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " +
                       response.data.decode('utf-8'))

    def test_find_assets(self):
        """
        Test case for find_assets


        """
        query_string = [('tags', 'antenna')]
        response = self.client.open('/api/assets',
                                    method='GET',
                                    content_type='application/json',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " +
                       response.data.decode('utf-8'))

    def test_update_asset_by_name(self):
        """
        Test case for update_asset_by_name


        """
        passcase = {
            "type": "diameter",
            "value": "23.3455"
        }

        assetDetails = [AssetDetails().from_dict(passcase)]
        headers = [('X-User', 'admin')]
        response = self.client.open('/api/assets/{name}'.format(name='name_example'),
                                    method='PATCH',
                                    data=json.dumps(assetDetails),
                                    headers=headers,
                                    content_type='application/json')
        self.assert200(response, "Response body is : " +
                       response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
