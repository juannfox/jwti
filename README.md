# jwti

*JWT Inspector* is a handy CLI tool for inspecting JWT tokens 🔑.

## Usage

![Example usage](img/usage.png)

Read from STDIN:

```bash
echo "<JWT>" | python3 -m jwti inspect -
```

Input argument:

```bash
python3 -m jwti inspect <JWT>
```

Get help:

```bash
python3 -m jwti ---help
```

## Local development

### Environment setup

First, install [uv](https://docs.astral.sh/uv/guides/install-python/).

Then prepare the local development environment (virtual environment and dependencies):

```bash
uv venv
source .venv/bin/activate
uv sync
```

### Building

#### Python package

Run:

```bash
uv build
ls dist
```

#### Standalone executable file

Run:

```bash
pyinstaller -Fyn jwti --clean jwti/__main__.py
ls dist
```
