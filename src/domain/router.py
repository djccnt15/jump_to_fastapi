from fastapi import APIRouter

from .answer import answer_controller
from .question import question_controller

router = APIRouter(prefix="/api")

router.include_router(question_controller.router)
router.include_router(answer_controller.router)
