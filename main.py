import yaml
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

# Импортируем наши модули
from database import SessionLocal, init_db, LogEntry

app = FastAPI(title="Apache Log Aggregator")

# --- СЕКЦИЯ АВТОРИЗАЦИИ ---
# Для простоты пропишем логин и пароль прямо здесь (в идеале они в БД)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


def check_auth(request: Request):
    """Проверяет, есть ли у пользователя 'пропуск' (кука)"""
    auth_cookie = request.cookies.get("session_token")
    if auth_cookie != "logged_in_token":
        return False
    return True


# --- API ЭНДПОИНТЫ ---

@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/api/login")
async def login(data: dict, response: Response):
    """Метод для входа"""
    if data.get("username") == ADMIN_USER and data.get("password") == ADMIN_PASS:
        # Ставим пользователю "печать" в браузер, что он вошел
        response.set_cookie(key="session_token", value="logged_in_token", httponly=True)
        return {"status": "ok"}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")


@app.get("/api/logs")
def get_logs(request: Request, ip: str = None, db: Session = Depends(lambda: SessionLocal())):
    # ЗАЩИТА: Если не авторизован — не даем данные
    if not check_auth(request):
        raise HTTPException(status_code=401, detail="Нужна авторизация")

    query = db.query(LogEntry)
    if ip:
        query = query.filter(LogEntry.ip.contains(ip))

    logs = query.order_by(LogEntry.timestamp.desc()).all()
    db.close()
    return logs


@app.post("/api/parse/run")
def trigger_parser(request: Request):
    if not check_auth(request):
        raise HTTPException(status_code=401, detail="Нужна авторизация")
    import parser
    parser.parse_logs()
    return {"status": "success"}


@app.delete("/api/logs/clear")
def clear_logs(db: Session = Depends(lambda: SessionLocal())):
    try:
        db.query(LogEntry).delete() # Удаляет все записи из таблицы логов
        db.commit()
        return {"status": "success", "message": "База данных очищена"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

app.mount("/", StaticFiles(directory="static", html=True), name="static")
