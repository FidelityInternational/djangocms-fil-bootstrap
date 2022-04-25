
class DisableMigrations(object):
    """
    Django-cms disables all migrations when they run their tests.
    It would be better to not do it. Right now we are forced to disable our
    migrations because we inherit one of our models from django-cms.
    The error in question is due to an incompability of sqlite3 and
    with atomic transactions.
    """
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


HELPER_SETTINGS = {
    "SECRET_KEY": "djangocms-fil-bootstrap-tests",
    "TIME_ZONE": "America/Chicago",
    "INSTALLED_APPS": [
        "djangocms_text_ckeditor",
        "djangocms_column",
        "djangocms_fil_bootstrap",
        "djangocms_versioning",
        "djangocms_version_locking",
        "djangocms_moderation",
    ],
    "CMS_PERMISSION": True,
    "LANGUAGES": (
        ("en", "English"),
        ("de", "German"),
        ("fr", "French"),
        ("it", "Italiano"),
    ),
    "MIGRATION_MODULES": DisableMigrations(),
    "CMS_LANGUAGES": {
        1: [
            {"code": "en", "name": "English", "fallbacks": ["de", "fr"]},
            {
                "code": "de",
                "name": "Deutsche",
                "fallbacks": ["en"],  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                "code": "fr",
                "name": "Française",
                "fallbacks": ["en"],  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                "code": "it",
                "name": "Italiano",
                "fallbacks": ["fr"],  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ]
    },
    "PARLER_ENABLE_CACHING": False,
    "LANGUAGE_CODE": "en",
    "DEFAULT_AUTO_FIELD": "django.db.models.AutoField",
}


def run():
    from app_helper import runner

    runner.cms("djangocms_fil_bootstrap", extra_args=[])


if __name__ == "__main__":
    run()
