from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.processing import ProcessingInput, ProcessingOutput, ScriptProcessor
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.condition_step import ConditionStep, JsonGet
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.parameters import ParameterInteger, ParameterString
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.step_collections import RegisterModel
from sagemaker.workflow.steps import ProcessingStep, TrainingStep

import sagemaker
import boto3

def get_session(region):
    session = boto3.Session(region_name=region)
    sm_client = session.client('sagemaker')
    smr_client = session.client('sagemaker-runtime')
    return sagemaker.session.Session(
        boto_session=session,
        sagemaker_client=sm_client,
        sagemaker_runtime_client=smr_client
    )

# Must be implemented by the Data Scientist
def get_pipeline(region, role, image_uri, model_path):

    session = get_session(region)
    if role is None:
        role = sagemaker.session.get_execution_role(session)

    train_data_param = ParameterString(name='train-data')
    validation_data_param = ParameterString(name='validation-data')
    image_uri_param = ParameterString(name='image-uri')
    model_path_param = ParameterString(name='model-path')

    estimator = Estimator(
        image_uri=image_uri,
        instance_type='ml.m5.xlarge',
        instance_count=1,
        output_path=model_path,
        sagemaker_session=session,
        role=role
    )

    ### Your Pipeline definition goes here ....
    ###########################################

    step_train = TrainingStep(
        name="iris-model-train",
        estimator=estimator,
        inputs={
            "train": TrainingInput(
                s3_data = train_data_param,
                content_type='text/csv'
            ),
            "validation": TrainingInput(
                s3_data = validation_data_param,
                content_type='text/csv'
            )        
        }
    )

    step_register = RegisterModel(
        name='iris-model-register',
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        estimator=estimator,
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.large"],
        transform_instances=["ml.m5.large"],
        model_package_group_name='iris-model'
    )

    pipeline = Pipeline(
        name='iris-model-pipeline',
        steps = [step_train, step_register],
        parameters = [train_data_param, validation_data_param],
        sagemaker_session=session        
    )

    ### end of Pipeline definition
    ###########################################

    return pipeline
