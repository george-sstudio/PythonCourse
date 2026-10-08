#!/usr/bin/env bash
# Course maintenance: run every solution (and setup) headless on a QGIS Python.
# Usage: tools/run_all_tests.sh /path/to/python-with-qgis
PY=${1:-python}
cd "$(dirname "$0")/.."
pass=0; fail=0
for f in modules/00-setup/setup_course.py modules/*/solutions/*.py; do
  out=$("$PY" tools/qgis_runner.py "$f" 2>&1)
  if [ $? -eq 0 ] && ! grep -q "Traceback" <<<"$out"; then
    pass=$((pass+1)); echo "PASS $f"
  else
    fail=$((fail+1)); echo "FAIL $f"; grep -v "PDAL Error\|QStandardPaths" <<<"$out" | tail -15
  fi
done
# The capstone's acceptance checks, run on the reference factory's output
out=$("$PY" tools/qgis_runner.py modules/12-capstone/acceptance_checks.py 2>&1)
if [ $? -eq 0 ] && ! grep -q "Traceback" <<<"$out"; then
  pass=$((pass+1)); echo "PASS acceptance_checks"
else
  fail=$((fail+1)); echo "FAIL acceptance_checks"; tail -15 <<<"$out"
fi
# Every code block of the cheat sheet
out=$("$PY" tools/qgis_runner.py tools/test_cheatsheet.py 2>&1)
if [ $? -eq 0 ] && grep -q "blocks ran OK" <<<"$out"; then
  pass=$((pass+1)); echo "PASS cheatsheet"
else
  fail=$((fail+1)); echo "FAIL cheatsheet"; tail -15 <<<"$out"
fi
# Exercises must at least be valid Python (except the deliberate SyntaxError one)
for f in modules/*/exercises/*.py; do
  case "$f" in *ex02_4_fix_errors.py) continue;; esac
  "$PY" -m py_compile "$f" 2>/dev/null || { echo "SYNTAX $f"; fail=$((fail+1)); }
done
echo "passed: $pass  failed: $fail"
[ $fail -eq 0 ]
