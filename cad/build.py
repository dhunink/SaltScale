import os
import sys
import cadquery as cq

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from saltscale_base import bottom_segment, top_segment, assembly_preview
from platform_v1 import platform_compound
from platform_v2 import platform_v2_full
from platform_v3 import platform_v3_full
from sensor_module_v1 import sensor_module
from sensor_module_v2 import sensor_module_v2
from sensor_module_v3 import sensor_module_v3

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
# Export the assembled platform_v1 model (combined segments)
platform_full = platform_compound()
cq.exporters.export(platform_full, os.path.join(STL, "platform_v1.stl"))
cq.exporters.export(platform_full, os.path.join(STEP, "platform_v1.step"))

# Export platform v2 (structural version)
platform2 = platform_v2_full()
cq.exporters.export(platform2, os.path.join(STL, "platform_v2.stl"))
cq.exporters.export(platform2, os.path.join(STEP, "platform_v2.step"))
# Export platform v3 (four-sensor architecture)
platform3 = platform_v3_full()
cq.exporters.export(platform3, os.path.join(STL, "platform_v3.stl"))
cq.exporters.export(platform3, os.path.join(STEP, "platform_v3.step"))

# Attempt PNG renders of platform_v3
try:
    cq.exporters.export(platform3, os.path.join(STEP, "platform_v3_iso.png"))
    cq.exporters.export(platform3, os.path.join(STEP, "platform_v3_top.png"))
    bottom = platform3.rotate((0, 0, 0), (1, 0, 0), 180)
    cq.exporters.export(bottom, os.path.join(STEP, "platform_v3_bottom.png"))
except Exception:
    print("PNG render skipped (exporter may not support PNG in this environment)")

# Export sensor module test jig
sensor_base, sensor_upper = sensor_module()
cq.exporters.export(sensor_base, os.path.join(STL, "sensor_module_v1.stl"))
cq.exporters.export(sensor_base, os.path.join(STEP, "sensor_module_v1.step"))

# Export sensor module v2 parts
base2, lower2, upper2, sensor_ph, assembly2 = sensor_module_v2()
cq.exporters.export(base2, os.path.join(STL, "sensor_module_base.stl"))
cq.exporters.export(lower2, os.path.join(STL, "sensor_module_lower_pad.stl"))
cq.exporters.export(upper2, os.path.join(STL, "sensor_module_upper_pad.stl"))
cq.exporters.export(sensor_ph, os.path.join(STL, "sensor_module_sensor_placeholder.stl"))

# Assembly export (STEP for multi-body)
cq.exporters.export(assembly2, os.path.join(STEP, "sensor_module_v2_assembly.step"))

print("Exported sensor_module_v2 parts to exports/stl and assembly to exports/step")

# Export sensor module v3 parts
base3, lower3, sensor_ph3, upper3, assembly3 = sensor_module_v3()
cq.exporters.export(base3, os.path.join(STL, "sensor_module_v3_base.stl"))
cq.exporters.export(lower3, os.path.join(STL, "sensor_module_v3_lower_pad.stl"))
cq.exporters.export(upper3, os.path.join(STL, "sensor_module_v3_upper_pad.stl"))
cq.exporters.export(sensor_ph3, os.path.join(STL, "sensor_module_v3_sensor_placeholder.stl"))
cq.exporters.export(assembly3, os.path.join(STEP, "sensor_module_v3_assembly.step"))

print("Exported sensor_module_v3 parts to exports/stl and assembly to exports/step")

print("Exported sensor_module_v1 to exports/stl and exports/step")
print("Exported SaltScale CAD files to exports/stl and exports/step")
