# Quickstart Guide: Local Kubernetes Deployment (Cloud-Native Todo Chatbot)

**Date**: 2026-01-24
**Feature**: 001-kubernetes-deployment

## Overview
This guide provides step-by-step instructions to deploy the Todo Chatbot application to a local Kubernetes cluster using Minikube and Helm charts with AI-assisted DevOps tools.

## Prerequisites
- Docker Desktop (version 4.53 or higher) with Docker AI Agent (Gordon) enabled
- Minikube installed and configured
- kubectl installed and configured
- Helm 3.x installed
- kubectl-ai plugin installed
- kagent installed
- Git

## Environment Setup

### 1. Verify Prerequisites
```bash
# Check Docker version and status
docker --version
docker ps

# Check Minikube version and status
minikube version
minikube status

# Check kubectl connection
kubectl version --client
kubectl cluster-info

# Check Helm installation
helm version

# Check AI tools availability
kubectl ai version
kagent version
```

### 2. Start Minikube Cluster
```bash
# Start Minikube with sufficient resources for the Todo Chatbot application
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Verify cluster is ready
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Enable ingress addon for external access
minikube addons enable ingress
```

## Application Containerization

### 3. Prepare Application Code
```bash
# Clone or navigate to the Todo Chatbot application directory
cd /path/to/todo-chatbot-application

# Verify application structure (should have frontend and backend directories)
ls -la
```

### 4. Generate Dockerfiles using AI Agent (Gordon)
```bash
# Navigate to frontend directory
cd frontend

# Use Docker AI Agent to generate optimized Dockerfile
# NOTE: Commands will vary based on Gordon's specific interface
# Typically involves: Right-click in Docker Desktop UI -> "Ask Gordon" -> "Create Dockerfile"
# Or using Docker CLI with AI features if available

# Example for manual creation (if Gordon is unavailable):
cat > Dockerfile << EOF
# Use official Node.js runtime as base image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/build ./build
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
EOF

# Navigate to backend directory
cd ../backend

# Generate backend Dockerfile using AI Agent or manually:
cat > Dockerfile << EOF
# Use official Python runtime as base image
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "main.py"]
EOF
```

### 5. Build Docker Images
```bash
# Build frontend image
docker build -t todo-chatbot-frontend:v1.0.0 ./frontend

# Build backend image
docker build -t todo-chatbot-backend:v1.0.0 ./backend

# Verify images exist
docker images | grep todo-chatbot
```

## Helm Chart Creation

### 6. Create Helm Charts using AI Tools
```bash
# Create charts directory
mkdir -p charts

# Create frontend chart
helm create charts/todo-chatbot-frontend

# Create backend chart
helm create charts/todo-chatbot-backend

# Clean up default templates
rm -rf charts/todo-chatbot-frontend/templates/*
rm -rf charts/todo-chatbot-backend/templates/*
```

### 7. Generate Frontend Templates using kubectl-ai
```bash
# Create frontend deployment template
cat > charts/todo-chatbot-frontend/templates/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot-frontend.fullname" . }}
  labels:
    {{- include "todo-chatbot-frontend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot-frontend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "todo-chatbot-frontend.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
EOF

# Create frontend service template
cat > charts/todo-chatbot-frontend/templates/service.yaml << EOF
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot-frontend.fullname" . }}
  labels:
    {{- include "todo-chatbot-frontend.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chatbot-frontend.selectorLabels" . | nindent 4 }}
EOF

# Create frontend ingress template
cat > charts/todo-chatbot-frontend/templates/ingress.yaml << EOF
{{- if .Values.ingress.enabled -}}
{{- \$fullName := include "todo-chatbot-frontend.fullname" . -}}
{{- \$svcPort := .Values.service.port -}}
{{- if and .Values.ingress.className (not (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion)) }}
  {{- if not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class") }}
  {{- \$_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className}}
  {{- end }}
{{- end }}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ \$fullName }}
  labels:
    {{- include "todo-chatbot-frontend.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ \$fullName }}
                port:
                  number: {{ \$svcPort }}
              {{- else }}
              serviceName: {{ \$fullName }}
              servicePort: {{ \$svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
  {{- with .Values.ingress.tls }}
  tls:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
EOF
```

### 8. Generate Backend Templates using kubectl-ai
```bash
# Create backend deployment template
cat > charts/todo-chatbot-backend/templates/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot-backend.fullname" . }}
  labels:
    {{- include "todo-chatbot-backend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot-backend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "todo-chatbot-backend.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-chatbot-backend.fullname" . }}-db-secret
                  key: database-url
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
EOF

# Create backend service template
cat > charts/todo-chatbot-backend/templates/service.yaml << EOF
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot-backend.fullname" . }}
  labels:
    {{- include "todo-chatbot-backend.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chatbot-backend.selectorLabels" . | nindent 4 }}
EOF

# Create backend configmap template
cat > charts/todo-chatbot-backend/templates/configmap.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-chatbot-backend.fullname" . }}-config
data:
  app-config.yaml: |
    database:
      host: localhost
      port: 5432
      name: todo_db
    logging:
      level: info
EOF

# Create backend secret template
cat > charts/todo-chatbot-backend/templates/secret.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-chatbot-backend.fullname" . }}-db-secret
type: Opaque
data:
  database-url: {{ .Values.database.url | b64enc | quote }}
EOF
```

### 9. Update Values Files
```bash
# Update frontend values
cat > charts/todo-chatbot-frontend/values.yaml << EOF
# Default values for todo-chatbot-frontend.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: todo-chatbot-frontend
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "v1.0.0"

service:
  type: ClusterIP
  port: 3000

ingress:
  enabled: true
  className: ""
  annotations:
    {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: todo-chatbot.local
      paths:
        - path: /
          pathType: Prefix
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
EOF

# Update backend values
cat > charts/todo-chatbot-backend/values.yaml << EOF
# Default values for todo-chatbot-backend.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: todo-chatbot-backend
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "v1.0.0"

service:
  type: ClusterIP
  port: 8000

database:
  url: "postgresql://user:password@localhost:5432/todo_db"

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
EOF
```

### 10. Validate Helm Charts
```bash
# Validate frontend chart
helm lint charts/todo-chatbot-frontend

# Validate backend chart
helm lint charts/todo-chatbot-backend

# Template and inspect the generated manifests
helm template dev-frontend charts/todo-chatbot-frontend
helm template dev-backend charts/todo-chatbot-backend
```

## Application Deployment

### 11. Load Images into Minikube
```bash
# Load images into Minikube's container runtime
minikube image load todo-chatbot-frontend:v1.0.0
minikube image load todo-chatbot-backend:v1.0.0

# Verify images are loaded
minikube ssh docker images | grep todo-chatbot
```

### 12. Deploy Backend First
```bash
# Deploy backend using Helm
helm install todo-chatbot-backend charts/todo-chatbot-backend --namespace default --create-namespace

# Wait for backend to be ready
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=todo-chatbot-backend --timeout=300s
```

### 13. Deploy Frontend
```bash
# Deploy frontend using Helm
helm install todo-chatbot-frontend charts/todo-chatbot-frontend --namespace default

# Wait for frontend to be ready
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=todo-chatbot-frontend --timeout=300s
```

### 14. Verify Deployment
```bash
# Check all pods are running
kubectl get pods

# Check all services are available
kubectl get services

# Check ingress routes
kubectl get ingress

# Test application connectivity
minikube service todo-chatbot-frontend --url
```

## Validation and Testing

### 15. Use AI Tools for Validation
```bash
# Use kubectl-ai to check cluster health
kubectl ai check cluster

# Use kagent for cluster analysis
kagent analyze cluster

# Check pod health
kubectl ai check pods

# Check service connectivity
kubectl ai check service todo-chatbot-frontend
kubectl ai check service todo-chatbot-backend
```

### 16. Access the Application
```bash
# Get the frontend service URL
minikube service todo-chatbot-frontend --url

# Or use ingress if configured
minikube tunnel  # In a separate terminal
# Then access via the ingress hostname (todo-chatbot.local)
```

## Scaling and Management

### 17. Scale Applications
```bash
# Scale frontend replicas using kubectl-ai
kubectl ai scale deployment todo-chatbot-frontend --replicas=3

# Scale backend replicas
kubectl ai scale deployment todo-chatbot-backend --replicas=2
```

### 18. Upgrade Applications
```bash
# Update values file with new image tag
# Then upgrade using Helm
helm upgrade todo-chatbot-frontend charts/todo-chatbot-frontend --set image.tag="v1.0.1"
```

## Cleanup
```bash
# Uninstall applications
helm uninstall todo-chatbot-frontend
helm uninstall todo-chatbot-backend

# Stop minikube
minikube stop

# Optionally delete the cluster
minikube delete
```

## Troubleshooting

### Common Issues:
1. **Images not found**: Ensure images are loaded into minikube with `minikube image load`
2. **Service unavailable**: Check if pods are running with `kubectl get pods`
3. **Ingress not working**: Ensure ingress addon is enabled with `minikube addons enable ingress`
4. **Connection timeouts**: Check resource allocation and increase if needed

### AI-Assisted Debugging:
```bash
# Use kubectl-ai to diagnose issues
kubectl ai explain pod <pod-name>
kubectl ai debug deployment todo-chatbot-frontend
kubectl ai troubleshoot service todo-chatbot-backend
```