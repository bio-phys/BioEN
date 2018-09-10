#ifndef KERNELS_LOGW_H
#define KERNELS_LOGW_H

/** C implementations of (grad_)_log_posterior(_forces), header file.
 */

#include "c_bioen_common.h"

double _bioen_log_posterior_logw(double *, double *, double *, double *,
                                 double *, double *, double *, double *, double,
                                 int, double *, double *, double *, int, int);
void _grad_bioen_log_posterior_logw(double *, double *, double *, double *,
                                    double *, double *, double *, double *,
                                    double, int, double *, double *, double *,
                                    int, int);

double _opt_bfgs_logw(double *, double *, double *, double *, double *,
                      double *, double *, double *, double, int, int,
                      struct gsl_config_params, struct caching_params,
                      struct visual_params);
double _opt_lbfgs_logw(double *, double *, double *, double *, double *,
                       double *, double *, double *, double, int, int,
                       struct lbfgs_config_params, struct caching_params,
                       struct visual_params);

#endif