PROJECT = fast-aing
DOCKER_PORT = 8081
CONTAINER_IMAGE = slmest
RUN_NAME = slmer
RUN_MEM = 2Gi

default:
	gcloud config set project ${PROJECT}

build_base: default
	gcloud builds submit --tag gcr.io/${PROJECT}/base_slm --timeout=1000s base_image

build_hello:
	gcloud builds submit --tag gcr.io/${PROJECT}/hello_run --timeout=1000s hello_image

build_app: default
	gcloud builds submit --config app_image/cloudbuild.yaml --timeout=1000s app_image

deploy_hello: default
	gcloud alpha run deploy hellorun \
	--image gcr.io/${PROJECT}/hello_run:latest \
	--region us-central1 \

deploy_app: default
	gcloud beta run deploy ${RUN_NAME} \
	--image gcr.io/${PROJECT}/${CONTAINER_IMAGE}:latest \
	--memory ${RUN_MEM} \
	--region us-central1 \
	--platform managed


# jupyter lab commands: client side
#ZONE = us-central1-a
ZONE = us-east1-c
INSTANCE_NAME = fastai-instance
INSTANCE_TYPE = n1-highmem-8
IMAGE_FAMILY = pytorch-latest-gpu
ACCELERATOR = nvidia-tesla-t4
ACCELERATOR_COUNT = 1

vm: default
	gcloud compute instances start --zone ${ZONE} ${INSTANCE_NAME}

lab: default
	xdg-open http://localhost:8080
	gcloud compute ssh --zone ${ZONE} ${INSTANCE_NAME} -- -L 8080:localhost:8080

stop: default
	gcloud compute instances stop --zone ${ZONE} ${INSTANCE_NAME}

deploy_lab: default
	gcloud compute instances create ${INSTANCE_NAME} \
	--zone=${ZONE} \
	--image-family=${IMAGE_FAMILY} \
	--image-project=deeplearning-platform-release \
	--maintenance-policy=TERMINATE \
	--accelerator="type=${ACCELERATOR},count=${ACCELERATOR_COUNT}" \
	--machine-type=${INSTANCE_TYPE} \
	--boot-disk-size=30GB \
	--metadata="install-nvidia-driver=True" \

upload:
	gsutil cp fine_tuned/export.pkl gs://fastai-nlp/fine_tuned


# docker
pull: default
	gcloud auth configure-docker
	docker pull gcr.io/${PROJECT}/${CONTAINER_IMAGE}:latest

lab_dock: default
	xdg-open http://localhost:${DOCKER_PORT}
	gcloud compute ssh --zone ${ZONE} ${INSTANCE_NAME} -- -L ${DOCKER_PORT}:localhost:${DOCKER_PORT}

local_dock:
	docker run -p ${DOCKER_PORT}:8080 -e PORT=8080 gcr.io/${PROJECT}/${CONTAINER_IMAGE}:latest

shell:
	docker run -it gcr.io/${PROJECT}/${CONTAINER_IMAGE}:latest sh


gcloud_update:
	sudo apt-get update && sudo apt-get --only-upgrade install kubectl \
	google-cloud-sdk google-cloud-sdk-app-engine-grpc google-cloud-sdk-pubsub-emulator \
	google-cloud-sdk-app-engine-go google-cloud-sdk-cloud-build-local \
	google-cloud-sdk-datastore-emulator google-cloud-sdk-app-engine-python \
	google-cloud-sdk-cbt google-cloud-sdk-bigtable-emulator \
	google-cloud-sdk-app-engine-python-extras google-cloud-sdk-datalab \
	google-cloud-sdk-app-engine-java
