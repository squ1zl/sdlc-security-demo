# Модель загроз (STRIDE)

## Контекст
Публічний Flask вебдодаток, SQLite, мінімальна аутентифікація.

## STRIDE-матриця (коротко)
- **S**poofing: підробка облікових даних, сесійні cookie без флагів.
- **T**ampering: SQLi для модифікації даних.
- **R**epudiation: недостатній аудит логінів.
- **I**nformation Disclosure: XSS для крадіжки cookie; витік конфігів.
- **D**enial of Service: зловмисні запити до /search.
- **E**levation of Privilege: слабкі ролі/перевірки доступу.

## 3 сценарії атак
1) **SQL Injection у /search**  
   - Вектор: параметр `q` прямо в SQL.  
   - Виявлення: SAST (Semgrep/Bandit B608), DAST (ZAP SQLi), мануальні тести.  
   - Пом'якшення: параметризовані запити.

2) **Reflected XSS у /echo**  
   - Вектор: параметр `msg` повертається як HTML без екранування.  
   - Виявлення: ZAP, браузерні індикатори.  
   - Пом'якшення: escaping, CSP, валідатори.

3) **Слабка автентифікація /login**  
   - Вектор: паролі в БД у відкритому вигляді, відсутнє rate limiting.  
   - Виявлення: SAST, пентест-чекліст; лог-аналіз.  
   - Пом'якшення: хешування (PBKDF2/Argon2), lockout, 2FA (опційно).

## Виявлені ризики/знахідки
- [x] R1 SQLi (`src/app.py:32`): виявлено Bandit `[B608:hardcoded_sql_expressions]` (CWE-89) — конкатенація параметра `q` у SQL-запиті.
- [x] R2 XSS (`src/app.py:21`): повернення неекранованого параметра `msg` у відповіді `/echo`.
- [x] R3 Weak auth (`src/db.py:12`, `src/app.py:41`): паролі у відкритому вигляді (`plaintext`), відсутність прапорців безпеки сесійних cookie.
- [x] R4 Misconfiguration (`src/app.py:6, 63`): виявлено Bandit `[B201:flask_debug_true]` (CWE-94) та `[B104:hardcoded_bind_all_interfaces]` (CWE-605).
