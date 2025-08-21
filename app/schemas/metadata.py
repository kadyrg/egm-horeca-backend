from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class Header(BaseModel):
    title: str
    search_placeholder: Annotated[str, Field(alias="searchPlaceholder")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class TopBar(BaseModel):
    store_location: Annotated[str, Field(alias="storeLocation")]
    store_location_url: Annotated[str, Field(alias="storeLocationURL")]
    phone: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class BottomNav(BaseModel):
    home: Annotated[str, Field(alias="home")]
    categories: Annotated[str, Field(alias="categories")]
    likes: Annotated[str, Field(alias="likes")]
    cart: Annotated[str, Field(alias="cart")]
    profile: Annotated[str, Field(alias="profile")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class RootLayout(BaseModel):
    header: Header
    top_bar: Annotated[TopBar, Field(alias="topBar")]
    bottom_nav: Annotated[BottomNav, Field(alias="bottomNav")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class HomePage(BaseModel):
    title: str
    description: str
    tops: str
    news: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductPage(BaseModel):
    add_to_cart: Annotated[str, Field(..., alias="addToCart")]
    checkout_now: Annotated[str, Field(..., alias="checkoutNow")]
    description: str
    related: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class RegisterPage(BaseModel):
    title: Annotated[str, Field(alias="title")]
    description: Annotated[str, Field(alias="description")]
    page_title: Annotated[str, Field(alias="pageTitle")]
    google_button: Annotated[str, Field(alias="googleButton")]
    first_name_placeholder: Annotated[str, Field(alias="firstNamePlaceholder")]
    last_name_placeholder: Annotated[str, Field(alias="lastNamePlaceholder")]
    email_placeholder: Annotated[str, Field(alias="emailPlaceholder")]
    phone_number_placeholder: Annotated[str, Field(alias="phoneNumberPlaceholder")]
    password_placeholder: Annotated[str, Field(alias="passwordPlaceholder")]
    signup_button: Annotated[str, Field(alias="signupButton")]
    already: Annotated[str, Field(alias="already")]
    sign_in: Annotated[str, Field(alias="signIn")]
    or_txt: Annotated[str, Field(alias="orTxt")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class LoginPage(BaseModel):
    title: Annotated[str, Field(alias="title")]
    description: Annotated[str, Field(alias="description")]
    page_title: Annotated[str, Field(alias="pageTitle")]
    google_button: Annotated[str, Field(alias="googleButton")]
    email_placeholder: Annotated[str, Field(alias="emailPlaceholder")]
    password_placeholder: Annotated[str, Field(alias="passwordPlaceholder")]
    signin_button: Annotated[str, Field(alias="signinButton")]
    or_txt: Annotated[str, Field(alias="orTxt")]
    dont_have: Annotated[str, Field(alias="dontHave")]
    sign_up: Annotated[str, Field(alias="signUp")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class VerifyEmailPage(BaseModel):
    title: Annotated[str, Field(alias="title")]
    description: Annotated[str, Field(alias="description")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class Shared(BaseModel):
    add_to_cart: Annotated[str, Field(alias="addToCart")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
