from graphene.test import Client
from graphql.schema import AccountQueries as query
import graphql.mutation as mutation
import graphene
import pytest
import os
import tempfile

FULL_USER_QUERY = """
    query User_grigo($id: ID!) {
        user(id: $id) {
            email
            firstName
            lastName
            isStaff
            isActive
            addresses {
                id
                isDefaultShippingAddress
                isDefaultBillingAddress
            }
            orders(first: 10) {
                totalCount
                edges {
                    node {
                        id
                    }
                }
            }
            languageCode
            dateJoined
            lastLogin
            defaultShippingAddress {
                firstName
                lastName
                companyName
                streetAddress1
                streetAddress2
                city
                cityArea
                postalCode
                countryArea
                phone
                country {
                    code
                }
                isDefaultShippingAddress
                isDefaultBillingAddress
            }
            defaultBillingAddress {
                firstName
                lastName
                companyName
                streetAddress1
                streetAddress2
                city
                cityArea
                postalCode
                countryArea
                phone
                country {
                    code
                }
                isDefaultShippingAddress
                isDefaultBillingAddress
            }
            avatar {
                url
            }
            userPermissions {
                code
                sourcePermissionGroups(userId: $id) {
                    name
                }
            }
            permissionGroups {
                name
                permissions {
                    code
                }
            }
            editableGroups {
                name
            }
        }
    }
"""


def test_query_customer_user(staff_api_client,
    customer_user,
    address,
    permission_manage_users,
    media_root,
    settings,):
    query = FULL_USER_QUERY


    assert executed == {"data": {"customers_grigo": {"edges": []}
  }
}
