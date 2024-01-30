# Step1 : Generate Data
In this part, a series of synthetic data is created through the **generator.py** file and must be placed in an API endpoint that will be given to the next steps for data processing.

## generator.py🪢
The **generator.py** script simulates financial data and sends it to an API endpoint. It generates stock prices, order book data, news sentiment, market data, and economic indicators. The script uses a single core to ensure maximum performance.

1. Define Sample Stock Symbols:
The script defines a list of sample stock symbols (AAPL, GOOGL, AMZN, MSFT, TSLA) that will be used to generate data.

2. Define API Endpoint:
The script defines the API endpoint ("http://localhost:5000/ingest") where the generated data will be sent.

3. Generate Stock Price Data:
The generate_data() function generates stock price data for a randomly selected stock symbol. It uses a random walk model to simulate price movements.

4. Generate Additional Data Types:
The generate_additional_data() function generates additional data types, such as order book data, news sentiment, market data, and economic indicators.

5. Send Data to API:
The send_data() function sends the generated data to the API endpoint in JSON format.
## Preparing the Python Application for Deployment 🪡
instead of using API endpoint, we can use Flask application:
```
from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def get_data():
    data = generate_additional_data()
    return jsonify(data)
```
The Flask application, on the other hand, is used to expose the data for direct consumption. The @app.route("/") decorator defines a GET endpoint that will return the generated data in JSON format. This endpoint can be accessed by sending a GET request to the URL http://localhost:5000.

## manager.sh🎛️
To run generator.py file and manage it, we need this file.

The**manager.sh** script is a Bash script that helps manage the producer, including initializing, starting, and stopping it.
Define Virtual Environment Directory:
The VENV_DIR variable defines the directory where the virtual environment will be created. In this case, it's named venv.

Define Python Script Name:
The SCRIPT_NAME variable defines the name of the Python script to run, which is **generator.py** in this case.

- **init() Function:**
This function initializes the project by creating a virtual environment (venv) if it doesn't exist, activating the virtual environment, installing the necessary dependencies from requirements.txt, and displaying a completion message.
```
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r requirements.txt
```
- **start() Function:**
This function starts the Python script, generator.py, by activating the virtual environment if it's not already activated, running the script with the '&' operator to run it in the background, and displaying a start message.
```
  echo "Starting $SCRIPT_NAME..."
  python $SCRIPT_NAME &
```
- **stop() Function:**
This function stops the Python script, generator.py, by using pkill -f to kill any running instances of the script.
```
pkill -f $SCRIPT_NAME
```
## Run🔧
So,run this instruction in the terminal :
```
cd ./home/***/project
./manager.sh init
#activating the virtual environment

./manager.sh start
# Run generator.py

./manager.sh stop
#stop generator.py
```
# Docker 🪄
**1. Packaging the Application as a Docker Image**🎁

A Dockerfile contains instructions for building a Docker image, which facilitates a consistent and reproducible environment for Kubernetes deployment.
```
FROM python:3.7-slim-buster

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY generator.py .

CMD ["python", "generator.py"]
EXPOSE 5000
```
It sets up a Python environment, copies requirements.txt and generator.py to /app, installs the required packages, and specifies the command to run the Flask app on port 5000.
**2. Pushing the Image to a Container Registry**🚌
Build the Docker image with the following command:
```
$ sudo docker build -t generateDate .
```
Tag the Docker image using the following command:
```
$ sudo docker tag generateDate localhost:5001/generateDate
$ sudo docker push localhost:5001/generateDate
```
run docker
```
sudo docker run -p 5000:5000 localhost:5001/generateDate:latest
```
**verify:**

docker image ls

**3. Install MetalLB**🐋
 We use metalLB for load balancing.
> MetalLB is a networking service for Kubernetes that allows you to point multiple pods in a Kubernetes cluster to a single domain name or IP. MetalLB uses several types of loopbacks and spokes to distribute traffic to pods.

**install Helm**
```
wget https://get.helm.sh/helm-v3.13.3-linux-arm64.tar.gz
tar -zxvf  helm-v3.13.3-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
```
**install metalLB**
```
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb
```
**4. Deploying the Python Application in Kubernetes**🕹️
To run your Flask application in Kubernetes, you need to create a deployment. A deployment is defined in a YAML file and specifies details like the Docker image for the application, the number of replicas, and other settings. In Kubernetes, a deployment manages a set of identical pods, where each pod represents a single instance of a running process in a cluster.
```
apiVersion: apps/v1
kind: Deployment
metadata:
 name: generatorDate-deployment
spec:
 replicas: 3 # Set the desired number of replicas (pods) for your application
 selector:
  matchLabels:
   app: generateDate
 template:
  metadata:
   labels:
    app: generateDate
  spec:
   containers:
   - name: generateDate
     image: localhost:5001/generateDate # Replace with your actual Docker image name
     ports:
     - containerPort: 5000
```
**Run the kubectl command to apply the deployment**
```
kubectl create deployment generatorDate-server --image=localhost:5001/generateDate:latest
kubectl port-forward <pod_name> 5000:5000

# stop and remove deployment
kubectl delete pod <pod_name>
kubectl delete deployment generatorDate-server
```
**5. Exposing the Deployment as a Service**🧮
To make the Flask app accessible from outside the Kubernetes cluster, create a service to expose the deployment.

In Kubernetes, a service is an abstraction layer that enables communication between a set of pods and external clients. It provides a stable IP address and DNS name for a set of pods, so that other pods or external clients can reliably access the application running in the pod. A service can have different types, such as ClusterIP, NodePort, and LoadBalancer.
```
apiVersion: v1
kind: Service
metadata:
  name: generateDate-service
  labels:
    app: generateDate
spec:
  type: LoadBalancer
  selector:
    app: generateDate
  ports:
    - port: 5000
      protocol: TCP
      targetPort: 5000
```
**Run the kubectl command to apply the service**
$kubectl apply -f generateDate-service.yaml
**6. running all manifests and checking result**⛓️
```
$kubectl apply -f kubernetes/
$kubectl get service generateDate-service
```
This command returns the external IP address of the LoadBalancer service. You can use it to access the Flask REST API from a web browser or HTTP client outside the Kubernetes cluster.
**7. result**🎥
```
http://<EXTERNAL_IP_ADDRESS>:80
```
