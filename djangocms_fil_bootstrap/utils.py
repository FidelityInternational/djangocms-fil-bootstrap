from cms.models import PageContent

from djangocms_versioning.models import Version


def get_version(page):
    return Version.objects.get_for_content(
        PageContent._base_manager.filter(page=page).last()
    )
