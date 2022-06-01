# Installation within docker

## Prerequisites

- **[Required]** Docker version `^20.10.14`.
- **[Optional]** Docker Compose version `^v2.5.1`.

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

Finally, you can build the stack by command:

```bash
docker-compose -f develop.yml build
```

If you want to emulate for **production environment**, please use the `production.yml` instead.
