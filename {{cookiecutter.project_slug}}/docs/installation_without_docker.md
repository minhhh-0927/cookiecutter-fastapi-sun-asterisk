# Installation without docker

## Prerequisites

- **[Required]** Python version `^3.9.6`. Tested with Python version `3.10.4`.
- **[Required]** Suggestion the OS is `MacOS` or `Linux`. If you use `Windows`, you may get error related to `encryption`.
- **[Required]** Pip version `20.0.4`.
- **[Optional]** You should use tools like `virtualenv`, `pyenv`, `pipenv` to create a Python virtual environment.
- **[Optional]** I tested with PostgreSQL `^13.5`. But, you can use other database engine like SQL. 

### Installation

First, you should create file `env`. In `develop.yml` file, i was setup `docker-compose` using filename `.env`.

```bash
cp .env.example .env
```

Alternatives, you can use export command like:

```bash
export ENV=development
export SECRET_KEY=hex key....
```

Next step, if you want to use file `env`, you need update value for key in this file.

After done, you can start install Python dependencies:

```bash
pip install poetry
poetry install
```

If you want to emulate for **production environment**, please use the command in below instead.

```bash
pip install poetry
poetry install --no-dev
```
