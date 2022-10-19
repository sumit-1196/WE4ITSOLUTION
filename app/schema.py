from .query import schema
import graphene
import graphql_jwt


class Query(schema.query, graphene.ObjectType):
    pass


class Mutation(schema.mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
