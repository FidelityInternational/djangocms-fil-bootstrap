from cms import __version__ as cms_version

try:
    from packaging.version import Version
except ModuleNotFoundError:
    from distutils.version import LooseVersion as Version


DJANGO_CMS_4_1 = Version(cms_version) >= Version('4.1')
