import os
import sys
import cadquery as cq

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from saltscale_base import bottom_segment, top_segment, assembly_preview

BASE = os.path.dirname(__file__)
STL = os.path.join(BASE, "exports", "stl")
STEP = os.path.join(BASE, "exports", "step")
os.makedirs(STL, exist_ok=True)
os.makedirs(STEP, exist_ok=True)

for q in range(4):
    cq.exporters.export(bottom_segment(q), os.path.join(STL, f"bottom_segment_{q}.stl"))
    cq.exporters.export(top_segment(q), os.path.join(STL, f"top_segment_{q}.stl"))
    cq.exporters.export(bottom_segment(q), os.path.join(STEP, f"bottom_segment_{q}.step"))
    cq.exporters.export(top_segment(q), os.path.join(STEP, f"top_segment_{q}.step"))

assembly_preview().save(os.path.join(STEP, "saltscale_v1_assembly.step"))
print("Exported SaltScale CAD files to exports/stl and exports/step")
