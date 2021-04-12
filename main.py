from dataflow.flow import Flow
import argparse
from utils.logger import LogSystem

logger = LogSystem()


def main(arguments):
    logger.log_info("Running Pipeline")

    if arguments.Mode.lower() == 'create':
        Flow(ontology=arguments.ontology.lower()).create()
    elif arguments.Mode.lower() == 'update':
        Flow(ontology=arguments.ontology.lower()).update()
    else:
        logger.log_error("Unsupported Mode")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A data Pipeline for OLS API.")
    parser.add_argument("--ontology", type=str, default='EFO', help="define an ontology type")
    parser.add_argument("--Mode", type=str, default='Create',
                        help="Define in which mode you want to run the pipeline. Choose between"
                             "<Create> and <Update>")
    args = parser.parse_args()
    main(args)
