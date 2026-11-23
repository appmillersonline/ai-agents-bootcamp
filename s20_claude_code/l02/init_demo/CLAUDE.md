# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A minimal Python module that calculates order totals for a small shop, using sample data. There is no package structure, dependency manifest, or build step. It is just `totals.py` and its pytest tests in `test_totals.py`.

## Commands

- Run all tests: `python3 -m pytest`
- Run a single test: `python3 -m pytest test_totals.py::test_exactly_forty_ships_free`

Tests import `totals` as a top-level module, so run pytest from the repository root.

## Business rules (`totals.order_total`)

- `discount` is a fraction (`0.1` = 10%). It is applied to the item subtotal **before** the free-shipping check.
- Shipping (`SHIPPING` = 4.50) is added only when the discounted subtotal is **below** `FREE_SHIPPING_FROM` (40.0). Exactly 40.0 ships free, and a test covers that boundary.
- Results are rounded to 2 decimal places. Amounts are euros.
