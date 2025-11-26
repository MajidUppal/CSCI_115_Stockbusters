## Model Development & Optimization

### Feature Engineering & Selection

**Approach**: Manual feature engineering and selection based on financial domain knowledge and exploratory data analysis (part of jupyter notebook).

**Features Selected**:
- **Technical Indicators** (lagged to prevent leakage):
  - `return_1m_lag1`, `return_3m_lag1`, `return_6m_lag1`
  - `volatility_20d_lag1`, `volatility_60d_lag1`
  - `rsi_14_lag1`, `volume_ratio_lag1`

- **Fundamental Metrics** (forward-filled quarterly):
  - `pe_ratio`, `price_to_book`, `debt_to_equity`
  - `roe`, `revenue_growth`, `eps_growth`

- **Combined Features**:
  - ~20 engineered features total
  - Features validated through correlation analysis
  - Removed highly correlated features (>0.95)

**Rationale**: 
- Domain-driven feature selection based on established quantitative finance principles
- Lagged technical features prevent data leakage
- Forward-filled fundamentals match real-world quarterly reporting lag

### Model Parameters

**Model**: Random Forest Classifier

**Parameters**:
```python
{
    'n_estimators': 100,          # Standard for financial data
    'max_depth': 20,               # Prevents overfitting
    'min_samples_split': 10,       # Ensures statistical significance
    'min_samples_leaf': 5,         # Reduces variance
    'class_weight': 'balanced',    # Handles class imbalance
    'random_state': 42             # Reproducibility
}
```

**Justification**: These parameters are based on best practices for financial time series:
- Ensemble size (100 trees) balances performance and training time
- Depth limit prevents overfitting on noisy market data
- Minimum samples ensure statistical reliability
- Balanced class weights address market regime shifts

### Model Performance

- **Accuracy**: ~62-65% (above random baseline of 50%)
- **Precision**: ~0.63 (63% of predicted outperformers actually outperform)
- **Recall**: ~0.61 (identifies 61% of actual outperformers)
- **AUC-ROC**: ~0.68 (good discriminative ability)

**Baseline Comparison**:
- Random prediction: 50% accuracy
- Always predict majority class: 50% accuracy
- Our model: **62-65% accuracy** (24-30% improvement)

### Future Enhancements ### 

MS4 focuses on establishing robust pipeline infrastructure. However there are still room in the future to improve this model.

1. **Systematic Hyperparameter Tuning**:
   - GridSearchCV across parameter space
   - Cross-validation on walk-forward basis
   - Target: 2-3% accuracy improvement

2. **Model Ensemble**:
   - Combine RF with XGBoost and LightGBM
   - Weighted voting based on validation performance

3. **Additional Features**:
   - Sentiment analysis from news
   - Alternative data integration
   - Macroeconomic indicators

