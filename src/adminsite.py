from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import PageSchema
from fastapi_user_auth.admin import AuthAdminSite, UserLoginFormAdmin
from fastapi import Request

from src.config import settings
from src.users.models import User

# Create AdminSite instance
site = AuthAdminSite(settings=Settings(database_url_async=settings.db_url))
#site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
auth = site.auth

# Registration management class
@site.register_admin
class GitHubIframeAdmin(admin.IframeAdmin):
    # Set page menu information
    page_schema = PageSchema(label='AmisIframeAdmin', icon='fa fa-github')
    # Set the jump link
    src = 'https://github.com/amisadmin/fastapi_amis_admin'


@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    page_schema = 'Category Management'
    # Configuration management model
    model = User


class UserLoginFormAdmin(UserLoginFormAdmin):
    async def has_page_permission(self, request: Request) -> bool:
        return True