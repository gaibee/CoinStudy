from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from utils.html_renderer import render_with_layout

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def dashboard():
    html_body = """
    <h3>환영합니다! 실험용 자동매매 서버입니다.</h3>
    """
    return HTMLResponse(content=render_with_layout(html_body, title="대시보드"))