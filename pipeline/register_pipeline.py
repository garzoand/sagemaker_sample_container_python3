# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""A CLI to create or update and run pipelines."""
from __future__ import absolute_import

import argparse
import json
import sys

from utils import get_pipeline_driver

sys.path.append('../model/')

DEFAULT_REGION='us-west-2'

def main():  # pragma: no cover
    """The main harness that creates or updates and runs the pipeline.

    Creates or updates the pipeline and runs it.
    """
    parser = argparse.ArgumentParser(
        "Creates or updates and runs the pipeline for the pipeline script."
    )

    parser.add_argument(
        "-role-arn",
        "--role-arn",
        dest="role_arn",
        type=str,
        help="The role arn for the pipeline service execution role.",
    )
    args = parser.parse_args()

    if args.role_arn is None:
        parser.print_help()
        sys.exit(2)

    try:
        pipeline = get_pipeline_driver('pipeline', DEFAULT_REGION, args.role_arn)
        print("###### Creating/updating a SageMaker Pipeline with the following definition:")
        parsed = json.loads(pipeline.definition())
        print(json.dumps(parsed, indent=2, sort_keys=True))

        upsert_response = pipeline.upsert(
            role_arn=args.role_arn, description="Model Pipeline"
        )
        print("\n###### Created/Updated SageMaker Pipeline: Response received:")
        print(upsert_response)

#        execution = pipeline.start()
#        print(f"\n###### Execution started with PipelineExecutionArn: {execution.arn}")

        #print("Waiting for the execution to finish...")
        #execution.wait()
        #print("\n#####Execution completed. Execution step details:")

        #print(execution.list_steps())
        # Todo print the status?
    except Exception as e:  # pylint: disable=W0703
        print(f"Exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
