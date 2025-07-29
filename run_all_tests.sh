#!/bin/bash
# run_all_tests.sh
# ----------------
# This script runs all tests in the tests directory and summarizes the results.

echo "Running all tests for CuckooPC-Simulation..."
echo "-------------------------------------------"

# Run all Python test files in the tests directory
for test_file in tests/test_*.py
do
    echo "Executing $test_file ..."
    python3 "$test_file"
    echo "-------------------------------------------"
done

echo "All tests completed."
