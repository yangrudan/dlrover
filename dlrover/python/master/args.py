# Copyright 2022 The DLRover Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from dlrover.python.common.global_context import DefaultValues
from dlrover.python.common.log import default_logger as logger


def add_params(parser):
    parser.add_argument("--job_name", help="ElasticJob name", required=True)
    parser.add_argument(
        "--namespace",
        default="default",
        type=str,
        help="The name of the Kubernetes namespace where ElasticJob "
        "pods will be created",
    )
    parser.add_argument(
        "--platform",
        default="pyk8s",
        type=str,
        help="The name of platform which can be pyk8s, k8s, ray or local.",
    )
    parser.add_argument(
        "--pending_timeout",
        "--pending-timeout",
        default=DefaultValues.SEC_TO_WAIT_PENDING_POD,
        type=int,
        help="The timeout value of pending.",
    )
    parser.add_argument(
        "--pending_fail_strategy",
        "--pending-fail-strategy",
        default=DefaultValues.PENDING_FAIL_STRATEGY,
        type=int,
        help="The fail strategy for pending case. "
        "Options: -1: disabled; 0: skip; 1: necessary part; 2: all",
    )
    parser.add_argument(
        "--service_type",
        "--service-type",
        default="grpc",
        type=str,
        help="The service type of master: grpc/http.",
    )


def print_args(args, exclude_args=[], groups=None):
    """
    Args:
        args: parsing results returned from `parser.parse_args`
        exclude_args: the arguments which won't be printed.
        groups: It is a list of a list. It controls which options should be
        printed together. For example, we expect all model specifications such
        as `optimizer`, `loss` are better printed together.
        groups = [["optimizer", "loss"]]
    """

    def _get_attr(instance, attribute):
        try:
            return getattr(instance, attribute)
        except AttributeError:
            return None

    dedup = set()
    if groups:
        for group in groups:
            for element in group:
                dedup.add(element)
                logger.info("%s = %s", element, _get_attr(args, element))
    other_options = [
        (key, value)
        for (key, value) in args.__dict__.items()
        if key not in dedup and key not in exclude_args
    ]
    for key, value in other_options:
        logger.info("%s = %s", key, value)


def pos_int(arg):
    res = int(arg)
    if res <= 0:
        raise ValueError("Positive integer argument required. Got %s" % res)
    return res


def _build_master_args_parser():
    parser = argparse.ArgumentParser(description="Training Master")
    parser.add_argument(
        "--port",
        default=0,
        type=pos_int,
        help="The listening port of master",
    )
    parser.add_argument(
        "--node_num",
        default=1,
        type=pos_int,
        help="The number of nodes",
    )
    parser.add_argument(
        "--hang_detection",
        default=1,
        type=pos_int,
        help="The strategy of 'hang detection', "
        "0: log only; 1: notify; 2: with fault tolerance",
    )
    add_params(parser)
    return parser


def parse_master_args(master_args=None):
    parser = _build_master_args_parser()

    args, unknown_args = parser.parse_known_args(args=master_args)
    print_args(args)
    if unknown_args:
        logger.warning("Unknown arguments: %s", unknown_args)

    return args
