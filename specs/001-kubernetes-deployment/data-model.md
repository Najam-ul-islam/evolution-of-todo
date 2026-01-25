# Data Model: Local Kubernetes Deployment (Cloud-Native Todo Chatbot)

**Date**: 2026-01-24
**Feature**: 001-kubernetes-deployment

## Overview
This document describes the data structures and configurations used in the Kubernetes deployment of the Todo Chatbot application. Since this is an infrastructure feature, the "data model" consists of configuration schemas and deployment descriptors.

## Kubernetes Resource Definitions

### Deployment Configuration
- **Entity**: DeploymentSpec
- **Fields**:
  - replicas: integer (desired number of pod instances)
  - selector: object (label selector for pods)
  - template: object (pod template specification)
    - metadata: object (pod metadata)
    - spec: object (pod specification)
      - containers: array (container definitions)
        - name: string (container name)
        - image: string (container image reference)
        - ports: array (port mappings)
        - env: array (environment variables)
        - resources: object (resource limits and requests)

### Service Configuration
- **Entity**: ServiceSpec
- **Fields**:
  - selector: object (selector to match pods)
  - ports: array (service port definitions)
    - port: integer (service port)
    - targetPort: integer (target port on pod)
    - protocol: string (protocol type, e.g., TCP)
  - type: string (service type: ClusterIP, NodePort, LoadBalancer)

### ConfigMap Configuration
- **Entity**: ConfigMapData
- **Fields**:
  - data: object (key-value pairs of configuration data)
    - key: string (configuration key)
    - value: string (configuration value)

## Helm Chart Structure

### Chart Metadata
- **Entity**: ChartYaml
- **Fields**:
  - name: string (chart name)
  - version: string (chart version)
  - description: string (chart description)
  - apiVersion: string (Helm API version)
  - appVersion: string (application version)

### Values Schema
- **Entity**: HelmValues
- **Fields**:
  - replicaCount: integer (number of pod replicas)
  - image:
    - repository: string (image repository)
    - tag: string (image tag)
    - pullPolicy: string (pull policy)
  - service:
    - type: string (service type)
    - port: integer (service port)
  - resources: object (resource constraints)
  - nodeSelector: object (node selection constraints)
  - tolerations: array (toleration specifications)
  - affinity: object (affinity/anti-affinity constraints)

## Docker Build Configuration

### Dockerfile Parameters
- **Entity**: DockerBuildArgs
- **Fields**:
  - BASE_IMAGE: string (base image for multi-stage builds)
  - BUILD_ARGS: object (build-time variables)
  - WORKDIR: string (working directory in container)
  - EXPOSE: array (ports to expose)
  - HEALTHCHECK: string (health check command)

## Environment Configuration

### Application Settings
- **Entity**: AppEnvironment
- **Fields**:
  - BACKEND_URL: string (URL for backend API)
  - DATABASE_URL: string (connection string for database)
  - LOG_LEVEL: string (logging verbosity level)
  - PORT: integer (application port)

## Kubernetes Secrets Schema
- **Entity**: SecretData
- **Fields**:
  - data: object (base64 encoded secret data)
  - stringData: object (plaintext secret data)
  - type: string (secret type)

## Ingress Configuration
- **Entity**: IngressSpec
- **Fields**:
  - rules: array (routing rules)
    - host: string (hostname)
    - http: object (HTTP routing)
      - paths: array (path-based routing)
        - path: string (URL path)
        - backend: object (backend service)
          - serviceName: string (service name)
          - servicePort: integer (service port)