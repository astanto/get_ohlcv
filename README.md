# Multi-Timeframe Python Script Runner

A small Python launcher that runs three scripts sequentially:

1. `1h.py`
2. `15m.py`
3. `5m.py`

The launcher prints a status message before starting each script and invokes each one using Python.

It used basically to get olhcv data from trading platform open API

## Project Structure

Keep `main.py` and the scripts it runs in the same directory:

```text
your-project/
├── main.py
├── 1h.py
├── 15m.py
└── 5m.py
```

Add any additional files or folders required by the individual scripts.

## Requirements

- Python installed on your computer and available as the `python` command.
- The three scripts (`1h.py`, `15m.py`, and `5m.py`) present in the same working directory as `main.py`.
- Any dependencies required by those scripts installed separately.

## How to Run

Open a terminal in the project directory and run:

```bash
python main.py
```

The launcher runs the scripts in this order:

```text
1h.py → 15m.py → 5m.py
```

## Notes

- The scripts are run sequentially, not in parallel.
- The launcher does not currently stop if one of the child scripts exits with an error; each subprocess result is not checked.
- The launcher uses the `python` command, so make sure it points to the Python interpreter you intend to use.

## License

No license is specified. Add a license file if you want to define how others may use, modify, or distribute this project.
