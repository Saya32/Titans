from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from spendingtrackers.views import category_views, dashboard_views, profile_login_views, records_views, transaction_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',profile_login_views.home_page, name ='home_page'),
    path('feed/',profile_login_views.feed, name ='feed'),
    path('sign_up/', profile_login_views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', profile_login_views.LogInView.as_view(), name='log_in'),
    path('log_out/', profile_login_views.log_out, name='log_out'),
    path('profile/', profile_login_views.ProfileUpdateView.as_view(), name='profile'),
    path('new_transaction/',transaction_views.new_transaction, name ='new_transaction'),
    path('edit_category_details/<int:id>', category_views.edit_category_details, name='edit_category_details'),
    path('records/', records_views.records, name='records'),
    path('update_record/<int:id>', records_views.update_record, name='update_record'),
    path('sign_success/', profile_login_views.sign_success, name='sign_success'),
    path('forgot_password/', profile_login_views.forgot_password, name='forgot_password'),
    path('banner/', profile_login_views.banner, name='banner'),
    path('delete_record/<int:id>', records_views.delete_record, name='delete_record'),
    path('category/',category_views.category, name='category'),
    path('view_category/<int:id>', category_views.view_category, name='view_category'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/balance_chart', dashboard_views.chart_balance_graph, name='chart_balance_graph'),
    path('dashboard/expense_chart', dashboard_views.chart_expense_graph, name='chart_expense_graph'),
    path('dashboard/income_chart', dashboard_views.chart_income_graph, name='chart_income_graph'),
    path('dashboard/expense_structure', dashboard_views.expense_structure.expense_structure, name='expense_structure'),
    path('dashboard/expense_structure2', dashboard_views.expense_structure2, name='expense_structure2'),
    path('add_category_details/', category_views.add_category_details, name='add_category_details'),
    path('delete_category/<int:id>', category_views.delete_category, name='delete_category'),
    path('overall/',category_views.overall, name ='overall'),
    path('view_achievements/', profile_login_views.view_achievements, name='view_achievements'),
]
urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

