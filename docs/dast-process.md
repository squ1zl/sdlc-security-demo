# DAST: процес тестування

1. Застосунок протестовано динамічним сканером **OWASP ZAP Baseline** у CI-воркфлоу `.github/workflows/dast.yml` (`zaproxy/action-baseline@v0.13.0`) на `http://127.0.0.1:5000`.
2. HTML-звіт (`report_html.html`) завантажено з артефакту `zap-report` та проаналізовано.
3. Підсумки первинного сканування (знайдені проблеми та рівень критичності):
   - **High:** *Cross Site Scripting (Reflected)* у `/echo?msg=...` — повернення неекранованого вводу у HTML.
   - **Medium:** *Content Security Policy (CSP) Header Not Set* та *Missing Anti-clickjacking Header* (`X-Frame-Options`) на всіх сторінках.
   - **Low:** *Cookie No HttpOnly Flag*, *Cookie Without SameSite Attribute* для сесійної cookie та *X-Content-Type-Options Header Missing*.
4. План виправлень: екранувати вивід у `/echo` (`markupsafe.escape`), параметризувати SQL у `/search`, додати захисні HTTP-заголовки та прапорці `HttpOnly`/`SameSite` для сесій.
