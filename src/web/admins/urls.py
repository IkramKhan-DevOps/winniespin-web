from django.urls import path
from .views import (
    DashboardView,
    UserListView, UserPasswordResetView, UserDetailView, UserUpdateView,
    EventListView, EventDetailView, EventDeleteView, EventUpdateView, EventCreateView, LuckyDrawView, spin_json_view,
    WinnerView, ResultUpdateView
)


app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

    path('event/', EventListView.as_view(), name='event-list'),
    path('event/add/', EventCreateView.as_view(), name='event-add'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    path('event/<int:pk>/spin/', LuckyDrawView.as_view(), name="lucky-draw"),
    path('event/<int:pk>/winner/', WinnerView.as_view(), name="lucky-draw-winner"),
    path('event/<int:pk>/result/', ResultUpdateView.as_view(), name="event-result"),

]

urlpatterns += [
    path('json/event/<str:event_id>/token_number/<str:token_number>/', spin_json_view, name='json-spin-view')
]