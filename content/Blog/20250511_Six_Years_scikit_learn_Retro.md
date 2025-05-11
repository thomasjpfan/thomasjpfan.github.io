Title: Six Years as a scikit-learn maintainer - Feature Retrospective
Date: 2025-05-11 09:29
Tags: python, scikit-learn
Math: False

It's hard to believe that it's been over six years since I joined the scikit-learn team as a maintainer. As of today, I have [1,374 commits](https://github.com/scikit-learn/scikit-learn/graphs/contributors) and reviewed [3179 pull requests](https://github.com/scikit-learn/scikit-learn/pulls?q=is%3Apr+is%3Aopen+reviewed-by%3A%40me). Behind these numbers, I am grateful for all the thoughtful discussions I have had with the community to push scikit-learn forward. Reviewing my commits, I would like to showcase some of my favorite features that I worked on:

### 1. Everything Trees 🌲🌲🌲
- Native categorical support in Histogram-based Gradient Boosting Trees. ([gh-26411](https://github.com/scikit-learn/scikit-learn/pull/26411), [gh-18394](https://github.com/scikit-learn/scikit-learn/pull/18394))
- Native missing value support in Random Forest & Trees. ([gh-23595](https://github.com/scikit-learn/scikit-learn/pull/23595), [gh-26391](https://github.com/scikit-learn/scikit-learn/pull/26391))
- Cost complexity pruning In Trees. ([gh-12887](https://github.com/scikit-learn/scikit-learn/pull/12887))

### 2. DataFrame interoperability 🖼️
- Pandas and Polars DataFrame output with the `set_output` API. ([gh-27315](https://github.com/scikit-learn/scikit-learn/pull/27315))
- `get_feature_names_out`: Mapping input feature names to output feature names. ([gh-18444](https://github.com/scikit-learn/scikit-learn/pull/18444))

### 3. Preprocessing 🔪
- `TargetEncoder`: Uses the target to encode categorical data. ([gh-25334](https://github.com/scikit-learn/scikit-learn/pull/25334))
- Group infrequent categories in `OrdinalEncoder` and `OneHotEncoder`. ([gh-25677](https://github.com/scikit-learn/scikit-learn/pull/25677))
- KNN-based missing value imputation. ([gh-12852](https://github.com/scikit-learn/scikit-learn/pull/12852))

### 4. Visualizations 📊
- HTML Representation to visualize estimators in Jupyter notebooks. ([gh-14180](https://github.com/scikit-learn/scikit-learn/pull/14180))
- Plotting API for evaluating or inspecting estimators. ([gh-14357](https://github.com/scikit-learn/scikit-learn/pull/14357))

### 5. Experimental GPU support 🏎️
- Integrate Array API to run natively with PyTorch or CuPy arrays on a GPU. ([gh-22554](https://github.com/scikit-learn/scikit-learn/pull/22554))

I hope you found some of these features useful or discovered some of them here 😁.
