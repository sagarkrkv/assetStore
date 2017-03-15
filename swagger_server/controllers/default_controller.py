import connexion
from swagger_server.models.asset import Asset
from swagger_server.models.asset_details import AssetDetails
from swagger_server.models.error_model import ErrorModel
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from flask import json
import string
import random
import re
import cuckoofilter
from collections import defaultdict


class AssetStore(object):

    def __init__(self):
        self.data = {}
        self.tags = defaultdict(set)

    def insert(self, asset):
        self.data[asset.name] = asset
        self.tags[asset.type].add(asset.name)
        self.tags[asset._class].add(asset.name)


datastore = AssetStore()
CF = cuckoofilter.CuckooFilter(capacity=500000, fingerprint_size=2)
PATTERN = re.compile("[A-Za-z0-9][\w-]{3,63}")


def add_asset(asset):
    """
    add_asset
    Creates a new asset.  Duplicates are not allowed
    :param asset: Asset to add
    :type asset: dict | bytes
    :param X_User: User key
    :type X_User: str

    :rtype: Asset
    """

    if not isAuthorized(connexion.request.headers['X-User']):
        return "User not authorized to post data", 401

    if connexion.request.is_json:
        asset = Asset.from_dict(connexion.request.get_json())

    if asset.name == "_random":
        asset.name = genRandName()

    if not PATTERN.match(asset.name):
        return "Given asset name `{}` is invalid.".format(asset.name), 422

    if CF.contains(asset.name):
        return "An asset already exists with the name " + asset.name, 409

    if not isValidClass(asset.type, asset._class.lower()):
        return "Invalid asset class for given asset type", 422

    if asset.details:
        details = asset.details
        for detail in details:
            isvalidDetail(asset, detail)

    CF.insert(asset.name)

    datastore.insert(asset)

    return json.jsonify(asset)


def find_asset_by_name(name):
    """
    find_asset_by_name
    Returns an asset based on a its name
    :param name: name of asset to fetch
    :type name: str

    :rtype: Asset

    """
    if not CF.contains(name):
        return "The asset `{}` does not exist".format(name), 400
    return json.jsonify(datastore.data[name])


def find_assets(tags=None):
    """
    find_assets
    Returns all assets from the system
    :param tags: tags to filter by, asset_type and/or asset_code
    :type tags: List[str]

    :rtype: List[Asset]
    """
    if not tags:
        return json.jsonify(list(datastore.data.values()))

    tags = tags.lower()
    if tags not in {"satellite", "dove", "rapideye", "antenna", "dish", "yagi"}:
        return "Invalid tag " + tags, 422

    return json.jsonify([datastore.data[k] for k in datastore.tags[tags]])


def update_asset_by_name(name, assetDetails):
    """
    update_asset_by_name
    Updates the asset details by name.
    :param name: name of asset to update
    :type name: str
    :param assetDetails: Asset to add
    :type assetDetails: list | bytes`
    :param X_User: User key
    :type X_User: str

    :rtype: Asset
    """
    if not isAuthorized(connexion.request.headers['X-User']):
        return "User not authorized to perform this operation", 500

    if not CF.contains(name):
        return "The asset `{}` does not exist.".format(name), 400

    if connexion.request.is_json:
        assetDetails = [AssetDetails.from_dict(d)
                        for d in connexion.request.get_json()]

    asset = datastore.data[name]

    for detail in assetDetails:
        isvalidDetail(asset, detail)

    return json.jsonify(asset)


def isAuthorized(user):
    "Checks the X-User Header validity "
    if not user or not user.isalpha() or user.lower() != "admin":
        return False
    return True


def isValidClass(assetType, assetClass):
    "Checks the validity of the given AssetClass for the AssetType"
    if assetType == "satellite":
        if assetClass not in {"dove", "rapideye"}:
            return False
    else:
        if assetClass not in {"dish", "yagi"}:
            return False
    return True


def isvalidDetail(asset, detail):
    if not asset.details or type(asset.details) != type(dict()):
        asset.details = {}
    key, value = detail.type, detail.value
    if asset._class == "dish":
        if key == "diameter" and isFloat(value):
            asset.details[key] = float(value)
            return True
        elif key == "radome" and value in {"true", "false"}:
            asset.details[key] = value
            return True
    elif asset._class == "yagi":
` if key == "gain" and isFloat(value):
            asset.details[key] = float(value)
            return True
    return False

def genRandName():
    "generates a psuedorandom string for the name"
    res = random.choice(string.ascii_letters + string.digits) + "".join(random.choice(string.ascii_letters \
            + string.digits +"_-") for _ in range(random.randint(3,63)))
    if CF.contains(res):
        res = genRandName()
    return res



def isFloat(n):
    try:
        float(n)
        return True
    except:
        return False
