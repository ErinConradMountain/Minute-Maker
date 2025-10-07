#!/usr/bin/env python3
"""
Test runner script for Minute Maker application.
Provides different test execution modes and reporting.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type="all", coverage=False, verbose=False, marker=None):
    """
    Run tests with specified options.
    
    Args:
        test_type: Type of tests to run (all, unit, integration, slow)
        coverage: Whether to generate coverage report
        verbose: Verbose output
        marker: Pytest marker to filter tests
    """
    cmd = ["python", "-m", "pytest"]
    
    # Add test path based on type
    if test_type == "unit":
        cmd.extend(["tests/", "-k", "not integration and not slow"])
    elif test_type == "integration":
        cmd.extend(["tests/test_integration.py"])
    elif test_type == "slow":
        cmd.extend(["-m", "slow"])
    else:  # all
        cmd.append("tests/")
    
    # Add coverage options
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Add custom marker
    if marker:
        cmd.extend(["-m", marker])
    
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd)


def check_dependencies():
    """Check if required test dependencies are installed."""
    try:
        import pytest
        print("✓ pytest available")
    except ImportError:
        print("✗ pytest not installed. Run: pip install pytest")
        return False
    
    try:
        import pytest_cov
        print("✓ pytest-cov available")
    except ImportError:
        print("✗ pytest-cov not installed. Run: pip install pytest-cov")
        return False
    
    return True


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run Minute Maker tests")
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "slow"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--marker",
        help="Run tests with specific pytest marker"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check test dependencies"
    )
    
    args = parser.parse_args()
    
    if args.check_deps:
        if check_dependencies():
            print("All test dependencies available!")
            sys.exit(0)
        else:
            print("Missing test dependencies!")
            sys.exit(1)
    
    if not check_dependencies():
        print("Install missing dependencies before running tests")
        sys.exit(1)
    
    exit_code = run_tests(
        test_type=args.type,
        coverage=args.coverage,
        verbose=args.verbose,
        marker=args.marker
    )
    
    if exit_code == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code {exit_code}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()