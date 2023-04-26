# MLOps Accelerator for Edge

> **Note:**
> This is a repo that can be shared to our customers. This means it's NOT OK to include Microsoft confidential
> content. All discussions should be appropriate for a public audience.

MLOps accelerator for Edge is an end to end workflow that supports generating and deploying models on IoT Edge devices. 

## Features

- Supports generation of multiple ML Models
- MLOps pipeline for Data preparation, transformation, Model Training, evaluation, scoring and registration 
- Each ML Model is packaged in a independent Docker Image
- Model verification before storing the Docker image
- All Docker images are stored in Azure Container Registry
- Gated approval before moving to deployment phase
- Supports deployment of Edge Modules to multiple and dynamically selected IoT Edge devices based on conditions
- Automated and incremental layered deployment of ML Models on Edge devices 
- Builds and deploys Smoke Test module on Edge device
- Smoke test of ML Model on each Edge device after deployment
- Supports storing inference input and outputs on Edge device
- Based on Azure ML SDK v2 1.4 and IoT Edge runtime 1.4

## About this repo

The idea of this end to end workflow is to provide a minimum number of scripts to implement development environment to train new models, embed them into Docker Images, deploy them on Edge devices and test them using Azure ML SDK v2, IoT Edge and Azure DevOps.

The workflow contains the following folders/files:

- devops: the folder contains Azure DevOps related files (yaml files to define Builds).
- docs: documentation.
- src: source code that is not related to Azure ML directly. This is typically data science related code.
- mlops: scripts that are related to Azure ML.
- mlops/nyc-taxi: a fake pipeline with some basic code to build a model
- mlops/london-taxi: a fake pipeline with some basic code to build another model
- test: a folder with dummy test to write unit tests for the build
- model: Model related files and dependencies
- edge: contains layered deployment manifest to deploy ML Models and Test Modules
- edge-smoke-test: packages smoke test logic into Docker images and pushes it to ACR
- .amlignore: using this file we are removing all the folders and files that are not supposed to be in Azure ML compute.

The workflow contains the following documents:

- docs/how_to_setup.md: explain how to configure the workflow.

## How to use the repo

Information about how to setup the repo is in [the following document](./docs/how_to_setup.md).  

## Reference

* [Azure IoT Hub](https://azure.microsoft.com/en-gb/products/iot-hub)
* [Azure IoT Edge documentation](https://learn.microsoft.com/en-us/azure/iot-edge/?view=iotedge-1.4)
* [Azure Container Registry](https://azure.microsoft.com/en-us/products/container-registry/)
* [Azure Machine learning](https://docs.microsoft.com/azure/machine-learning)
* [Azure DevOps pipelines](https://learn.microsoft.com/en-gb/azure/devops/pipelines/)
* [Dockerfile](https://docs.docker.com/engine/reference/builder/)
* [Azure Machine learning SDK V2](https://learn.microsoft.com/en-gb/python/api/overview/azure/ai-ml-readme?view=azure-python)
* [Azure IoT CLI](https://learn.microsoft.com/en-us/cli/azure/azure-cli-reference-for-iot)
* [Azure AD Service Principal](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
* [Azure Key Vault](https://learn.microsoft.com/en-gb/azure/key-vault/general/)