# richiamare in saleor.graphql.api


from .accountGrigo.graphql.mutation import CustomerCreateGrigo, CustomerUpdateGrigo
from .accountGrigo.graphql.schema import AccountQueries

class GrigoprintQueries(
    AccountQueries
):
    pass


class GrigoprintMutations():
    customer_create_grigo = CustomerCreateGrigo.Field()
    customer_update_grigo = CustomerUpdateGrigo.Field()
