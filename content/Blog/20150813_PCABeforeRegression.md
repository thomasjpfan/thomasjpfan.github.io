Title: PCA Before Regression
Date: 2015-08-15 19:29
Tags: machine learning, python
Image: 20150813_PCABeforeRegression/front.png
Summary: Sometimes it can be quite harmful to remove features in a data set. This entry gives an example of when principle component analysis can drastically change the result of a simple linear regression.

Sometimes it can be quite harmful to remove features in a data set. This entry gives an example of when principle component analysis can drastically change the result of a simple linear regression. I am also trying out importing <a href="http://jupyter.org" target="_blank">Jupyter notebooks</a> into this post, so you will see In[] and Out[] tags, which signify the input and output of the notebook$.$

{% notebook 20150813_PCABeforeRegression.ipynb cells[1:] %}

One should be careful when performing feature engineering, you may accidentally lose some crucial information.
