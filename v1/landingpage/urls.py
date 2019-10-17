from infomagazine.custom_packages import DefaultRouter
from v1.landingpage.views import LandingPageViewSets

router = DefaultRouter()
router.register(r'landing_pages', LandingPageViewSets, basename='landing-page')
