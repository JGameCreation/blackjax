from typing import Callable

import jax
import jax.numpy as jnp

from blackjax.types import PyTree


def gradient_estimator_fn(
    logprior_fn: Callable, loglikelihood_fn: Callable, data_size: int
) -> Callable:
    """Builds a simple gradient estimator.

    This estimator first appeared in [1]_.

    Parameters
    ----------
    logprior_fn
        The log-probability density function corresponding to the prior distribution.
    loglikelihood_fn
        The log-probability density function corresponding to the likelihood.
    data_size
        The number of items in the full dataset.

    References
    ----------
    .. [1]: Robbins H. and Monro S. A stochastic approximation method. Annals of Mathematical Statistics, 22(30):400-407, 1951.

    """

    def logposterior_estimator_fn(position: PyTree, data_batch) -> float:
        """Returns an approximation of the log-posterior density.

        Parameters
        ----------
        position
            The current value of the random variables.
        data_batch
            The current batch of data

        Returns
        -------
        An approximation of the value of the log-posterior density function for
        the current value of the random variables.

        """
        batch_loglikelihood = jax.vmap(loglikelihood_fn, in_axis=(None, 0))
        return logprior + data_size * jnp.mean(
            batch_loglikelihood(position, data_batch), axis=0
        )

    logprob_grad = jax.grad(logposterior_estimator_fn)

    return logprob_grad
