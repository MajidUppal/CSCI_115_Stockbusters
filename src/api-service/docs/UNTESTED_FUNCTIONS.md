# API Service - Untested Functions Documentation

**Last Updated:** December 2024  
**Current Test Coverage:** ~70% overall (exceeds 60% minimum requirement)  
**Purpose:** Document production code paths not covered by **unit tests**, with justifications.

**Note:** This document excludes legacy, archived, duplicated, or unused code.

---

## Overview

This document lists **production code paths** not covered by **unit tests** and explains why. Many are tested in **integration tests**. All critical business logic, API endpoints, and core functionality **are tested**.

---

## Untested Production Code Paths (Unit Tests)

### 1. API Validation Error Paths

**File:** `routers/chatbot_final.py`  
**Untested in Unit Tests:** Lines 123, 160, 163, 193, 198, 255, 258, 267

**Functions:**
- `get_chats()` (line 123): Missing `X-Session-ID` header validation
- `get_chat()` (lines 160, 163): Missing `X-Session-ID` header, chat not found
- `start_chat()` (lines 193, 198): Missing `X-Session-ID` header, missing message content
- `continue_chat()` (lines 255, 258, 267): Missing `X-Session-ID` header, chat not found, missing message content

**Why Not Tested in Unit Tests:**
- Unit tests always provide valid inputs (session IDs, chat IDs, message content)
- Focus on happy path and business logic validation
- **Note:** Most of these ARE tested in integration tests:
  - Line 123: `test_get_chats_requires_session_header` ✅
  - Line 160: `test_get_specific_chat_requires_session` ✅
  - Line 163: `test_get_specific_chat_not_found` ✅
  - Line 193: `test_start_chat_requires_session_header` ✅
  - Line 198: `test_start_chat_requires_message` ✅
  - Line 255: `test_continue_chat_requires_session` ✅
  - Line 258: `test_continue_chat_not_found` ✅
  - Line 267: ❌ **Not tested** (missing message content in continue_chat)

**Recommendation:** ✅ **Acceptably untested in unit tests** - Most tested in integration tests. Line 267 could be added to integration tests.

---

### 2. Module-Level Initialization Code

#### `routers/chatbot_final.py` - Credential Loading (Lines 62-63, 69, 101)

**Code:**
```python
# Lines 62-63: Credential loading (when file exists)
credentials = service_account.Credentials.from_service_account_file(credentials_path)
llm = ChatVertexAI(model="gemini-2.5-flash", credentials=credentials)

# Line 69: Exception handler
except Exception as e:
    print(f"Info: Could not load credentials: {e}...")

# Line 101: ChatAgent initialization (when llm is not None)
if llm is not None:
    abot = ChatAgent(llm, [], system=system_prompt, checkpointer=memory)
```

**Why Not Tested:**
- `conftest.py` patches `service_account.Credentials.from_service_account_file` at module level (line 44-55) before imports
- Tests mock entire credential loading to avoid requiring actual credentials
- These paths never execute in test environment due to mocking

**Recommendation:** ✅ **Correctly untested** - Appropriately mocked at module level.

#### `routers/stock_details.py` - DataFrame Fallback (Lines 38, 40, 42)

**Code:**
```python
if df_quant_model is None:
    df_quant_model = pd.DataFrame()  # Line 38 - UNTESTED
if df_company_profile is None:
    df_company_profile = pd.DataFrame()  # Line 40 - UNTESTED
if df_stocks is None:
    df_stocks = pd.DataFrame()  # Line 42 - UNTESTED
```

**Why Not Tested:**
- Tests patch `get_gcs_data()` to always return sample DataFrames (see `conftest.py`)
- Defensive code for production GCS failures
- Tested indirectly through empty DataFrame handling in utility functions

**Recommendation:** ✅ **Acceptably untested** - Defensive code, tested indirectly.

#### `utils/get_gcs_bucket.py` - GCS Client Initialization (Lines 13, 14, 20, 21)

**Code:**
```python
# Lines 13-14: Successful initialization
storage_client = storage.Client.from_service_account_json(credentials_path)
print(f"GCS Client initialized...")

# Lines 20-21: Exception handler
except Exception as e:
    print(f"Info: Could not initialize GCS Client: {e}...")
    storage_client = None
```

**Why Not Tested:**
- `conftest.py` patches `storage.Client` at module level (line 34-40) before imports
- Tests always use mocked storage client
- These paths never execute in test environment

**Recommendation:** ✅ **Correctly untested** - Appropriately mocked.

---

### 3. Edge Cases

#### `routers/stock_details.py` - Default Fallback (Line 116)

**Code:**
```python
else:
    # Use Hybrid_Score as default
    ai_score = float(stock_info.get("Hybrid_Score", 0)) if pd.notna(stock_info.get("Hybrid_Score")) else 0.0
```

**Why Not Tested:**
- Edge case when neither `short_term` nor `long_term` selected (unlikely - UI requires selection)
- Simple fallback logic, low complexity
- All other conditional branches (short_term, long_term, both) are tested

**Recommendation:** ✅ **Acceptably untested** - Edge case, low risk.

#### `utils/get_gcs_bucket.py` - Parquet File Type (Line 46)

**Code:**
```python
elif file_type == "parquet":
    df = pd.read_parquet(BytesIO(csv_bytes))
```

**Why Not Tested:**
- Similar logic to CSV path (line 45, which is tested)
- Tests use CSV format; parquet follows same pattern
- Production uses parquet for `df_stocks`, but tests mock dataframes directly

**Recommendation:** ✅ **Acceptably untested** - Similar to tested CSV path.

#### `utils/chat_bot_agent.py` - Empty System Prompt (Line 43)

**Code:**
```python
def call_llm(self, state: ChatAgentState):
    messages = state["messages"]
    if self.system:
        messages = [SystemMessage(content=self.system)] + messages  # Line 42 - tested
    # Line 43 - UNTESTED: implicit else (when self.system is empty)
    message = self.model.invoke(messages)
```

**Why Not Tested:**
- Edge case - system prompt always provided in practice
- Function works correctly without system prompt
- System prompt behavior tested when provided (line 42)

**Recommendation:** ✅ **Acceptably untested** - Edge case, low risk.

---

### 4. Side Effects

**Print statements** throughout codebase - Not tested (standard practice, not business logic)

---

## Summary

| Category | Lines | Status | Reason |
|----------|-------|--------|--------|
| API validation errors (unit tests) | 8 | ⚠️ Mostly tested in integration | 7/8 tested in integration, 1 missing |
| Module initialization | ~10 | ✅ Correctly mocked | Appropriately mocked at module level |
| Edge cases | 3 | ✅ Acceptable | Low risk, unlikely scenarios |
| Side effects | ~5 | ✅ Correct | Not business logic |

**Total Untested in Unit Tests:** ~20 lines  
**Current Coverage:** ~70% (exceeds 60% requirement)  
**Note:** Most validation errors ARE tested in integration tests (7 of 8 paths)

---

## Testing Strategy

### What We Test ✅
- All API endpoints (unit, integration, system tests)
- All business logic and core utilities
- Service layer, middleware, routing
- Data processing algorithms
- Most validation errors (integration tests)

### What We Don't Test in Unit Tests (Production Code) ❌
- Module-level initialization (mocked)
- Defensive code paths (tested indirectly)
- Edge cases (low risk)
- Side effects (print statements)
- Some validation errors (tested in integration tests)

---

## Coverage by Module

| Module | Coverage | Status |
|--------|----------|--------|
| `service.py` | 100% | ✅ Fully tested |
| `routers/chatbot_final.py` | ~89% | ✅ Core tested |
| `routers/stock_details.py` | ~95% | ✅ Core tested |
| `utils/chat_bot_agent.py` | 100% | ✅ Fully tested |
| `utils/detailed_page_funcs.py` | 100% | ✅ Fully tested |
| `utils/get_gcs_bucket.py` | ~85% | ✅ Core tested |

---

## Conclusion

The API service has **comprehensive test coverage** of all critical functionality. Untested production code paths in unit tests are intentionally excluded because they are:

1. **Module Initialization**: Appropriately mocked at module level
2. **Defensive Code**: Tested indirectly through error handling
3. **Edge Cases**: Low-risk, unlikely scenarios
4. **Side Effects**: Not business logic
5. **Validation Errors**: Most tested in integration tests (7 of 8 paths)

**Current test coverage (~70%) exceeds the 60% requirement** and focuses on high-value, high-risk functionality.

---

## References

- **Test Files:** `src/api-service/tests/`
- **CI Pipeline:** `.github/workflows/ci.yml`
- **Coverage Reports:** `src/api-service/coverage/`
