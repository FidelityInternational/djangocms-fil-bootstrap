from django.contrib.auth import get_user_model

import factory
from factory.fuzzy import FuzzyText


class UserFactory(factory.django.DjangoModelFactory):
    username = FuzzyText(length=12)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda u: "%s.%s@example.com" % (u.first_name.lower(), u.last_name.lower())
    )

    class Meta:
        model = get_user_model()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Return existing user instance if found.
        Otherwise create a new user."""
        manager = cls._get_manager(model_class)
        username = kwargs.get("username")
        if username is not None:
            try:
                return manager.get(username=username)
            except model_class.DoesNotExist:
                pass
        return manager.create_user(*args, **kwargs)
