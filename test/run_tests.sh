#!/usr/bin/env sh
FAILURES=0
rm .coverage 2>/dev/null
rm .coverage.* 2>/dev/null

for filename in ./tests/test_*; do
    echo "Running $filename"
    coverage run -p --source fenixlib --omit fenixlib/config.py ${filename}
    if [ $? -ne 0 ]; then
        FAILURES=1
    fi
done

if [ $FAILURES -ne 0 ]; then
    echo "\\nTEST(S) FAILED!!! See Above\\n"
    exit 1
fi

coverage combine
coverage report -m
rm .coverage 2>/dev/null

