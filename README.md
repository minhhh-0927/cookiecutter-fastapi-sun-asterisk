# FastAPI Codebase Creator

To quickly create a project with your project name, your email..., we used [Cookiecutter](https://github.com/cookiecutter/cookiecutter) to generate project.

## Usage

First, you need to get Cookiecutter by [pip](https://pypi.org/project/pip/):

```bash
pip install "cookiecutter>=1.7.0"
```

Now run it against this repo:

```bash
$ cookiecutter https://github.com/minhhh-0927/cookiecutter-fastapi-sun-asterisk
project_name [Name of the project]: example
project_slug [example]:
project_description [A description of the project]:
author [Your name]: minhhahao
email [Your address email (you@example.com)]: minhhahao@gmail.com
version [0.1.0]:
$ cd example
$ ls
CHANGELOG.md   Makefile       __init__.py    components     config         docs           logs           migrations     production.yml pytest.ini     testing.yml    upload
LICENSE        README.md      alembic.ini    compose        develop.yml    framework      main.py        poetry.lock    pyproject.toml setup.cfg      tools          utilities
```

You need input for some values. Provide them, then a Fastapi project will be created for you.

## License

This project is licensed under the terms of the MIT license.
