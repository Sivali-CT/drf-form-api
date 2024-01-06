# Form API
This is solely for demonstration purposes.

![drf](https://res.cloudinary.com/andinianst93/image/upload/v1703884289/Screenshot_from_2023-12-30_04-11-09_kfrpkx.png)

This web application works in conjunction with Next 14 as frontend.

## K8s

### Step 1: Create PV
```bash
apiVersion: v1
kind: PersistentVolume
metadata:
  name: form-pv
  labels:
    type: form
spec:
  capacity:
    storage: 4Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/form_data"
```

### Step 2: Create Statefulsets
```bash
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: form-db
  namespace: development
spec:
  selector:
    matchLabels:
      db: form-db 
  serviceName: "form-db"
  replicas: 1
  minReadySeconds: 10
  template:
    metadata:
      labels:
        db: form-db
    spec:
      terminationGracePeriodSeconds: 10
      nodeSelector:
        db: postgres
      containers:
      - name: form-db
        image: postgres:latest
        ports:
        - containerPort: 5433
          name: form-db
        env:
        - name: POSTGRES_USER 
          value: postgres
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: form-db-secret
              key: password
        - name: POSTGRES_DB
          value: form
        - name: PGDATA
          value: /var/lib/postgresql/data
        volumeMounts:
        - name: form-pvc
          mountPath: /mnt/form_data
  volumeClaimTemplates:
  - metadata:
      name: form-pvc
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 2Gi


---
apiVersion: v1
kind: Service
metadata:
  name: form-db
  namespace: development
  labels:
    app: form-db
spec:
  ports:
    - port: 5433
      name: form-db
  clusterIP: None
  selector:
    db: form-db

```

### Step 4: Create Secret for the DB and Django
```bash
k create secret generic form-secret -n development \
    --from-literal=DJANGO_SECRET_KEY=yourvalue \
    --from-literal=DEBUG=True \
    --from-literal=DJANGO_SUPERUSER_USERNAME=yourvalue \
    --from-literal=DJANGO_SUPERUSER_PASSWORD=yourvalue \
    --from-literal=DJANGO_SUPERUSER_EMAIL=yourvalue \
    --from-literal=POSTGRES_USER=yourvalue \
    --from-literal=POSTGRES_PASSWORD=yourvalue \
    --from-literal=POSTGRES_DB=form \
    --from-literal=POSTGRES_HOST=form-db \
    --from-literal=POSTGRES_PORT=5432

k create secret generic form-db-secret -n development \
    --from-literal=password=yourvalue \
```

### Step 5: Create Deployment

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: form
  labels:
    app: form
  namespace: development
spec:
  replicas: 2
  selector:
    matchLabels:
      tier: backend-form
  template:
    metadata:
      labels:
        tier: backend-form
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: tier
                operator: In
                values:
                - backend
      containers:
      - name: form
        image: svlct/form-demo-drf:v15
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: form-secret
        resources:
          requests:
            cpu: "200m"
            memory: "2Gi"
          limits:
            cpu: "400m"
            memory: "4Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: form
  namespace: development
spec:
  selector:
    tier: backend-form
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
```