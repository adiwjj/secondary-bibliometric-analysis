"""Run the full pipeline: Layers A to D, then figures."""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ["layer_a_network.py", "layer_b_subcorpus.py", "layer_c_concepts.py",
               "layer_d_temporal.py", "make_figures.py"]:
    print(f"\n=== {script} ===")
    runpy.run_path(str(HERE / script), run_name="__main__")
print("\nDone. Tables in outputs/tables, figures in outputs/figures.")
