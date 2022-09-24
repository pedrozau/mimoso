# Api para sistema de geladari 

* /app/docs documentação para o api 

* token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBlZHJvIiwiZXhwIjozNDY0MDE2NjMwfQ.dNN-PsrBwu6J7hRB_zqKjlkDAoStk2aiwq-Tqw2bVpE


* Estrutura do projecto 

.
├── Procfile
├── README.md
├── requirements.txt
├── settings.toml
└── vite
    ├── app.py
    ├── blueprint
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-310.pyc
    │   │   ├── __init__.cpython-39.pyc
    │   │   └── view.cpython-39.pyc
    │   ├── restapi
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── action.cpython-39.pyc
    │   │   │   ├── __init__.cpython-310.pyc
    │   │   │   ├── __init__.cpython-39.pyc
    │   │   │   ├── resources.cpython-310.pyc
    │   │   │   ├── resources.cpython-39.pyc
    │   │   │   ├── token.cpython-310.pyc
    │   │   │   └── token.cpython-39.pyc
    │   │   ├── #resources.py#
    │   │   ├── resources.py
    │   │   └── token.py
    │   └── webui
    │       ├── __init__.py
    │       ├── __pycache__
    │       │   ├── __init__.cpython-310.pyc
    │       │   ├── __init__.cpython-39.pyc
    │       │   ├── view.cpython-310.pyc
    │       │   └── view.cpython-39.pyc
    │       ├── templates
    │       │   ├── 400.html
    │       │   ├── 404.html
    │       │   ├── 500.html
    │       │   └── index.html
    │       └── view.py
    ├── extension
    │   ├── command.py
    │   ├── configuration.py
    │   ├── database.py
    │   ├── docs.py
    │   ├── __init__.py
    │   ├── look.py
    │   └── __pycache__
    │       ├── command.cpython-310.pyc
    │       ├── command.cpython-39.pyc
    │       ├── configuration.cpython-310.pyc
    │       ├── configuration.cpython-39.pyc
    │       ├── database.cpython-310.pyc
    │       ├── database.cpython-39.pyc
    │       ├── docs.cpython-310.pyc
    │       ├── docs.cpython-39.pyc
    │       ├── generate.cpython-39.pyc
    │       ├── __init__.cpython-310.pyc
    │       └── __init__.cpython-39.pyc
    ├── __init__.py
    ├── model.py
    ├── __pycache__
    │   ├── app.cpython-310.pyc
    │   ├── __init__.cpython-310.pyc
    │   └── model.cpython-310.pyc
    └── static
        ├── image
        │   └── user.png
        └── swagger.json
