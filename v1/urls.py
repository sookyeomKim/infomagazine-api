from django.conf import settings
from django.urls import path, include

from infomagazine.custom_packages import DefaultRouter

from v1.db.urls import router as db_router, companies_router
from v1.landingpage.urls import router as landingpage_router
from v1.organization.urls import router as organization_router
from v1.user.urls import router as user_router
from v1.views import custom_token_obtain_pair, custom_token_refresh
from v1.company.urls import router as company_router

router = DefaultRouter()
router.extend(user_router)
router.extend(organization_router)
router.extend(company_router)
router.extend(landingpage_router)
router.extend(db_router)

api_urlpatterns = ([
                       path('', include((router.urls, 'root_router'), namespace='router')),
                       path('', include((companies_router.urls, 'companies_router'), namespace='companies_router')),
                       path('auth/', custom_token_obtain_pair, name='token_obtain'),
                       path('auth/refresh/', custom_token_refresh, name='token_refresh'),
                   ], 'v1')

if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title='Infomagzine API')
    api_urlpatterns[0].append(path('swagger/', schema_view, name='swagger'))
