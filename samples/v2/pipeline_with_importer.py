# Copyright 2021 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pipeline using dsl.importer."""

from typing import NamedTuple
from kfp import components
from kfp.v2 import compiler
from kfp.v2 import dsl
from kfp.v2.dsl import component, importer, Dataset, Model, Input


@component
def train(
        dataset: Input[Dataset]
) -> NamedTuple('Outputs', [
    ('scalar', str),
    ('model', Model),
]):
    """Dummy Training step."""
    with open(dataset.path, 'r') as f:
        data = f.read()
    print('Dataset:', data)

    scalar = '123'
    model = 'My model trained using data: {}'.format(data)

    from collections import namedtuple
    output = namedtuple('Outputs', ['scalar', 'model'])
    return output(scalar, model)




@dsl.pipeline(name='pipeline-with-importer')
def pipeline_with_importer():

    importer1 = importer(
        artifact_uri='gs://ml-pipeline-playground/shakespeare1.txt',
        artifact_class=Dataset,
        reimport=False)
    train(dataset=importer1.output)



if __name__ == "__main__":
    # execute only if run as a script
    compiler.Compiler().compile(
        pipeline_func=pipeline_with_importer,
        package_path='pipeline_with_importer.json'
    )


