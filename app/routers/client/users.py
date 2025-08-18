from fastapi import APIRouter


router = APIRouter()

@router.get('/profile')
async def get_user_profile():
    pass
