import factory
from faker import Factory as FakerFactory


faker = FakerFactory.create()


class RedirectFactory(factory.DjangoModelFactory):
    local_path = factory.LazyAttribute(lambda n: faker.uri_path())
    destination_url = factory.LazyAttribute(lambda n: faker.uri())
    sender_ip = factory.LazyAttribute(lambda n: faker.ipv4())

    class Meta:
        model = 'redirects.Redirect'
