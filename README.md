# OBJECT VALIDATION AND CONVERSION WITH MARSHMALLOW

[![CircleCI](https://github.com/CIRCLECI-GWP/object-validation-and-conversion-marshmallow.svg?style=svg)](https://github.com/CIRCLECI-GWP/object-validation-and-conversion-marshmallow)

<p align="center"><img src="https://avatars3.githubusercontent.com/u/59034516"></p>

![python badge](https://img.shields.io/badge/Python-3.8-green) ![Flask badge](https://img.shields.io/badge/Flask%20-2.0.1-gray) ![MarshMallow badge](https://img.shields.io/badge/MarshMallow%20-13.3-blue) ![Pytest badge](https://img.shields.io/badge/pytest-6.2.5-red)

The goal of this project is to illustrate object validation in marshmallow.
It uses SQLAlchemy to manage models, SQLite for data storage, Marshmallow for
data serialization,deserialization, and validation and tests created with
pytest.

## Installation

---

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

---

```shell
FLASK_APP=src/app.py flask run
```

## Running tests

---

```shell
python -m pytest -s
```

## Details

This repo is built following a tutorial published on CircleCI blog under the CircleCI Guest Writer Program.

- Blog post: [Object Validation and Conversion with Marshmallow][blog]
- Author's GitHub profile: [Waweru Mwaura][author]

### About CircleCI Guest Writer Program

Join a team of freelance writers and write about your favorite technology topics for the CircleCI blog. Read more about the program [here][gwp-program].

Reviewers: [Ron Powell][ron], [Stanley Ndagi][stan]

[blog]: https://circleci.com/blog/object-validation-and-conversion-with-marshmallow/
[author]: https://github.com/mwaz
[gwp-program]: https://circle.ci/3ahQxfu
[ron]: https://github.com/ronpowelljr
[stan]: https://github.com/NdagiStanley
