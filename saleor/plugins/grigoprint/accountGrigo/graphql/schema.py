from itertools import permutations
import graphene


from .type import UserGrigo

class AccountQueries(graphene.ObjectType):
    
    users_grigo = graphene.List(
        UserGrigo,
        description="Look up a user by ID or email address.",
    )
    user_grigo = graphene.Field(
        UserGrigo,
        id=graphene.Argument(graphene.ID, description="ID of the user."),
        email=graphene.Argument(
            graphene.String, description="Email address of the user."
        ),
        
        description="Look up a user by ID or email address.",
    )