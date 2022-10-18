from django.contrib.auth import get_user_model
from .mutations import Mutation
from graphene_django import DjangoObjectType
from graphene import relay, ObjectType, Schema
from graphql_jwt.decorators import superuser_required
from .models import Creditor, Fuel, Machine, Payment
from graphene_django.filter import DjangoFilterConnectionField

User = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ["id", "username"]
        interfaces = (relay.Node, )


class FuelNode(DjangoObjectType):
    class Meta:
        model = Fuel
        filter_fields = ["id", "type", "price"]
        interfaces = (relay.Node, )


class MachineNode(DjangoObjectType):
    class Meta:
        model = Machine
        filter_fields = ["id", "name", "reading"]
        interfaces = (relay.Node, )


class PaymentNode(DjangoObjectType):
    class Meta:
        model = Payment
        filter_fields = ["id", "allowed_subcategory", "mode"]
        interfaces = (relay.Node, )


class CreditorNode(DjangoObjectType):
    class Meta:
        model = Creditor
        filter_fields = ["id", "name", "limit_warning", "limit_stop_credit"]
        interfaces = (relay.Node, )


class Query(ObjectType):
    # user query
    users = DjangoFilterConnectionField(UserNode)

    @superuser_required
    def resolve_users(self, info, **kwargs):
        return User.objects.filter(is_staff=False)

    # fuel query
    fuels = DjangoFilterConnectionField(FuelNode)

    @superuser_required
    def resolve_fuels(self, info, **kwargs):
        return Fuel.objects.all()

    # machine query
    machines = DjangoFilterConnectionField(MachineNode)

    @superuser_required
    def resolve_machines(self, info, **kwargs):
        return Machine.objects.all()

    # payment query
    payments = DjangoFilterConnectionField(PaymentNode)

    @superuser_required
    def resolve_payments(self, info, **kwargs):
        return Payment.objects.all()

    # creditor query
    creditors = DjangoFilterConnectionField(CreditorNode)

    @superuser_required
    def resolve_creditors(self, info, **kwargs):
        return Creditor.objects.all()


schema = Schema(query=Query, mutation=Mutation)
