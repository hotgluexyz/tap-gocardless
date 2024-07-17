# tap-gocardless

`tap-gocardless` is a Singer tap for GoCardless.


## Installation

```bash
pipx install tap-gocardless
```

## Configuration

### Accepted Config Options

```bash
{
  "access_token":"sandbox_EuTXXXXX",
  #OR
  "apikey":"sandbox_EuTXXXXX"
}
```

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-gocardless --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Usage

```bash
tap-gocardless --version
tap-gocardless --help
tap-gocardless --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_gocardless/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-gocardless` CLI interface directly using `poetry run`:

```bash
poetry run tap-gocardless --help
```
