from django.contrib import admin
from django.urls import path
from spendingtrackers import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page, name ='home_page'),
    path('feed/',views.feed, name ='feed'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('new_transaction/',views.new_transaction, name ='new_transaction'),
    path('edit_category_details/<int:id>', views.edit_category_details, name='edit_category_details'),
    path('records/', views.records, name='records'),
    path('update_record/<int:id>', views.update_record, name='update_record'),
    path('sign_success/', views.sign_success, name='sign_success'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('banner/', views.banner, name='banner'),
    path('delete_record/<int:id>', views.delete_record, name='delete_record'),
    path('category/',views.category, name='category'),
    path('view_category/<int:id>', views.view_category, name='view_category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/balance_chart', views.chart_balance_graph, name='chart_balance_graph'),
    path('dashboard/expense_chart', views.chart_expense_graph, name='chart_expense_graph'),
    path('dashboard/income_chart', views.chart_income_graph, name='chart_income_graph'),
    path('dashboard/expense_structure', views.expense_structure, name='expense_structure'),
    path('dashboard/expense_structure2', views.expense_structure2, name='expense_structure2'),
    path('add_category_details/', views.add_category_details, name='add_category_details'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('overall/',views.overall, name ='overall'),
    path('view_achievements/', views.view_achievements, name='view_achievements'),
]
urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
