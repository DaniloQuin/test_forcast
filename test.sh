
gcloud ml-engine jobs submit training second_job \                                                                                                 dsepulveda@localhost
--module-name trainer_codes.model \
--staging-bucket gs://backup-test1 \
--package-path ./trainer_codes \
--region us-central1
