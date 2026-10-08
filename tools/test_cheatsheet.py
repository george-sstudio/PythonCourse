"""Course maintenance: run every python block of CHEATSHEET.md, top to bottom (via qgis_runner.py)."""
import re
from pathlib import Path

from qgis.core import QgsExpressionContextUtils

course = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
text = (course / "CHEATSHEET.md").read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", text, flags=re.S)
(course / "output").mkdir(exist_ok=True)
exec(compile("\n".join(blocks), "CHEATSHEET.md", "exec"), {"__name__": "__cheatsheet__"})
print(f"CHEATSHEET.md: {len(blocks)} blocks ran OK")
