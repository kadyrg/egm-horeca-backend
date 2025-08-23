from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import ProductInstance, Product
from app.schemas import (
    StatusRes,
    ProductListAdmin,
    ProductListView,
    ProductInstanceListAdmin,
    ProductInstanceListView
)


async def add_product_instance(session: AsyncSession) -> StatusRes:
    product_instance = ProductInstance()
    session.add(product_instance)
    await session.commit()
    return StatusRes(status="success", message="Product instance added")


async def get_product_instances_admin(page: int, session: AsyncSession) -> ProductInstanceListAdmin:
    total_stmt = select(func.count(ProductInstance.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(
            ProductInstance,
            func.count(Product.id).label("products_count")
        )
        .outerjoin(Product, Product.instance_id == ProductInstance.id)
        .group_by(ProductInstance.id)
        .order_by(ProductInstance.id.desc())
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    rows = result.all()
    data = [
        ProductInstanceListView.model_validate({
            **row[0].__dict__,
            "products_count": row.products_count
        }) for row in rows
    ]
    return ProductInstanceListAdmin(
        data=data,
        total=total,
        initial=(page - 1) * 25 + 1 if rows else 0,
        last=(page - 1) * 25 + len(rows),
        total_pages=(total + 25 - 1) // 25,
        page=page,
    )


async def delete_product_instance(product_instance_id: int, session: AsyncSession) -> StatusRes:
    stmt = (
        select(ProductInstance)
        .where(ProductInstance.id == product_instance_id)
    )
    result = await session.execute(stmt)
    product_instance = result.scalar_one_or_none()
    if product_instance is None:
        raise HTTPException(status_code=404, detail="Product instance not found")
    await session.delete(product_instance)
    await session.commit()
    return StatusRes(status="success", message="Product instance deleted")


async def get_products_of_instance_admin(
        product_instance_id: int,
        page: int,
        session: AsyncSession
) -> ProductListAdmin:
    total_stmt = (
        select(func.count(Product.id))
        .where(Product.instance_id == product_instance_id)
    )
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(Product)
        .where(Product.instance_id == product_instance_id)
        .order_by(-Product.id)
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    products = result.scalars().all()

    return ProductListAdmin(
        data=[ProductListView.model_validate(product) for product in products],
        total=total,
        initial=(page - 1) * 25 + 1 if products else 0,
        last=(page - 1) * 25 + len(products),
        total_pages=(total + 25 - 1) // 25,
        page=page,
    )
