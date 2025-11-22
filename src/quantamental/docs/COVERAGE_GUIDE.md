# 🎯 Coverage Improvement Plan - Reach 50% for MS4

## Current Situation
- **Current coverage:** ~35-40%
- **MS4 requirement:** ≥50%
- **Your setting:** 60%
- **Status:** ❌ Need more tests!

---

## Quick Win Strategy: Reach 50% Coverage

### Priority Test Files to Create

Create these test files in this order for maximum coverage gain:

#### 1. **test_data_process.py** (Highest Impact!)
```python
"""Tests for data processing module"""
import pytest
import pandas as pd
from data_process import process_data, engineer_features

@pytest.mark.unit
def test_process_data_basic():
    """Test basic data processing."""
    df = pd.DataFrame({
        'symbol': ['AAPL', 'MSFT'],
        'date': ['2023-01-01', '2023-01-02'],
        'close': [150.0, 250.0]
    })
    result = process_data(df)
    assert not result.empty
    assert 'symbol' in result.columns

@pytest.mark.unit
def test_engineer_features_creates_columns():
    """Test feature engineering adds columns."""
    df = pd.DataFrame({
        'symbol': ['AAPL'] * 30,
        'date': pd.date_range('2023-01-01', periods=30),
        'close': range(100, 130),
        'volume': range(1000, 1030)
    })
    result = engineer_features(df)
    
    # Should have more columns after feature engineering
    assert result.shape[1] > df.shape[1]

# Add 5-10 more tests covering different functions
```

**Expected coverage gain:** +15% → Total: ~50%

---

#### 2. **test_backtest.py** (Medium Impact)
```python
"""Tests for backtesting module"""
import pytest
import pandas as pd
from backtest import run_backtest, calculate_returns

@pytest.mark.unit
def test_calculate_returns_basic():
    """Test basic return calculation."""
    prices = pd.Series([100, 110, 105, 115])
    returns = calculate_returns(prices)
    
    assert len(returns) == len(prices) - 1
    assert abs(returns.iloc[0] - 0.10) < 0.01  # 10% return

@pytest.mark.integration
def test_run_backtest_simple():
    """Test backtest with simple data."""
    predictions = pd.DataFrame({
        'symbol': ['AAPL', 'MSFT'],
        'date': ['2023-01-01', '2023-01-01'],
        'predicted_return': [0.05, 0.03]
    })
    
    prices = pd.DataFrame({
        'symbol': ['AAPL', 'MSFT'],
        'date': ['2023-01-01', '2023-01-01'],
        'close': [150.0, 250.0]
    })
    
    result = run_backtest(predictions, prices, initial_capital=10000)
    
    assert 'final_value' in result
    assert result['final_value'] > 0

# Add 5-10 more tests
```

**Expected coverage gain:** +10% → Total: ~60%

---

#### 3. **test_model_predict.py** (Medium Impact)
```python
"""Tests for prediction module"""
import pytest
import pandas as pd
import numpy as np
from model_predict import generate_predictions, format_predictions

@pytest.mark.unit
def test_format_predictions_structure():
    """Test prediction formatting."""
    raw_predictions = np.array([0.05, 0.03, -0.02])
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    result = format_predictions(raw_predictions, symbols)
    
    assert isinstance(result, pd.DataFrame)
    assert 'symbol' in result.columns
    assert 'predicted_return' in result.columns
    assert len(result) == 3

@pytest.mark.integration
def test_generate_predictions_with_mock_model():
    """Test prediction generation with mock model."""
    # Create mock model and data
    # Test that predictions are generated correctly
    pass

# Add 5-10 more tests
```

**Expected coverage gain:** +8% → Total: ~68%

---

## Quick Coverage Wins (Low Hanging Fruit)

### Test Simple Utility Functions
Add to `test_utils.py`:

```python
@pytest.mark.unit
def test_ensure_dir_creates_nested():
    """Test creating nested directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'a', 'b', 'c')
        ensure_dir(path)
        assert os.path.exists(path)

@pytest.mark.unit
def test_get_feature_names_all_features():
    """Test getting all feature names."""
    config = load_config()
    features = get_feature_names(config)
    assert len(features) > 0
    assert all(isinstance(f, str) for f in features)
```

**Expected coverage gain:** +3% → Total: ~53%

---

## Coverage Calculation Example

### How to Calculate Your Current Coverage

```bash
# Run this in your container
pytest tests/ --cov=. --cov-report=term-missing

# Output will show:
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
data_collect.py       250    150    40%   lines 45-67, 89-120
data_process.py       180    120    33%   lines 23-45, 78-100
model_train.py        200    140    30%   lines 56-89, 101-145
model_predict.py      120     84    30%   lines 34-67, 89-110
backtest.py           150    105    30%   lines 23-56, 78-99
main.py                50     40    20%   lines 12-45
utils.py               80     16    80%   lines 45-52
-------------------------------------------------
TOTAL                1030    655    36%   ← YOUR CURRENT %
```

### Target Breakdown for 50% Coverage

You need to cover **515 lines** (50% of 1030):
- Currently tested: ~375 lines
- Need to add: ~140 more lines of tested code

**Strategy:** Focus on high-statement files first!

---

## Realistic Plan for MS4

### Minimum Viable Coverage (50%)

**Create these 3 test files:**
1. `test_data_process.py` - 15 tests → +15% coverage
2. `test_backtest.py` - 10 tests → +10% coverage  
3. Expand `test_utils.py` - 5 more tests → +3% coverage

**Total: ~53% coverage** ✅ Meets MS4!

### Time Estimate

- `test_data_process.py`: 2-3 hours
- `test_backtest.py`: 1-2 hours
- Expand `test_utils.py`: 30 minutes

**Total: 4-6 hours of work**

---

## How to Monitor Coverage While Writing Tests

### Real-time Coverage Feedback

```bash
# After writing each test, check coverage
pytest tests/ --cov=. --cov-report=term-missing

# Watch coverage increase!
# test_utils.py done:     38% → 41%
# test_data_process.py:   41% → 56%  ✅ Hit 50%!
# test_backtest.py:       56% → 66%  ✅ Hit 60%!
```

### HTML Report (Visual)

```bash
# Generate HTML report
pytest tests/ --cov=. --cov-report=html

# Open htmlcov/index.html
# Shows exactly which lines need tests (in RED)
```

---

## Quick Reference: Coverage Commands

```bash
# Basic coverage report
pytest --cov=.

# Detailed report showing untested lines
pytest --cov=. --cov-report=term-missing

# HTML report (interactive)
pytest --cov=. --cov-report=html

# Fail if coverage < 50%
pytest --cov=. --cov-fail-under=50

# Coverage for specific file
pytest tests/test_utils.py --cov=utils
```

---

## What Goes in Your MS4 Screenshot

When CI passes, screenshot should show:

### GitHub Actions Tab
```
✅ Quantamental CI/CD - MS4
  ✅ Code Quality Checks (30s)
     ✅ Lint with flake8
     ✅ Check code formatting with Black
  ✅ Run Tests (3m 45s)
     ✅ Run tests with pytest
     ✅ Check coverage threshold
        Coverage: 53% ✅ (required: 50%)
  ✅ Build and Test Docker Image (2m 12s)
```

### Coverage Report Section
```
---------- coverage: platform linux, python 3.10 ----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
data_collect.py       250    120    52%   lines 89-120, 145-167
data_process.py       180     80    56%   lines 78-100, 134-156
backtest.py           150     65    57%   lines 89-110, 145-160
utils.py               80     16    80%   lines 45-52
-------------------------------------------------
TOTAL                1030    485    53%   ✅ PASSES (≥50%)
```

---

## Action Plan: Next 2 Hours

1. **Lower threshold to 50%** (5 min)
   - Edit `pytest.ini`: `--cov-fail-under=50`
   - Edit `ci.yml`: `coverage report --fail-under=50`

2. **Create test_data_process.py** (90 min)
   - 10 unit tests for key functions
   - 3 integration tests

3. **Run coverage check** (5 min)
   ```bash
   pytest tests/ --cov=. --cov-report=term-missing
   ```

4. **If <50%, add more tests** (30 min)
   - Use HTML report to find untested lines
   - Add quick tests for simple functions

5. **Push to GitHub** (5 min)
   ```bash
   git add .
   git commit -m "feat: Add tests to reach 50% coverage"
   git push
   ```

6. **Screenshot passing CI** ✅
   - Wait ~5 minutes for CI to run
   - Take screenshot showing all green checkmarks

---

## Tips for Writing Tests Quickly

### Use Parameterization
```python
@pytest.mark.parametrize("input,expected", [
    ([1,2,3], 6),
    ([0,0,0], 0),
    ([-1,1], 0),
])
def test_sum_function(input, expected):
    assert sum(input) == expected

# 1 test function = 3 test cases = more coverage!
```

### Test Expected Exceptions
```python
@pytest.mark.unit
def test_invalid_input_raises_error():
    with pytest.raises(ValueError):
        process_data(None)
    
    with pytest.raises(ValueError):
        process_data(pd.DataFrame())

# 2 exception tests = quick coverage boost
```

### Mock Expensive Operations
```python
@pytest.mark.unit
def test_api_call_with_mock(monkeypatch):
    """Test without real API call."""
    def mock_fetch(*args, **kwargs):
        return pd.DataFrame({'symbol': ['AAPL']})
    
    monkeypatch.setattr('data_collect.fetch_ohlcv_data', mock_fetch)
    
    # Now test runs fast without real API!
```

---

**Goal: 50% coverage in 4-6 hours of focused work!** 🎯

Focus on `test_data_process.py` first - it's your biggest coverage win! 💪
