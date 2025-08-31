# backend/app.py
import os
from flask import Flask
from api.check import bp as check_bp
from api.qna import bp as qna_bp
from web.views import bp as web_bp


def create_app() -> Flask:
    # Глобальная папка со статикой: backend/static
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    # Дев-настройки: не кэшировать статику и авто-перезагружать шаблоны
    app.config.update(
        SEND_FILE_MAX_AGE_DEFAULT=0,   # отключить кэш статики (для dev)
        TEMPLATES_AUTO_RELOAD=True
    )

    # Регистрация блюпринтов
    app.register_blueprint(web_bp)                     # страницы (templates)
    app.register_blueprint(check_bp, url_prefix="/api")
    app.register_blueprint(qna_bp,   url_prefix="/api")

    # Простой healthcheck
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
