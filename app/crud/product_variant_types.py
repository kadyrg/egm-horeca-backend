from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    func
)

from app.schemas import (
    ProductVariantTypeIn,
    ProductVariantTypeListView,
    ProductVariantTypeListAdmin, StatusRes
)
from app.models import ProductVariantType


# Admin

async def add_product_variant_type(
        product_variant_type_in: ProductVariantTypeIn,
        session: AsyncSession
) -> ProductVariantTypeListView:
    product_variant_type = ProductVariantType(
        name_ro=product_variant_type_in.name_ro,
        name_en=product_variant_type_in.name_en,
    )
    session.add(product_variant_type)
    await session.commit()
    return ProductVariantTypeListView.model_validate(product_variant_type)

async def get_product_variant_types(
        page: int,
        session: AsyncSession
) -> ProductVariantTypeListAdmin:
    total_stmt = select(func.count(ProductVariantType.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(ProductVariantType)
        .order_by(-ProductVariantType.id)
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    product_variant_types = result.scalars().all()
    return ProductVariantTypeListAdmin(
        data=[ProductVariantTypeListView.model_validate(product_variant_type) for product_variant_type in product_variant_types],
        total = total,
        initial = (page - 1) * 25 + 1 if product_variant_types else 0,
        last = (page - 1) * 25 + len(product_variant_types),
        total_pages = (total + 25 - 1) // 25,
        page = page
    )

async def update_product_variant_type(
        product_variant_type_in: ProductVariantTypeIn,
        product_variant_type_id: int,
        session: AsyncSession
) -> ProductVariantTypeListView:
    stmt = (
        select(ProductVariantType)
        .where(ProductVariantType.id == product_variant_type_id)
    )
    result = await session.execute(stmt)
    product_variant_type = result.scalar_one_or_none()
    if product_variant_type is None:
        raise HTTPException(
            status_code=404,
            detail="Product Variant Type not found"
        )
    product_variant_type.name_ro=product_variant_type_in.name_ro
    product_variant_type.name_en=product_variant_type_in.name_en
    await session.commit()
    return ProductVariantTypeListView.model_validate(product_variant_type)


async def delete_product_variant_type(
        product_variant_type_id: int,
        session: AsyncSession
) -> StatusRes:
    stmt = (
        select(ProductVariantType)
        .where(ProductVariantType.id == product_variant_type_id)
    )
    result = await session.execute(stmt)
    product_variant_type = result.scalar_one_or_none()
    if product_variant_type is None:
        raise HTTPException(
            status_code=404,
            detail="Product Variant Type not found"
        )
    await session.delete(product_variant_type)
    await session.commit()
    return StatusRes(
        status="success",
        message="Product Variant Type deleted",
    )