# coding: utf-8

"""
  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License").
  You may not use this file except in compliance with the License.
  A copy of the License is located at

      http://www.apache.org/licenses/LICENSE-2.0

  or in the "license" file accompanying this file. This file is distributed
  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
  express or implied. See the License for the specific language governing
  permissions and limitations under the License.
"""


"""
    ProductAdvertisingAPI

    https://webservices.amazon.com/paapi5/documentation/index.html  # noqa: E501
"""


import pprint
import re  # noqa: F401

import six


class OfferSavings(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'amount': 'float',
        'currency': 'str',
        'display_amount': 'str',
        'percentage': 'int',
        'price_per_unit': 'float'
    }

    attribute_map = {
        'amount': 'Amount',
        'currency': 'Currency',
        'display_amount': 'DisplayAmount',
        'percentage': 'Percentage',
        'price_per_unit': 'PricePerUnit'
    }

    def __init__(self, amount=None, currency=None, display_amount=None, percentage=None, price_per_unit=None):  # noqa: E501
        """OfferSavings - a model defined in Swagger"""  # noqa: E501

        self._amount = None
        self._currency = None
        self._display_amount = None
        self._percentage = None
        self._price_per_unit = None
        self.discriminator = None

        if amount is not None:
            self.amount = amount
        if currency is not None:
            self.currency = currency
        if display_amount is not None:
            self.display_amount = display_amount
        if percentage is not None:
            self.percentage = percentage
        if price_per_unit is not None:
            self.price_per_unit = price_per_unit

    @property
    def amount(self):
        """Gets the amount of this OfferSavings.  # noqa: E501


        :return: The amount of this OfferSavings.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this OfferSavings.


        :param amount: The amount of this OfferSavings.  # noqa: E501
        :type: float
        """

        self._amount = amount

    @property
    def currency(self):
        """Gets the currency of this OfferSavings.  # noqa: E501


        :return: The currency of this OfferSavings.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this OfferSavings.


        :param currency: The currency of this OfferSavings.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def display_amount(self):
        """Gets the display_amount of this OfferSavings.  # noqa: E501


        :return: The display_amount of this OfferSavings.  # noqa: E501
        :rtype: str
        """
        return self._display_amount

    @display_amount.setter
    def display_amount(self, display_amount):
        """Sets the display_amount of this OfferSavings.


        :param display_amount: The display_amount of this OfferSavings.  # noqa: E501
        :type: str
        """

        self._display_amount = display_amount

    @property
    def percentage(self):
        """Gets the percentage of this OfferSavings.  # noqa: E501


        :return: The percentage of this OfferSavings.  # noqa: E501
        :rtype: int
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """Sets the percentage of this OfferSavings.


        :param percentage: The percentage of this OfferSavings.  # noqa: E501
        :type: int
        """

        self._percentage = percentage

    @property
    def price_per_unit(self):
        """Gets the price_per_unit of this OfferSavings.  # noqa: E501


        :return: The price_per_unit of this OfferSavings.  # noqa: E501
        :rtype: float
        """
        return self._price_per_unit

    @price_per_unit.setter
    def price_per_unit(self, price_per_unit):
        """Sets the price_per_unit of this OfferSavings.


        :param price_per_unit: The price_per_unit of this OfferSavings.  # noqa: E501
        :type: float
        """

        self._price_per_unit = price_per_unit

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(OfferSavings, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OfferSavings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
