from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from sqlalchemy import select

from app.models import ProductVariant
from app.schemas import ProductVariantIn, StatusRes, ProductVariantListView


async def add_product_variant(
    product_variant_in: ProductVariantIn, session: AsyncSession
) -> StatusRes:
    product_variant = ProductVariant(
        name_ro=product_variant_in.name_ro,
        name_en=product_variant_in.name_en,
        price=product_variant_in.price,
        stock=product_variant_in.stock,
        variant_type_id=product_variant_in.variant_type_id,
        product_id=product_variant_in.product_id,
    )
    session.add(product_variant)
    await session.commit()
    return StatusRes(
        status="success",
        message="Product Variant Added",
    )

async def get_product_variants_all(
    session: AsyncSession
) -> List[ProductVariantListView]:
    stmt = select(ProductVariant)
    result = await session.execute(stmt)
    product_variants = result.scalars().all()
    return [ProductVariantListView.model_validate(product_variant) for product_variant in product_variants]
