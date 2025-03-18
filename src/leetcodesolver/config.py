#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv
from phoenix.otel import register

from opentelemetry import trace
from enum import Enum
load_dotenv(override=True)


def init_trace():
    global tracer_provider
    PHOENIX_COLLECTOR_ENDPOINT = os.getenv(
        "PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces")
    tracer_provider = register(
        project_name=os.getenv('PHOENIX_PROJECT_NAME',
                               'default'),  # Default is 'default'
        endpoint=PHOENIX_COLLECTOR_ENDPOINT,
        batch=os.getenv("BATCH_TRACER", "true").lower(
        ) == "true",  # Default is True
        auto_instrument=True,
    )
