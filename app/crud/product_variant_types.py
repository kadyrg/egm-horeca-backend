from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.schemas import (
    ProductVariantTypeIn,
    ProductVariantTypeListView,
    ProductVariantTypeListAdmin,
    StatusRes,ProductVariantsListAdmin,ProductVariantListView,ProductVariantTypeListViewAll
)
from app.models import ProductVariantType, ProductVariant


# Admin


async def add_product_variant_type(
    product_variant_type_in: ProductVariantTypeIn, session: AsyncSession
) -> StatusRes:
    product_variant_type = ProductVariantType(
        name_ro=product_variant_type_in.name_ro,
        name_en=product_variant_type_in.name_en,
    )
    session.add(product_variant_type)
    await session.commit()
    return StatusRes(
        status="success",
        message="Product Variant Type Added",
    )


async def get_product_variant_types(
    page: int, session: AsyncSession
) -> ProductVariantTypeListAdmin:
    total_stmt = select(func.count(ProductVariantType.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(
            ProductVariantType,
            func.count(ProductVariant.id).label("variants_count"),
        )
        .outerjoin(ProductVariant, ProductVariant.variant_type_id == ProductVariantType.id)
        .group_by(ProductVariantType.id)
        .order_by(ProductVariantType.id.desc())
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    rows = result.all()
    product_variant_types = [
        ProductVariantTypeListView.model_validate({
            **row[0].__dict__,
            "variants_count": row.variants_count,
        }) for row in rows
    ]
    return ProductVariantTypeListAdmin(
        data=product_variant_types,
        total=total,
        initial=(page - 1) * 25 + 1 if rows else 0,
        last=(page - 1) * 25 + len(rows),
        total_pages=(total + 25 - 1) // 25,
        page=page,
    )


async def update_product_variant_type(
    product_variant_type_in: ProductVariantTypeIn,
    product_variant_type_id: int,
    session: AsyncSession,
) -> StatusRes:
    stmt = select(ProductVariantType).where(
        ProductVariantType.id == product_variant_type_id
    )
    result = await session.execute(stmt)
    product_variant_type = result.scalar_one_or_none()
    if product_variant_type is None:
        raise HTTPException(status_code=404, detail="Product Variant Type not found")
    product_variant_type.name_ro = product_variant_type_in.name_ro
    product_variant_type.name_en = product_variant_type_in.name_en
    await session.commit()
    return StatusRes(status="success", message="Product Variant Type Updated")


async def delete_product_variant_type(
    product_variant_type_id: int, session: AsyncSession
) -> StatusRes:
    stmt = select(ProductVariantType).where(
        ProductVariantType.id == product_variant_type_id
    )
    result = await session.execute(stmt)
    product_variant_type = result.scalar_one_or_none()
    if product_variant_type is None:
        raise HTTPException(status_code=404, detail="Product Variant Type not found")
    await session.delete(product_variant_type)
    await session.commit()
    return StatusRes(
        status="success",
        message="Product Variant Type deleted",
    )


async def get_product_variant_types_all(
    session: AsyncSession,
) -> List[ProductVariantTypeListViewAll]:
    stmt = select(ProductVariantType).order_by(-ProductVariantType.id)
    result = await session.execute(stmt)
    product_variant_types = result.scalars().all()
    return [
        ProductVariantTypeListViewAll.model_validate(product_variant_type)
        for product_variant_type in product_variant_types
    ]

async def get_variants_of_product_variant_type(
    product_variant_type_id: int,
    page: int,
    session: AsyncSession,
) -> ProductVariantsListAdmin:
    total_stmt = (
        select(func.count(ProductVariantType.id))
        .where(ProductVariantType.id == product_variant_type_id)
    )
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(ProductVariant)
        .where(ProductVariant.variant_type_id == product_variant_type_id)
        .order_by(ProductVariant.id.desc())
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    product_variants = result.scalars().all()
    return ProductVariantsListAdmin(
        data=[ProductVariantListView.model_validate(product_variant) for product_variant in product_variants],
        total=total,
        initial=(page - 1) * 25 + 1 if product_variants else 0,
        last=(page - 1) * 25 + len(product_variants),
        total_pages=(total + 25 - 1) // 25,
        page=page,
    )
