from faker import Faker


def get_fake_user(self, domain, password):
    fake = Faker()
    first = fake.first_name()
    last = fake.last_name()
    email = '{}.{}@{}'.format(first.lower(), last.lower(), domain)
    user = {
        'profile': {
            'firstName': first,
            'lastName': last,
            'email': email,
            'login': email,
            'mobilePhone': fake.phone_number(),
        },
        'credentials': {
            'password': {
                'value': password
            }
        }
    }
    return user
