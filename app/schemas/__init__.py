from .statuses import StatusRes
from .categories import CategoryAdminList, CategoryList, CategoryDetail
from .products import ProductList, ProductDetail, ProductDetailAll
from .login import Login
from .register import Register, RegisterResponse
from .metadata import RootLayout, HomePage, ProductPage, RegisterPage, VerifyEmailPage


__all__ = [
    'StatusRes',
    'CategoryAdminList', "CategoryList", 'CategoryDetail',
    'ProductList', 'ProductDetail', 'ProductDetailAll',
    'Login',
    'Register', 'RegisterResponse',
    'RootLayout', 'HomePage', 'ProductPage', 'RegisterPage', 'VerifyEmailPage'
]
