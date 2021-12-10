# Kubernetes Message Forum

Message forum created using Python3, MongoDB, Jinja2, MetalLB, and Metrics Server.

## Downloading files
```
git clone https://github.com/aarole/k8s-message-board.git
cd k8s-message-board/
```

## Setting up Metrics Server
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Verify that Metrics Server is running
```
kubectl get pods -n kube-system
```

## Setup MetalLB
```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.11.0/manifests/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.11.0/manifests/metallb.yaml
```

Create ConfigMap to configure MetalLB.
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
      - 192.168.10.2-192.168.10.10
```

Apply ConfigMap.
```
kubectl apply -f /path/to/configmap.yaml
```

## Configure MongoDB
### Create PersistentVolume and PersistentVolumeClaim
```
kubectl apply -f ./mongo/pv.yaml
kubectl apply -f ./mongo/pvc.yaml
```

### Create Deployment and Service
```
kubectl apply -f ./mongo/deployment.yaml
kubectl apply -f ./mongo/service.yaml
```

## Configure Flask App
### Create Deployment
```
kubectl apply -f ./flask/deployment.yaml
```

### Create Service
```
kubectl apply -f ./flask/service.yaml
```

### Create Ingress
```
kubectl apply -f ./flask/ingress.yaml
```

### Create HPA
```
kubectl apply -f ./flask/hpa.yaml
```

## Access Flask App
Get the external IP assigned to the LoadBalancer.
```
kubectl get svc flask-svc
```

Access the application using a browser.
```
http://LOADBALANCER_EXTERNAL_IP
```