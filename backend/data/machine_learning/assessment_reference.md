# Machine Learning Assessment Reference

## Math & Statistics Foundations
Vectors and matrices represent features and transformations; derivatives guide optimization. Probability models uncertainty, while confidence intervals and hypothesis tests quantify evidence under assumptions.
## Data Preparation
Fit preprocessing only on training data to prevent leakage. Missingness, categorical encoding, scaling, imbalance, and outliers need model- and domain-aware treatment.
## EDA & Feature Engineering
EDA finds distributions, relationships, anomalies, and data-quality issues without using test outcomes. Features should be available at prediction time and stable under deployment conditions.
## Linear Regression
Least squares minimizes squared residuals under assumptions used for inference, not basic fitting alone. Regularization controls coefficient complexity; correlation does not establish causation.
## Classification
Logistic regression models log odds and produces scores interpretable as probabilities when calibrated. Threshold choice depends on error costs, not a universal 0.5 rule.
## Trees & Ensemble Models
Trees split feature space and can overfit without constraints. Bagging reduces variance, boosting corrects sequential residuals, and feature importance can be biased or misleading.
## Unsupervised Learning
Clustering discovers structure without labels, so evaluation needs geometry, stability, or domain utility. PCA finds high-variance linear directions and is not a clustering algorithm.
## Model Evaluation
Use held-out data or cross-validation and metrics aligned to objectives. Accuracy can hide minority failure; precision, recall, F1, ROC, PR, calibration, and cost answer different questions.
## Overfitting & Regularization
Overfitting is low training error with poor generalization. Regularization, simpler models, more representative data, augmentation, and early stopping manage bias-variance trade-offs.
## Optimization
Gradient descent follows local derivative information; learning rate controls progress and stability. Batch, stochastic, and mini-batch variants trade noise, speed, and memory.
## Neural Networks
Forward passes compute predictions and backpropagation applies the chain rule for gradients. Activations add nonlinearity; normalization and initialization influence optimization rather than model correctness alone.
## Natural Language Processing
Tokenization maps text to model units, embeddings represent learned relationships, and attention conditions representations on context. Evaluation must account for ambiguity, bias, and task-specific failure.
## Computer Vision
Convolutions exploit local structure and shared weights; augmentation encodes plausible invariances. Classification, detection, and segmentation require different labels and metrics.
## ML Deployment & MLOps
Production needs reproducible data, model versioning, serving, monitoring, drift detection, and safe rollback. Data drift does not always imply performance drift, which needs labels or proxies.
## Responsible ML
Fairness definitions can conflict and depend on context. Explainability, privacy, consent, robustness, human oversight, and recourse are lifecycle concerns.
