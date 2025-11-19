import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer

train = pd.read_csv('./train.csv')
test = pd.read_csv('./test.csv')

train = train.replace(r'^\s*$', None, regex=True)
test = test.replace(r'^\s*$', None, regex=True)

num_cols = ['ClientPeriod', 'MonthlySpending', 'TotalSpent']
cat_cols = [
    'Sex','IsSeniorCitizen','HasPartner','HasChild','HasPhoneService',
    'HasMultiplePhoneNumbers','HasInternetService','HasOnlineSecurityService',
    'HasOnlineBackup','HasDeviceProtection','HasTechSupportAccess',
    'HasOnlineTV','HasMovieSubscription','HasContractPhone',
    'IsBillingPaperless','PaymentMethod'
]

feature_cols = num_cols + cat_cols
target_col = 'Churn'

X_train = train[feature_cols]
y_train = train[target_col]

preprocess = ColumnTransformer(
    transformers=[
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), num_cols),

        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]), cat_cols)
    ]
)

model = Pipeline([
    ('prep', preprocess),
    ('logreg', LogisticRegression(max_iter=500))
])

model.fit(X_train, y_train)

X_test = test[feature_cols]
pred_probs = model.predict_proba(X_test)[:, 1]

submission = pd.DataFrame({
    'ID': test['ID'],
    'Churn': pred_probs
})

submission.to_csv('submission.csv', index=False)
print("Minimal submission saved!")
