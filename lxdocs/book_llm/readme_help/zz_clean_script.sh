#!/usr/bin/env bash
# Usage: ./build_latex.sh [basename]
# Default basename is "main" when not provided.

# latexmk -C           # clean previous builds

set -euo pipefail

basename="${1:-main}"
basename="${basename%.tex}"

#1) Clean latexmk artifacts
latexmk -C

#2) Remove specific auxiliary files using a one-line list + loop
exts=(aux bbl bcf blg fdb_latexmk fls lof log lot out run.xml toc); 
for ext in "${exts[@]}"; do
  rm -f "${basename}.${ext}"
done

