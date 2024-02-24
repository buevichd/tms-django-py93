from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote', views.choice_vote),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/update', views.UpdateCartView.as_view(), name='update_cart'),
]
