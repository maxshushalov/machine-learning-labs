"""Run both notebooks with fresh kernels; save outputs only after successful execution."""
from pathlib import Path
from time import monotonic
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    for relative in (
        "regression/notebooks/regression.ipynb",
        "classification/classification.ipynb",
    ):
        path = ROOT / relative
        notebook = nbformat.read(path, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        start = monotonic()
        print(f"START {relative}", flush=True)
        NotebookClient(
            notebook, timeout=1800, kernel_name="python3", allow_errors=False,
            resources={"metadata": {"path": str(path.parent)}},
        ).execute()
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
        print(f"OK {relative} ({monotonic() - start:.1f} s)", flush=True)


if __name__ == "__main__":
    main()
