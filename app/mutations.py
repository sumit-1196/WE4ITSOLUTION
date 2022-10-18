import graphene
import re
from .models import Creditor, Fuel, Machine, Payment
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id
from graphql_jwt.decorators import superuser_required
User = get_user_model()

# CRUD OPERATION FOR USER


class UserType(DjangoObjectType):
    class Meta:
        model = User


def passwords_match(password):
    regexp = r'[@#%]+[0-9]+@*[a-zA-Z]+'
    sorted_x = ''.join(sorted(password))
    if '@' in sorted_x:
        sorted_x = '@%s' % sorted_x
    p = re.compile(regexp)
    if p.match(sorted_x) is None:
        return False
    return True


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        mobile = graphene.String()
        password = graphene.String()
        authorisation = graphene.String()

    user = graphene.Field(UserType)

    @superuser_required
    def mutate(self, info, name, mobile, password, authorisation):
        try:
            if not passwords_match(password):
                return GraphQLError('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters')
            user = User.objects.create_user(
                name=name, username=mobile, password=password, authorisation=authorisation
            )
            response = CreateUser(user=user)
            return response
        except Exception as e:
            raise GraphQLError("user already exist")


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        mobile = graphene.String()
        password = graphene.String()
        authorisation = graphene.String()

    user = graphene.Field(UserType)

    @superuser_required
    def mutate(self, info, id, name, mobile, password, authorisation):
        try:
            user = User.objects.get(id=from_global_id(id)[1])
            if len(password):
                if not passwords_match(password):
                    return GraphQLError('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters')
                user.set_password(password)
            user.name = name
            user.username = mobile
            user.authorisation = authorisation
            user.save()
            response = UpdateUser(user=user)
            return response
        except Exception as e:
            raise GraphQLError("user already exist")


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    user = graphene.Field(UserType)
    success = graphene.Boolean()

    @superuser_required
    def mutate(self, info, id):
        try:
            user = User.objects.get(id=from_global_id(id)[1])
            user.delete()
            response = DeleteUser(success=True)
            return response
        except Exception as e:
            raise GraphQLError(e)


# CRUD OPERATION FOR FUEL
class FuelType(DjangoObjectType):
    class Meta:
        model = Fuel


class CreateFuel(graphene.Mutation):
    class Arguments:
        type = graphene.String()
        price = graphene.Float()

    fuel = graphene.Field(FuelType)

    @superuser_required
    def mutate(self, info, type, price):
        try:
            fuel = Fuel.objects.create(type=type, price=price)
            response = CreateFuel(fuel=fuel)
            return response
        except Exception as e:
            raise GraphQLError('fuel already exist')


class UpdateFuel(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        type = graphene.String()
        price = graphene.Float()

    fuel = graphene.Field(FuelType)

    @superuser_required
    def mutate(self, info, id, type, price):
        try:
            fuel = Fuel.objects.get(id=from_global_id(id)[1])
            fuel.type = type
            fuel.price = price
            fuel.save()
            response = UpdateFuel(fuel=fuel)
            return response
        except Exception as e:
            raise GraphQLError('fuel already exist')


class DeleteFuel(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    fuel = graphene.Field(FuelType)
    success = graphene.Boolean()

    @superuser_required
    def mutate(self, info, id):
        try:
            fuel = Fuel.objects.get(id=from_global_id(id)[1])
            fuel.delete()
            response = DeleteFuel(success=True)
            return response
        except Exception as e:
            raise GraphQLError(e)


# CRUD OPERATION FOR MACHINE
class MachineType(DjangoObjectType):
    class Meta:
        model = Machine


class CreateMachine(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        fuel = graphene.ID()
        reading = graphene.Float()

    machine = graphene.Field(MachineType)

    @superuser_required
    def mutate(self, info, name, fuel, reading):
        try:
            machine = Machine.objects.create(
                name=name,
                fuel=Fuel.objects.get(id=from_global_id(fuel)[1]),
                reading=reading
            )
            response = CreateMachine(machine=machine)
            return response
        except Exception as e:
            raise GraphQLError(e)


class UpdateMachine(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        fuel = graphene.ID()
        reading = graphene.Float()

    machine = graphene.Field(MachineType)

    @superuser_required
    def mutate(self, info, id, name, fuel, reading):
        try:
            machine = Machine.objects.get(id=from_global_id(id)[1])
            f = Fuel.objects.get(id=from_global_id(fuel)[1])
            machine.fuel = f
            machine.name = name
            machine.reading = reading
            machine.save()
            response = UpdateMachine(machine=machine)
            return response
        except Exception as e:
            raise GraphQLError(e)


class DeleteMachine(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    machine = graphene.Field(MachineType)
    success = graphene.Boolean()

    @superuser_required
    def mutate(self, info, id):
        try:
            machine = Machine.objects.get(id=from_global_id(id)[1])
            machine.delete()
            response = DeleteMachine(success=True)
            return response
        except Exception as e:
            raise GraphQLError(e)


# CRUD OPERATION PAYMENT
class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment


class CreatePayment(graphene.Mutation):
    class Arguments:
        allowed_subcategory = graphene.Boolean()
        mode = graphene.String()

    payment = graphene.Field(PaymentType)

    @superuser_required
    def mutate(self, info, allowed_subcategory, mode):
        try:
            payment = Payment.objects.create(
                allowed_subcategory=allowed_subcategory,
                mode=mode
            )
            response = CreatePayment(payment=payment)
            return response
        except Exception as e:
            raise GraphQLError(e)


class UpdatePayment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        allowed_subcategory = graphene.Boolean()
        mode = graphene.String()

    payment = graphene.Field(PaymentType)

    @superuser_required
    def mutate(self, info, id, allowed_subcategory, mode):
        try:
            payment = Payment.objects.get(id=from_global_id(id)[1])
            payment.allowed_subcategory = allowed_subcategory
            payment.mode = mode
            payment.save()
            response = UpdatePayment(payment=payment)
            return response
        except Exception as e:
            raise GraphQLError(e)


class DeletePayment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    payment = graphene.Field(PaymentType)
    success = graphene.Boolean()

    @superuser_required
    def mutate(self, info, id):
        print('COMING')
        try:
            payment = Payment.objects.get(id=from_global_id(id)[1])
            payment.delete()
            response = DeletePayment(success=True)
            return response
        except Exception as e:
            raise GraphQLError(e)


# CRUD OPERATION FOR MACHINE
class CreditorType(DjangoObjectType):
    class Meta:
        model = Creditor


class CreateCreditor(graphene.Mutation):
    class Arguments:
        payment = graphene.ID()
        name = graphene.String()
        limit_warning = graphene.String()
        limit_stop_credit = graphene.String()

    creditor = graphene.Field(CreditorType)

    @superuser_required
    def mutate(self, info, payment, name, limit_warning, limit_stop_credit):
        try:
            creditor = Creditor.objects.create(
                payment=Payment.objects.get(id=from_global_id(payment)[1]),
                name=name,
                limit_warning=limit_warning,
                limit_stop_credit=limit_stop_credit
            )
            response = CreateCreditor(creditor=creditor)
            return response
        except Exception as e:
            raise GraphQLError(e)


class UpdateCreditor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        payment = graphene.ID()
        name = graphene.String()
        limit_warning = graphene.String()
        limit_stop_credit = graphene.String()

    creditor = graphene.Field(CreditorType)

    @superuser_required
    def mutate(self, info, id, payment, name, limit_warning, limit_stop_credit):
        try:
            creditor = Creditor.objects.get(id=from_global_id(id)[1])
            p = Payment.objects.get(id=from_global_id(payment)[1])
            creditor.payment = p
            creditor.name = name
            creditor.limit_warning = limit_warning
            creditor.limit_stop_credit = limit_stop_credit
            creditor.save()
            response = UpdateCreditor(creditor=creditor)
            return response
        except Exception as e:
            raise GraphQLError(e)


class DeleteCreditor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    creditor = graphene.Field(CreditorType)
    success = graphene.Boolean()

    @superuser_required
    def mutate(self, info, id):
        try:
            creditor = Creditor.objects.get(id=from_global_id(id)[1])
            creditor.delete()
            response = DeleteCreditor(success=True)
            return response
        except Exception as e:
            raise GraphQLError(e)


# LIST OF ALL MUTATIONS
class Mutation(graphene.ObjectType):

    # User Mutations
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    # Fuel Mutations
    create_fuel = CreateFuel.Field()
    update_fuel = UpdateFuel.Field()
    delete_fuel = DeleteFuel.Field()

    # Fuel Mutations
    create_machine = CreateMachine.Field()
    update_machine = UpdateMachine.Field()
    delete_machine = DeleteMachine.Field()

    # Payment Mutations
    create_payment = CreatePayment.Field()
    update_payment = UpdatePayment.Field()
    delete_payment = DeletePayment.Field()

    # Creditor Mutations
    create_creditor = CreateCreditor.Field()
    update_creditor = UpdateCreditor.Field()
    delete_creditor = DeleteCreditor.Field()
