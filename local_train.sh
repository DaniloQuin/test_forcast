
#Local train
 gcloud ml-engine local train \
  --package-path trainer_codes/ \
  --module-name trainer_codes.task \
  --job-dir "output/" \
  -- \

export MODEL_NAME="modelo_test_1"
export REGION="us-central1"
export BUCKET="gs://backup-test1"
export JSON_INSTANCES="request.json"
export SAVED_MODEL_PATH="/home/dsepulveda/test_cloud_python/output/keras_export/1556259590"

gcloud ml-engine models create $MODEL_NAME \
 --regions $REGION


gcloud ml-engine versions create v1 \
  --model $MODEL_NAME \
  --staging-bucket $BUCKET \
  --origin $SAVED_MODEL_PATH

gcloud ml-engine predict \
    --model $MODEL_NAME \
    --version v1 \
    --json-instances $JSON_INSTANCES

