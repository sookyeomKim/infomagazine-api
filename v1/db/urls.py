from rest_framework_nested import routers as nested_router
from v1.landingpage.urls import router
from v1.db.views import LandingPageDBViewSets

companies_router = nested_router.NestedDefaultRouter(router, r'landing_pages', lookup='landing_page')
companies_router.register(r'landing_dbs', LandingPageDBViewSets, basename='landing-db')
