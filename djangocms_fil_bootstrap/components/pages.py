from cms.api import add_plugin, assign_user_to_page, create_page

from ..utils import get_version
from .base import Component


class Pages(Component):
    field_name = "pages"
    default_factory = dict

    def parse(self):
        for name, data in self.raw_data.items():
            self.each(name, data)

    def each(self, name, data):
        is_home = data.pop("is_home", False)
        language = data["language"]
        publish = data.pop("publish", False)
        assignments = data.pop("assignments", [])
        content = data.pop("content", [])
        data["created_by"] = self.bootstrap.users[data["created_by"]]
        page = create_page(**data)
        if is_home:
            page.set_as_homepage()
        version = get_version(page)
        placeholder = version.content.get_placeholders().get(slot="content")
        for assignment in assignments:
            assignment["user"] = self.bootstrap.users[assignment["user"]]
            assign_user_to_page(page, **assignment)
        for plugin in content:
            self.add_plugin(placeholder, plugin, language)
        if publish:
            version.publish(data["created_by"])
        self.data[name] = page

    def add_plugin(self, placeholder, plugin_data, language, parent=None):
        type_ = plugin_data.pop("type")
        children = plugin_data.pop("children", [])
        plugin = add_plugin(placeholder, type_, language, target=parent, **plugin_data)
        for child in children:
            self.add_plugin(placeholder, child, language, parent=plugin)
