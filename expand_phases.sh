#!/bin/bash
# Expand phase documentation to 50+ pages

echo "📚 Expanding phase documentation..."

# Generate detailed content for each phase
for phase in spark forge ignition drift orbit flare ascension; do
    echo "Expanding $phase documentation..."
    python3 -c "
from expansion_generator import expand_phase
expand_phase('$phase')
"
done

echo "✅ Phase expansion complete!"
