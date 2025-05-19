from fastapi import APIRouter
from .endpoints import users, team_members, objectives, progress_updates, rewrite_text, key_results

api_router = APIRouter()
api_router.include_router(users.users_public_router, prefix="/users", tags=["users"])
api_router.include_router(users.users_router, prefix="/users", tags=["users"])
api_router.include_router(team_members.router, prefix="/team-members", tags=["team-members"])
api_router.include_router(objectives.router, prefix="/objectives", tags=["objectives"])
api_router.include_router(progress_updates.router, prefix="/progress-updates", tags=["progress-updates"])
api_router.include_router(key_results.router, prefix="/key-results", tags=["key-results"])
api_router.include_router(rewrite_text.router, prefix="/rewrite-text", tags=["rewrite-text"])
