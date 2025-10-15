from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import crud
from ..schemas import UserCreate, User
from ..auth import require_admin, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[User])
async def read_users(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "admin":
        # Обычный пользователь видит только себя
        return [current_user]
    return await crud.get_all_users(db)

@router.post("/", response_model=User)
async def create_new_user(
    user: UserCreate,
    admin = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_user(db, user)

@router.delete("/{user_id}")
async def remove_user(
    user_id: int,
    admin = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "Deleted"}