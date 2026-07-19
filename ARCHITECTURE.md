# Ustuvon Test Platformasi — Backend Architecture

Owner: Abdulaziz Komiljonov (Backend Team Lead / System Architect)
Stack: Django + DRF, PostgreSQL, Redis, Celery, Docker

## 1. Principles

- **Dependency direction is one-way**: presentation → application → domain/data. A layer only calls the layer directly below it, never sideways or up. Views never touch the ORM directly; services never import DRF.
- **Every domain concept is its own Django app** (`subjects`, `tests`, `results`, `certificates`, ...). No god-app.
- **Every app follows the same internal shape** (see §3), so any developer can open any app and know exactly where to look.
- **Business logic lives in services, not in views or models.** Views orchestrate HTTP; models describe data; services decide what happens.
- **Base classes are inherited, not copy-pasted.** `core/` defines the shared building blocks once.

## 2. Top-level folder structure

```
ustuvon-backend/
├── config/                      👤 Abdulaziz
│   ├── settings/
│   │   ├── base.py              👤 Abdulaziz
│   │   ├── local.py             👤 Abdulaziz
│   │   ├── staging.py           👤 Abdulaziz
│   │   └── production.py        👤 Abdulaziz
│   ├── urls.py                  👤 Abdulaziz
│   ├── celery.py                👤 Abdulaziz  (Davronbek N. can propose changes)
│   ├── asgi.py                  👤 Abdulaziz
│   └── wsgi.py                  👤 Abdulaziz
│
├── core/                        👤 Abdulaziz  — foundation, everyone reads, only Abdulaziz merges
│   ├── models.py                👤 Abdulaziz
│   ├── serializers.py           👤 Abdulaziz
│   ├── viewsets.py              👤 Abdulaziz
│   ├── permissions.py           👤 Abdulaziz
│   ├── exceptions.py            👤 Abdulaziz
│   ├── middleware.py            👤 Abdulaziz
│   └── pagination.py            👤 Abdulaziz
│
├── common/                      👥 Shared — anyone can add a utility, no single owner
│   ├── utils.py
│   ├── validators.py
│   ├── constants.py
│   └── enums.py
│
├── apps/
│   ├── users/                   👤 Abdulaziz          — auth, roles, security
│   ├── subjects/                👤 Javohir             — subjects taxonomy
│   ├── exams/                   👤 Javohir             — tests, questions, answers
│   ├── results/                 👤 Sirojiddin          — user_tests, user_answers, results
│   ├── statistics/              👤 Sirojiddin          — aggregated stats, leaderboard
│   ├── certificates/            👤 Davronbek Nazarov   — PDF + QR + validation
│   ├── notifications/           👤 Davronbek Nazarov   — SMS, email, Telegram
│   ├── payments/                👤 Sirojiddin          — to'lovlar (admin side)
│   ├── ai_parser/                👥 Abdulaziz + Davronbek Nazarov  — AI test import
│   └── admin_panel/              👥 Javohir (content) + Sirojiddin (users/payments)
│
├── infra/
│   ├── docker/                  👤 Abdulaziz
│   └── nginx/                   👤 Abdulaziz
│
├── requirements/                👤 Abdulaziz  — but everyone must add their own new packages here via PR
│   ├── base.txt
│   ├── local.txt
│   ├── staging.txt
│   └── production.txt
│
├── tests/                       👥 Shared — project-wide integration/e2e tests, anyone can add
├── .env.example                 👤 Abdulaziz
├── manage.py                    👤 Abdulaziz
└── pytest.ini                   👤 Abdulaziz
```

## 3. Standard shape of every app (`apps/<name>/`)

Every domain app repeats this same internal structure — this consistency is the point:

```
apps/results/
├── models.py            # ORM models only: fields, constraints, no logic
├── serializers.py        # inherits core.serializers.BaseSerializer
├── services.py            # business logic: calculate_score(), enforce_single_device()
├── selectors.py            # read-only query helpers (keeps ORM queries out of views/services)
├── views.py              # inherits core.viewsets.BaseViewSet, calls services/selectors only
├── urls.py
├── permissions.py         # app-specific permission classes, if needed
├── tasks.py               # Celery tasks owned by this app
├── admin.py               # Django admin registration
├── apps.py
├── migrations/
└── tests/
    ├── test_models.py
    ├── test_services.py
    └── test_api.py
```

**Rule of thumb for where code goes:**

| Question you're asking | File |
|---|---|
| What does the data look like? | `models.py` |
| How do I read/filter this data? | `selectors.py` |
| What happens when X occurs? (scoring, sending SMS, generating a certificate) | `services.py` |
| How does the HTTP request map to a response? | `views.py` + `serializers.py` |
| What runs in the background / on a schedule? | `tasks.py` |

## 4. Request flow (example: submitting a test)

1. `POST /api/results/submit/` hits `results/views.py`
2. View validates input via `results/serializers.py`, then calls `results/services.py::submit_test()`
3. Service runs the scoring logic, calls `results/selectors.py` for any lookups, saves via the model
4. Service may enqueue a Celery task (`results/tasks.py`) — e.g. update leaderboard, trigger certificate generation
5. View returns the serialized result

## 5. Infrastructure (`infra/docker/docker-compose.yml` services)

- `web` — Django/Gunicorn
- `db` — PostgreSQL
- `redis` — cache + Celery broker
- `worker` — Celery worker
- `beat` — Celery beat (scheduled jobs: daily stats, cleanup)
- `nginx` — reverse proxy (production only)

## 6. Naming conventions

- Apps: lowercase, plural nouns (`subjects`, `results`, not `Subject`, `resultApp`)
- Services: verb-first function names — `submit_test()`, `send_verification_sms()`, `generate_certificate()`
- Selectors: `get_` / `list_` prefix — `get_user_results()`, `list_active_subjects()`
- Serializers: `<Model>Serializer`, `<Model>CreateSerializer` when input/output shapes differ
- Celery tasks: `<verb>_<noun>_task` — `send_notification_task`, `calculate_daily_stats_task`

## 7. Ownership map (current sprint)

| App | Owner |
|---|---|
| `users` | Abdulaziz |
| `core`, `infra/docker`, `config` | Abdulaziz |
| `ai_parser` | Abdulaziz + Davronbek Nazarov |
| `notifications`, `payments-jobs`, `certificates` | Davronbek Nazarov |
| `subjects`, `exams`, `admin_panel` (content side) | Javohir |
| `results`, `statistics`, `admin_panel` (users/payments side) | Sirojiddin |
