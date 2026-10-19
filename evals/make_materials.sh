#!/usr/bin/env bash
# Build the blind-test materials folders (images are generated, not committed).
#   evals/software/materials  ← templates/assets (wireframe placeholder screens) + README
#   evals/service/materials   ← drawn placeholder photos (make_service_materials.mjs) + README
# The physical-product folder is examples/product-demo/materials (copy it elsewhere before a blind run,
# so the run cannot read the reference treatment next to it).
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"; A="$HERE/../templates/assets"; M="$HERE/software/materials"
cp "$A/ui-sample.png" "$M/workspace.png"; cp "$A/plot-1.png" "$M/survival-curve.png"; cp "$A/plot-2.png" "$M/roc-curve.png"
cp "$A/plot-3.png" "$M/forest-plot.png"; cp "$A/phone.png" "$M/phone-results.png"; cp "$A/clip.webm" "$M/scroll-results.webm"; cp "$A/logo.png" "$M/logo.png"
node "$HERE/make_service_materials.mjs"
echo "materials ready: $M, $HERE/service/materials"
