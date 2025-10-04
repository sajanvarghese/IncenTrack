from django.urls import path
from .views import dashboard_views, salesmen_views,incentives_views,reports_views
urlpatterns = [
    path('',dashboard_views.login_view,name="login"),
    path('dashboard/',dashboard_views.base_view, name="base"),
    path('logout/',dashboard_views.logout_view, name="logout"),
    path('salesmen/', salesmen_views.salesman_list_view, name="salesman_list"),
    path('salesmen/add/', salesmen_views.add_salesman_view, name="add_salesman"),
    path('salesmen/edit/<int:id>/', salesmen_views.edit_salesman_view, name="edit_salesman"),
    path('salesmen/delete/<int:id>/', salesmen_views.delete_salesman_view, name="delete_salesman"),
    path('monthly-incentives/', incentives_views.monthly_incentive_view, name="monthly_incentives"),
    path('monthly-incentive/', incentives_views.monthly_incentive_view, name="monthly_incentive"),
    path('monthly-incentive/add/<int:salesman_id>/', incentives_views.add_incentive_details_view, name="add_incentive_details"),
    path("reports/", reports_views.reports_view, name="reports"),
]

