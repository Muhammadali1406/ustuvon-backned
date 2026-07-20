ustuvon-backend/
├── config/
│   ├── __init__.py                  (empty file, create manually)
│   ├── urls.py                      ✅ from chat
│   ├── wsgi.py                      ✅ from chat
│   ├── asgi.py                      ✅ from chat
│   └── settings/
│       ├── __init__.py              (empty file, create manually)
│       ├── base.py                  ✅ from chat (patched with AUTHENTICATION_BACKENDS + validator)
│       ├── local.py                 ✅ from chat
│       ├── staging.py               ✅ from chat
│       └── production.py            ✅ from chat
│
├── core/
│   ├── __init__.py                  (empty file, create manually)
│   ├── models.py                    ✅ from chat (BaseModel — Davron's merged version)
│   ├── serializers.py               ✅ from chat (BaseModelSerializer)
│   ├── viewsets.py                  ✅ from chat (BaseViewSet)
│   ├── permissions.py               ✅ from chat (IsOwner, IsAdmin, IsVerified, ReadOnlyOrIsAdmin)
│   └── exceptions.py                ✅ from chat (ServiceError family + custom_exception_handler)
│
├── apps/
│   ├── __init__.py                  ✅ from chat (empty, but needed so `apps` is a package)
│   └── users/
│       ├── __init__.py              ✅ from chat (empty)
│       ├── apps.py                  ✅ from chat
│       ├── models.py                ✅ from chat
│       ├── backends.py              ✅ from chat
│       ├── validators.py            ✅ from chat
│       ├── selectors.py             ✅ from chat
│       ├── services.py              ✅ from chat
│       ├── tasks.py                 ✅ from chat
│       ├── serializers.py           ✅ from chat
│       ├── views.py                 ✅ from chat
│       ├── urls.py                  ✅ from chat
│       ├── admin.py                 ✅ from chat
│       ├── migrations/              (empty folder — run `makemigrations` to generate)
│       │   └── __init__.py
│       └── tests/
│           ├── __init__.py          ✅ from chat (empty)
│           └── test_models.py       ✅ from chat
│
└── requirements/
    ├── base.txt                     ✅ from chat
    ├── local.txt                    ✅ from chat
    ├── staging.txt                  ✅ from chat
    └── production.txt               ✅ from chat