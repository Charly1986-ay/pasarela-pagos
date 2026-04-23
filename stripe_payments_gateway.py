import os
import dotenv
import stripe

# Configuración del entorno
dotenv.load_dotenv()
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

stripe.api_key=STRIPE_SECRET_KEY

# Crear un metodo de pago
def create_payment_method() -> str:

    try:
        # Aca se genera el metodo de pago
        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={'token': 'tok_visa'}
        )
        print(payment_method)

        print(f'Método de pago con ID: {payment_method.id}')

        return payment_method.id
    except stripe.StripeError as e:
        print(e.user_message)


# crear un pago
def create_payment(client_id: str, payment_method_id: str):
    try:
        payment=stripe.PaymentIntent.create(
            # OJO sea usd o euros hay que convertirlos en CENTIMOS
            amount=5 * 100, # se multiplica por 100
            currency='usd',
            customer=client_id,
            payment_method=payment_method_id,
            payment_method_types=['card'],
            confirm=True
        )

        print(f'Pago con ID {payment.id} realizada correctamente.')
    except stripe.CardError as e:
        print(f'Error en la tarjeta: {e.user_message}')
    except stripe.StripeError as e:
        print(f'Error en stripe: {e.user_message}')


# creacion de usuario segun al api stripe
def create_user(name: str, email:str):
    try:
        client = stripe.Customer.create(
            name=name,
            email=email
        )
        print(f'Cliente {client.name} creado correctamente con ID: {client.id}')

        return client.id
    except stripe.StripeError as e:
        print(f'Error en stripe: {e.user_message}')


# Asociar el método de pago al usuario
def add_payment_method_to_user(client_id, payment_method_id):
    # asocia el cliente con el método de pago
    stripe.PaymentMethod.attach(
        payment_method_id=payment_method_id,
        customer=client_id
    )

    print('método de pago asociado al usuario')


# Prueba
client_id = create_user(name='Pepito Perez', email='pepito@example.com')

payment_method_id=create_payment_method()

add_payment_method_to_user(
    client_id=client_id, 
    payment_method_id=payment_method_id
)

create_payment(
    client_id=client_id, 
    payment_method_id=payment_method_id
)