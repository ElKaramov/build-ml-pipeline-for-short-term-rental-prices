#!/usr/bin/env python
"""
long_description [An example of a step using MLflow and Weights & Biases]: Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
logger.info("Downloading artifact from W&B for basic cleaning")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact that was cleaned",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Artifact type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=int,
        help="minimum price of the rental",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=int,
        help="maximum price of the rental",
        required=True
    )
    args = parser.parse_args()

    go(args)
