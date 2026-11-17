# Підсумковий аудит безпеки

## Виконання початкових вимог
- **AUTH-1:** Виконано — маршрут `/profile` перевіряє наявність `user_id` у сесії.
- **AUTH-2:** Заплановано у беклог — інтеграція `Flask-Limiter` для захисту `/login` від брутфорсу.
- **STOR-1:** Виконано — паролі зберігаються у вигляді хешів `PBKDF2-SHA256` (`werkzeug.security`).
- **LOG-1:** Виконано — налаштовано аудит подій успішного та невдалого входу (`logging`).
- **CONF-1:** Виконано — видалено захардкоджений `SECRET_KEY` та вимкнено `debug=True`.

## Перегляд змін у коді
- Комміти з виправленнями уразливостей: `fix(security): remediate SQLi, XSS, password hashing and security headers`.

## Закриті вразливості
- **R1 SQLi:** closed in Issue #1 (параметризовані запити у `/search`).
- **R2 XSS:** closed in Issue #2 (HTML-екранування через `markupsafe.escape()` у `/echo`).
- **R3/R4 Weak auth & Misconfig:** closed in Issue #3 (хешування паролів, `HttpOnly`/`SameSite` cookie, HTTP-заголовки `CSP`, `X-Frame-Options`, `X-Content-Type-Options`).

## Ролі та відповідальність
- **Owner:** Визначає бізнес-пріоритети задач безпеки та затверджує прийнятний рівень ризиків.
- **Security Champion:** Формує вимоги безпеки (ASVS) та STRIDE-модель, налаштовує SAST/DAST, проводить тріаж.
- **Dev:** Пише безпечний код, усуває вразливості за звітами сканерів у межах SLA.
- **QA:** Розробляє негативні тест-кейси (SQLi/XSS/Auth) та перевіряє виправлення.
- **DevOps:** Підтримує CI/CD пайплайни GitHub Actions, керує секретами та безпекою контейнерів.

## Рекомендації
- Додати rate limiting (`Flask-Limiter`) на `/login`, сканування Docker-образу через **Trivy**, pre-commit перевірку секретів (`gitleaks`) та перенесення секретів у **HashiCorp Vault**.
