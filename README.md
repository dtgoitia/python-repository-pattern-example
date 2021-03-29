## Usage

Steps to set up the project for regular usage:

```shell
python3 -m venv .venv                     # create Python environment
. .venv/bin/activate                      # activate Python environment
export DATABASE_URI="sqlite:///my_db.db"  # set environment variables

make install                              # install dependencies

alembic upgrade head                      # apply DB migrations
```

## Development

Steps to set up the project to develop it:

```shell
python3 -m venv .venv                     # create Python environment
. .venv/bin/activate                      # activate Python environment
export DATABASE_URI="sqlite:///my_db.db"  # set environment variables
export DEBUG="true"

make dev-install                          # install development dependencies

alembic upgrade head                      # apply DB migrations
```
