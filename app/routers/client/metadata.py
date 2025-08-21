from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.deps import lang_dep
from app.models import MetaDataGroup
from app.crud import get_metadata
from app.schemas import Shared
from app.schemas.metadata import (
    HomePage,
    ProductPage,
    RegisterPage,
    VerifyEmailPage,
    RootLayout,
    LoginPage,
)


router = APIRouter(prefix="/metadata", tags=["Metadata"])


@router.get("/root_layout", response_model=RootLayout)
async def get_root_layout(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.root_layout, session)
    return RootLayout.model_validate(metadata)


@router.get("/home_page", response_model=HomePage)
async def get_home_page(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.home_page, session)
    return HomePage.model_validate(metadata)


@router.get("/product_page", response_model=ProductPage)
async def get_product_page(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.product_page, session)
    return ProductPage.model_validate(metadata)


@router.get("/register_page", response_model=RegisterPage)
async def get_register_page(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.register_page, session)
    return RegisterPage.model_validate(metadata)


@router.get("/login_page", response_model=LoginPage)
async def get_register_page(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.login_page, session)
    return LoginPage.model_validate(metadata)


@router.get("/verify_email_page", response_model=VerifyEmailPage)
async def get_verify_email_page(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.verify_email_page, session)
    return VerifyEmailPage.model_validate(metadata)


@router.get("/shared", response_model=Shared)
async def get_verify_email_page(
    lang: str = Depends(lang_dep), session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(lang, MetaDataGroup.shared, session)
    return Shared.model_validate(metadata)
