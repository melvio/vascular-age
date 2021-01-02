import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.base import RegressorMixin
from sklearn.dummy import DummyRegressor as Baseline
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet, SGDRegressor as SGD
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.svm import LinearSVR, SVR
from tqdm import tqdm


class RunResults:
    def __init__(self, *, kfold_results: DataFrame,
                 age_predictions: DataFrame,
                 fitted_models: [RegressorMixin]):
        self.kfold_results = kfold_results
        self.age_predictions = age_predictions
        self.fitted_models = fitted_models


class CtCalcificationModelRunner:
    def __init__(self, *,
                 models=None,
                 k: int,
                 scoring: callable = None):
        """
        :param models: models to run
        :param k: number of folds in k-fold cross validation
        :param scoring: scoring function (default: mean absolute error)
        """
        self._models = models
        self.k = k
        self.scoring = scoring if scoring else make_scorer(mean_absolute_error)
        self.results = DataFrame()  # results will be populated after models ran
        self.age_predictions = DataFrame()  # results will be populated after model ran

    @property
    def models(self) -> [RegressorMixin]:
        if self._models is None:
            self._models = [LinearSVR(), SVR(), SVR(C=100), SVR(kernel='poly'),
                            LinearRegression(), Lasso(), ElasticNet(),
                            SGD(), SGD('epsilon_insensitive'), SGD('squared_epsilon_insensitive'),
                            Baseline(strategy='median')]

        return self._models if isinstance(self._models, list) else [self._models]

    def run_models(self, *, features: np.ndarray, labels: np.ndarray) -> RunResults:
        """

        :param features: features on which to train models on
        :param labels: labels that models use to calculate loss
        :return: a DataFrame containing k-fold cross validation results and list of fitted models for later analysis
        """
        # todoN2H: this can be done in multi-threaded manner since every iter is temporally independent
        # * only diff is the results in the results table, but we end up sorting it anyways
        for i, model in enumerate(tqdm(self.models, total=len(self.models))):
            kfold_predictions: [float] = cross_val_score(model, features, labels, cv=self.k, scoring=self.scoring)
            model.fit(features, labels)

            kfold_col_dict = {f'kfold={n}': kfold_pred for n, kfold_pred in enumerate(kfold_predictions)}
            #  TODON2H You don't append every row separately. Performance wise it is better to do this in one call.
            new_row = DataFrame({
                'model': model,
                'score': np.mean(kfold_predictions),
                **kfold_col_dict,
                'k_fold_stdev': np.std(kfold_predictions)
            }, index=[i])
            self.results = self.results.append(new_row)

            age_preds = DataFrame(data={
                'model': [model for _ in labels],
                'age_pred': model.predict(features),
                'age_label': labels
            })

            self.age_predictions = self.age_predictions.append(age_preds, ignore_index=True)

        return RunResults(
            kfold_results=self.results,
            age_predictions=self.age_predictions,
            fitted_models=self.models
        )

#%%

# runner = CtCalcificationModelRunner()
# results = runner.run_models(features=np.arange(5 * 2).reshape((5, 2)), labels=np.arange(5))
# pd.set_option('display.max_columns', None)
# print(results)
