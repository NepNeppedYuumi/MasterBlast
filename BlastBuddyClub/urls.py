from django.contrib import admin
from django.urls import path
from Blaster.views.index import index_page
from Blaster.views.blast_results import blast_result_page, share_to_buddie
from Blaster.views.blast_hit import blast_hit_page
from Blaster.views.loading import loading_result_page, get_processed_status
from Blaster.views.login import login_page, logout_view
from Blaster.views.signup import signup_page
from Blaster.views.recent import recent_page
from Blaster.views.personalia import personalia_page, remove_buddie, search_user, add_buddie
from Blaster.views.comparison import comparison_page


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", login_page, name="login"),
    path("signup", signup_page, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("", index_page),
    path("blast_result/<int:blast_job_id>", blast_result_page),
    path("recent", recent_page),
    path("personalia", personalia_page, name="personalia_page"),
    path("comparison", comparison_page, name="comparison"),
    path("loading_result/<int:job_id>", loading_result_page),
    path("loading_result/get_processed_status/<int:job_id>",
         get_processed_status),
    path("blast_hit/<int:blast_hit_id>", blast_hit_page),
    path('remove_buddie/<str:user_username>/<str:buddie_username>/',
          remove_buddie, name='remove_buddie'),
    path('search_user/', search_user, name='search_user'),
    path('add_buddie/<str:buddie_username>/',
          add_buddie, name='add_buddie'),
    path('share_to_buddie/<int:job_id>/<str:buddie_username>/',
          share_to_buddie, name='share_to_buddie'),
]

handler403 = 'Blaster.views.errors.permission_denied.permission_denied_page'
handler404 = 'Blaster.views.errors.does_not_exist.does_not_exist_page'
handler500 = 'Blaster.views.errors.server_error.server_error_page'