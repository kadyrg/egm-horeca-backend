from fastapi import UploadFile, HTTPException, Request
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.schemas import BannerListView, BannerListAdmin, StatusRes, BannerList
from app.models import Banner
from app.utils import save_banner_image, delete_media_file, revalidate_frontend


# Admin

async def add_banner(image: UploadFile, session: AsyncSession) -> BannerListView:
    image_bytes = await image.read()
    image_path=save_banner_image(image_bytes)

    banner = Banner(image=image_path)
    session.add(banner)
    await session.commit()
    await revalidate_frontend(["banners"])
    return BannerListView.model_validate(banner)

async def get_banners_admin(page: int, session: AsyncSession) -> BannerListAdmin:
    total_stmt = select(func.count(Banner.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(Banner)
        .order_by(-Banner.id)
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    banners = result.scalars().all()

    return BannerListAdmin(
        data=[BannerListView.model_validate(banner) for banner in banners],
        total=total,
        initial=(page - 1) * 25 + 1 if banners else 0,
        last=(page - 1) * 25 + len(banners),
        total_pages=(total + 25 - 1) // 25,
        page=page,
    )
async def delete_banner_admin(category_id: int, session: AsyncSession) -> StatusRes:
    stmt = select(Banner).where(Banner.id == category_id)
    result = await session.execute(stmt)
    banner = result.scalar_one_or_none()
    if banner is None:
        raise HTTPException(status_code=404, detail="Banner not found")
    delete_media_file(banner.image)
    await session.delete(banner)
    await session.commit()
    await revalidate_frontend(["banners"])
    return StatusRes(
        status="success",
        message="Banner deleted successfully",
    )


async def update_banner_admin(
    id: int, image: UploadFile | None, session: AsyncSession
) -> BannerListView:
    stmt = select(Banner).where(Banner.id == id)
    result = await session.execute(stmt)
    banner = result.scalar_one_or_none()
    if banner is None:
        raise HTTPException(status_code=404, detail="Banner not found")
    image_to_delete: str | None = None
    if image:
        image_to_delete = banner.image
        image_bytes = await image.read()
        new_image_path = save_banner_image(image_bytes)
        banner.image = new_image_path
    await session.commit()
    if image_to_delete:
        delete_media_file(image_to_delete)
    await revalidate_frontend(["banners"])
    return BannerListView.model_validate(banner)


# Client

async def get_banners(request: Request, session: AsyncSession) -> List[BannerList]:
    stmt = (
        select(Banner)
        .order_by(-Banner.id)
    )
    result = await session.execute(stmt)
    banners = result.scalars().all()
    base_url = str(request.base_url)
    return [
        BannerList(
            id=banner.id,
            image=f"{base_url}{banner.image}"
        ) for banner in banners
    ]
