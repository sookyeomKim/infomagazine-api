from infomagazine.custom_packages import DefaultRouter
from v1.company.views import CompanyViewSets

router = DefaultRouter()
router.register(r'companies', CompanyViewSets, basename='company')
