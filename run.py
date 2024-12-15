import sys
from pathlib import Path

# Add src to Python path to allow direct execution
src_path = str(Path(__file__).parent / "src")
sys.path.insert(0, src_path)

from insightvault.app.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
