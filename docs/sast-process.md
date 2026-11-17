# SAST: процес керування

1. CI (`.github/workflows/sast.yml`) автоматично запускає `semgrep`, `bandit` та `pip-audit` на кожен `push` і `Pull Request`.
2. Результати формуються у форматі SARIF (`semgrep.sarif`, `bandit.sarif`, `pip-audit.sarif`), публікуються в артефактах збірки (`sast-reports`) та завантажуються у вкладку **GitHub Security → Code scanning alerts**.
3. Правила тріажу: для знахідок рівня `High/Critical` створюється задача у **GitHub Issues** з міткою `security` (SLA на виправлення — до 24 годин; для `Medium` — до 7 днів).
4. Пріоритезація виконується за оцінкою CVSS, складністю експлуатації та критичністю ураженого модуля.
5. Виправлення фіксується окремим комітом/PR із прив'язкою до номера Issue (`fixes #ID`) та перевіряється повторним запуском SAST.
