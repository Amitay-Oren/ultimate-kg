#!/usr/bin/env python3
"""
Test runner for Agentic GraphRAG System

This script provides convenient commands for running different types of tests
and validation procedures for the Agentic GraphRAG system.
"""

import sys
import subprocess
import argparse
import asyncio
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
    else:
        print(f"❌ {description} - FAILED (exit code: {result.returncode})")
    
    return result.returncode == 0

def run_unit_tests():
    """Run unit tests for individual components"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/test_a2a_server.py",
        "tests/test_kg_agent.py",
        "-m", "not integration and not slow",
        "--tb=short"
    ]
    return run_command(cmd, "Unit Tests")

def run_integration_tests():
    """Run integration tests"""
    cmd = [
        "python", "-m", "pytest",
        "tests/test_integration.py",
        "-m", "integration",
        "--tb=short"
    ]
    return run_command(cmd, "Integration Tests")

def run_all_tests():
    """Run all tests"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-m", "not slow and not real",
        "--tb=short"
    ]
    return run_command(cmd, "All Tests (excluding slow/real)")

def run_performance_tests():
    """Run performance tests"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-m", "performance",
        "--tb=short"
    ]
    return run_command(cmd, "Performance Tests")

def run_real_integration_tests():
    """Run tests that require real services"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-m", "real",
        "--tb=short"
    ]
    return run_command(cmd, "Real Integration Tests")

def run_code_quality_checks():
    """Run code quality checks"""
    results = []
    
    # Black formatting check
    cmd = ["python", "-m", "black", "--check", "--diff", "."]
    results.append(run_command(cmd, "Code Formatting Check (Black)"))
    
    # Ruff linting
    cmd = ["python", "-m", "ruff", "check", "."]
    results.append(run_command(cmd, "Code Linting (Ruff)"))
    
    # MyPy type checking
    cmd = ["python", "-m", "mypy", "agentic_graphrag/"]
    results.append(run_command(cmd, "Type Checking (MyPy)"))
    
    return all(results)

def run_system_validation():
    """Run system validation checks"""
    results = []
    
    # Configuration validation
    cmd = ["python", "main.py", "--config-check"]
    results.append(run_command(cmd, "Configuration Validation"))
    
    # System tests
    cmd = ["python", "main.py", "--test-only"]
    results.append(run_command(cmd, "System Self-Tests"))
    
    return all(results)

def run_a2a_validation():
    """Run A2A protocol validation"""
    cmd = [
        "python", "-m", "agentic_graphrag.server.a2a_utils",
        "--server-url", "http://localhost:8080"
    ]
    return run_command(cmd, "A2A Protocol Validation")

def run_coverage_report():
    """Generate coverage report"""
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "--cov=agentic_graphrag",
        "--cov-report=html:htmlcov",
        "--cov-report=term",
        "-m", "not slow and not real"
    ]
    success = run_command(cmd, "Test Coverage Report")
    
    if success:
        print("\n📊 Coverage report generated in htmlcov/index.html")
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Test runner for Agentic GraphRAG System")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--real", action="store_true", help="Run tests requiring real services")
    parser.add_argument("--quality", action="store_true", help="Run code quality checks")
    parser.add_argument("--system", action="store_true", help="Run system validation")
    parser.add_argument("--a2a", action="store_true", help="Run A2A protocol validation")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--all", action="store_true", help="Run all test categories")
    parser.add_argument("--quick", action="store_true", help="Run quick validation (unit + system)")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        # Default behavior - run quick validation
        args.quick = True
    
    results = []
    
    print("🧪 Agentic GraphRAG System - Test Runner")
    print(f"Working directory: {Path.cwd()}")
    
    try:
        if args.unit or args.all or args.quick:
            results.append(("Unit Tests", run_unit_tests()))
        
        if args.integration or args.all:
            results.append(("Integration Tests", run_integration_tests()))
        
        if args.performance or args.all:
            results.append(("Performance Tests", run_performance_tests()))
        
        if args.real or args.all:
            results.append(("Real Integration Tests", run_real_integration_tests()))
        
        if args.quality or args.all:
            results.append(("Code Quality", run_code_quality_checks()))
        
        if args.system or args.all or args.quick:
            results.append(("System Validation", run_system_validation()))
        
        if args.a2a or args.all:
            results.append(("A2A Validation", run_a2a_validation()))
        
        if args.coverage or args.all:
            results.append(("Coverage Report", run_coverage_report()))
        
        if not results:
            results.append(("All Tests", run_all_tests()))
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        return 1
    
    # Summary
    print(f"\n{'='*80}")
    print("📋 TEST SUMMARY")
    print(f"{'='*80}")
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:30} {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} test categories passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())