"""shop URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from products.views import ProductsView, ProductDetail, export_csv,\
     import_csv, ExportPDF

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<uuid:pk>/', ProductDetail.as_view(),
         name='product_detail'),
    path('products/csv/', export_csv, name='export_csv'),
    path('products/pdf/', ExportPDF.as_view(), name='export_pdf'),
    path('products/import/', import_csv, name='import_csv'),
]