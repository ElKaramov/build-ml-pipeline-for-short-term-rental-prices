#!/usr/bin/env python
"""
This Module performs basic cleaning on 
the data and save the results in Weights & Biases
"""
import argparse
import logging
import pandas as pd
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
    logger.info(f"Using artifact {args.input_artifact}")
    
    #Artifact path:
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Reading the csv file of the artifact using the path")
    # reading the data
    df = pd.read_csv(artifact_local_path)

    logger.info(f"Selecting only those data in which price feature \
                is between {args.min_price} and {args.max_price}")

    idx = df["price"].between(args.min_price, args.max_price) & \
        df['longitude'].between(-74.25, -73.50) & \
        df['latitude'].between(40.5, 41.2)

    new_df = df[idx].copy()

    logger.info("Converting last_review variable to datatime type")
    new_df["last_review"] = pd.to_datetime(new_df["last_review"])

    # saving the output artifact as a csv file and
    new_df.to_csv("clean_sample.csv", index=False)

    logger.info(f"Creating artifact name {args.output_artifact}")
    
    # Uploading artifact to W&B:
     #-Creating the Artifact:
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )

    #-Adding our saved file:
    artifact.add_file("clean_sample.csv")

    #-Uploading the artifact:
    run.log_artifact(artifact)
    logger.info("Artifact uploaded to W&B")


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
