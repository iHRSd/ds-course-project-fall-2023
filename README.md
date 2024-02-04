# Distributed-Systems-Project
Developing a Real-Time Financial Analysis &amp; Trading System

In this project, we have to process financial data in real time.

## Tools ⚙

- Ubuntu 22.04 focal
- Docker
- Kubernetes
- metalLB
- flask
- python libraries
 ## sketch 🧩 
 There are 4 steps to implement this project:

**1.Data Generation:**
- generates simulated financial data.
- use load balancing
- send data to **Data Ingestion**

**2. Data Ingestion &stream processing**
- receives the simulated data
- validates it
- use kafka for real time stream processing
- send data to **Processing**

**3.Processing:**
- calculates the mandatory trading indicators
- generates real-time trading signals.

![diagram](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/diagram.drawio.svg)


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
bash manager.sh init
#activating the virtual environment

bash manager.sh start
# Run generator.py

bash manager.sh stop
#stop generator.py
```
![manager.sh_code](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-01-30%20154618.png)
# Docker 🪄

**1. Packaging the Application as a Docker Image**🎁

A Dockerfile contains instructions for building a Docker image, which facilitates a consistent and reproducible environment for Kubernetes deployment.
```
FROM python:3.8.10
sudo docker build -t generatedate .
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY generator.py .

CMD ["python", "generator.py"]
EXPOSE 5000
```
It sets up a Python environment, copies requirements.txt and generator.py to /app, installs the required packages, and specifies the command to run the Flask app on port 5000.

**2. Pushing the Image to a Container Registry** 🚌

Build the Docker image with the following command:
```
sudo docker build -t generatedate .
```
![build_docker_image](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-01-31%20190901.png)

Tag the Docker image using the following command:
```
sudo docker tag generatedate localhost:5100/generatedate
```
```
sudo docker push localhost:5100/generatedate
```
run docker
```
sudo docker run -p 5000:5000 localhost:5100/generatedate
```
![build_container](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-01-31%20192109.png)
**verify:**

docker image ls

![output_container](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-01-31%20192031.png)

**3. Install minikube and MetalLB** 🐋

To install the latest minikube stable release on x86-64 Linux using binary download:
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Install kubectl binary with curl on Linux:
Download the latest release with the command:
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

Validate the binary (optional), Download the kubectl checksum file:
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
```
Validate the kubectl binary against the checksum file:
```
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```
If valid, the output is:
```
kubectl: OK
```

Install kubectl:
```
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
Test to ensure the version you installed is up-to-date:
```
kubectl version --client
```

 We use metalLB for load balancing.
> MetalLB is a networking service for Kubernetes that allows you to point multiple pods in a Kubernetes cluster to a single domain name or IP. MetalLB uses several types of loopbacks and spokes to distribute traffic to pods.

**install metalLB**

go to the [metalLB](https://github.com/metallb/metallb/blob/main/config/manifests/metallb-native.yaml) and download metallb-native.yaml .

and run this:
```
minikube start --driver=docker
````

````
kubectl apply -f metallb-native.yaml
````


![build_container](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-01%20193015.png)

**4. Deploying the Python Application in Kubernetes**🕹️

To run your Flask application in Kubernetes, you need to create a deployment. A deployment is defined in a YAML file and specifies details like the Docker image for the application, the number of replicas, and other settings. In Kubernetes, a deployment manages a set of identical pods, where each pod represents a single instance of a running process in a cluster.
```
apiVersion: apps/v1
kind: Deployment
metadata:
 name: generatordate-deployment
spec:
 replicas: 3 # Set the desired number of replicas (pods) for your application
 selector:
  matchLabels:
   app: generatedate
 template:
  metadata:
   labels:
    app: generatedate
  spec:
   containers:
   - name: generatedate
     image: localhost:5000/generatedate # Replace with your actual Docker image name
     ports:
     - containerPort: 5000
```

**Run the kubectl command to apply the deployment**
```
kubectl create deployment generatordate-server --image=localhost:5100/generatedate:latest
```
![generatedate-server](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-01%20194151.png)

**verify**
```
kubectl get pods
```

![get pods](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-01%20194705.png)


**activating metalLB addon**
After start minikube, we must activate the metallb addon. To view all the available addons, run this command:

```
minikube addons list
```
![addon list](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20134823.png)

> Addons are activated with minikube addons enable:

![metallb active](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20135516.png)


**stop and remove deployment**
```
kubectl delete pod <pod_name>
kubectl delete deployment generatordate-server
```

![remove](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20151200.png)

**5. Exposing the Deployment as a Service**🧮

To make the Flask app accessible from outside the Kubernetes cluster, create a service to expose the deployment.

In Kubernetes, a service is an abstraction layer that enables communication between a set of pods and external clients. It provides a stable IP address and DNS name for a set of pods, so that other pods or external clients can reliably access the application running in the pod. A service can have different types, such as ClusterIP, NodePort, and LoadBalancer.
```
apiVersion: v1
kind: Service
metadata:
  name: generatedate-service
spec:
  type: LoadBalancer
  selector:
    app: generatedate
  sessionAffinity: None
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  ports:
  - name: generatedate
    protocol: TCP
    port: 5000
    targetPort: 5000
    # If you set the `spec.type` field to `NodePort` and you want a specific port number,
    # you can specify a value in the `spec.ports[*].nodePort` field.
   
```

**6. Create metallb config file** Ⓜ️

Next you need to create ConfigMap, which includes an IP address range for the load balancer. The pool of IPs must be dedicated to MetalLB's use.

> You can't reuse for example the Kubernetes node IPs or IPs controlled by other services.

```
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - <ip-address-range-start>-<ip-address-range-stop>
```


**7. running all manifests and checking result**⛓️

```
$kubectl apply -f mykube/
```

![apply](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20152818.png)

```
$kubectl get service generatedate-service
```

This command returns the external IP address of the LoadBalancer service. You can use it to access the Flask REST API from a web browser or HTTP client outside the Kubernetes cluster.

**8. result**🎥

```
http://<EXTERNAL_IP_ADDRESS>:
```
for result, minikube ip is 172.18.0.1 and docker ip is 172.17.0.1. So , when we go to the minikube ssh and "crul 172.18.0.1", we can see result(dataset) :

![result](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-03%20215257.png)


![Screenshot 2024-02-03 220225](https://github.com/iHRSd/ds-course-project-fall-2023/assets/156912661/0e8c9258-e396-4bba-b3b9-b10e56c0dd1e)


# Step2 : Ingestion and stream processing 📼

for processing data in realtime, we need stream processing services like : apache kafka,apache spark ... .
we use apache kafka.
we need to pull a Kafka image and integrate it into this setup for real-time data processing.

## Deploying Kafka in Minikube:

**1. Pull the Kafka Docker Image:**

```
docker pull confluentinc/cp-kafka:latest
```

![pull kafka](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20182816.png)

**2. Create a Kafka Deployment:**

Create a kafka-deployment.yaml file with the following content:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      containers:
      - name: kafka
        image: confluentinc/cp-kafka:latest
        ports:
        - containerPort: 9092
          name: kafka
        env:
        - name: KAFKA_ZOOKEEPER_CONNECT
          value: zookeeper:2181
        - name: KAFKA_METRICS_REPORTER_ENABLED
          value: true
        - name: KAFKA_METRICS_REPORTER_INTERVAL_MS
          value: 30000
        livenessProbe:
          tcpSocket:
            port: 9092
          initialDelaySeconds: 15
          periodSeconds: 20
          successThreshold: 1
          timeoutSeconds: 5
        readinessProbe:
          tcpSocket:
            port: 9092
          initialDelaySeconds: 15
          periodSeconds: 20
          successThreshold: 1
          timeoutSeconds: 5
```

**3. Create a Kafka Service:**

Create a kafka-service.yaml file with the following content:


```
apiVersion: v1
kind: Service
metadata:
  name: kafka
spec:
  selector:
    app: kafka
  ports:
  - port: 9092
    targetPort: 9092
  type: NodePort
```

**4. Apply the Deployments:**

```
kubectl apply -f kafka/
```

![apply kafka](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20184052.png)

**result**🎥

![result](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/images/Screenshot%202024-02-02%20184209.png)


**5. Deploying Kafka Connect:**

Ensure to update the BOOTSTRAP_SERVERS environment variable in the deployment to point to Kafka service:
```
- name: BOOTSTRAP_SERVERS
  value: http://kafka:9092
```
according to this command ,we must update generator.py .
we create [generator-update.py](https://github.com/iHRSd/ds-course-project-fall-2023/blob/main/generator-update.py)

and for this file we use confluent_kafka library,that we run this command:
```
pip install confluent-kafka
```

in dockerfile ,generator.py file is included in docker image via COPY instructions:
> COPY generator.py .

```diff
+  you'll need to rebuild your Docker image.
```
⚠️Don't forget to update dockerfile with new app file:
> COPY generator-update.py .

# Step3 : process ⚒️

Now, we can processes the data by calculating financial indicators.
Indicators are:
> Moving Average (MA)
> Exponential Moving Average (EMA)
> Relative Strength Index (RSI).

so for this instruction,we get data from kafka and process them by calculating financial.then we can show it:
1.wrtie kafka consumer for get data:

```
from kafka import KafkaConsumer
import pandas as pd

consumer = KafkaConsumer('my_topic',
                         bootstrap_servers=['kafka_broker:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=False,
                         group_id='my_group_id',
                         value_deserializer=lambda x: x.decode('utf-8')
                        )

for message in consumer:
    data = message.value.decode("utf-8")
    df = pd.read_json(data)
    print("Received data: ", df.head())
```

2.write calculation functions
3.write Kafka Producer to get result and show in broker:

```
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["kafka_broker:9092"]
)

producer.send("topic_name", value="Hello, World!".encode("utf-8"))
```

## team 🎭
- [Hamidreza SayyadDaryabakhsh](https://github.com/iHRSd)
- [Rozhina Ghiasi](https://github.com/Rozh-Zizigoloo)
## References📑

- [Source](https://github.com/Msiavashi/ds-course-project-fall-2023)
- [Deploying a Python Application with Kubernetes](https://komodor.com/blog/deploying-a-python-application-with-kubernetes/)
- [Using Flask to Build a Simple API](https://betterprogramming.pub/setting-up-a-simple-api-b3b00bc026b4)
- [metallb config file](https://docs.k0sproject.io/v1.23.6+k0s.2/examples/metallb-loadbalancer/)
- [kafka config](https://medium.com/@ramjoshi.blogs/stream-processing-with-python-and-apache-kafka-a-beginners-guide-3f01a373cd6f)
