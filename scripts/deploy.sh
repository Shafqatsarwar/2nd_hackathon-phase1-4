#!/bin/bash

# Deployment script for The Evolution of Todo - Phase IV
# This script automates the deployment of the Todo application to Kubernetes

set -e  # Exit on any error

echo "🚀 Starting deployment of The Evolution of Todo - Phase IV"

# Function to check if required tools are installed
check_dependencies() {
    echo "🔍 Checking dependencies..."

    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl is not installed. Please install kubectl and try again."
        exit 1
    fi

    if ! command -v helm &> /dev/null; then
        echo "❌ helm is not installed. Please install helm and try again."
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        echo "❌ docker is not installed. Please install docker and try again."
        exit 1
    fi

    echo "✅ All dependencies are installed"
}

# Function to build Docker images
build_images() {
    echo "🏗️ Building Docker images..."

    # Build backend image
    echo "📦 Building backend image..."
    docker build -f Dockerfile.backend -t todo-backend:latest .

    # Build frontend image
    echo "📦 Building frontend image..."
    docker build -f Dockerfile.frontend -t todo-frontend:latest .

    echo "✅ Docker images built successfully"
}

# Function to create Kubernetes secrets
create_secrets() {
    echo "🔐 Creating Kubernetes secrets..."

    # Check if secrets already exist, if not create them
    if ! kubectl get secret todo-app-secrets &> /dev/null; then
        kubectl create secret generic todo-app-secrets \
            --from-literal=DATABASE_URL="$DATABASE_URL" \
            --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
            --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"
        echo "✅ Secrets created successfully"
    else
        echo "⚠️ Secrets already exist, skipping creation"
    fi
}

# Function to deploy to Kubernetes using Helm
deploy_helm() {
    echo "🚢 Deploying to Kubernetes using Helm..."

    # Navigate to helm chart directory
    cd helm-chart

    # Check if release already exists
    if helm list | grep -q "todo-release"; then
        echo "🔄 Upgrading existing release..."
        helm upgrade todo-release .
    else
        echo "🚀 Installing new release..."
        helm install todo-release .
    fi

    cd ..

    echo "✅ Helm deployment completed"
}

# Function to verify deployment
verify_deployment() {
    echo "🔍 Verifying deployment..."

    echo "⏳ Waiting for deployments to be ready..."
    kubectl rollout status deployment/todo-release-backend -n default
    kubectl rollout status deployment/todo-release-frontend -n default

    echo "📋 Checking pods status..."
    kubectl get pods

    echo "📋 Checking services..."
    kubectl get services

    echo "✅ Deployment verification completed"
}

# Function to display deployment info
display_info() {
    echo "🌐 Deployment Information:"
    echo ""
    echo "Backend Service: $(kubectl get svc todo-release-backend-service -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')"
    echo "Frontend Service: $(kubectl get svc todo-release-frontend-service -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}')"
    echo ""
    echo "To access services locally, use:"
    echo "kubectl port-forward svc/todo-release-frontend-service 3000:3000"
    echo "kubectl port-forward svc/todo-release-backend-service 8000:8000"
    echo ""
    echo "For ingress access (if configured):"
    echo "Frontend: http://todo-app.local"
    echo "Backend: http://todo-app.local/api/"
}

# Main deployment flow
main() {
    echo "🎯 Starting deployment process..."

    # Check dependencies
    check_dependencies

    # Build Docker images
    build_images

    # Create secrets
    create_secrets

    # Deploy using Helm
    deploy_helm

    # Verify deployment
    verify_deployment

    # Display information
    display_info

    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "🔧 You can now access your application"
}

# Parse command line arguments
case "$1" in
    build)
        build_images
        ;;
    secrets)
        create_secrets
        ;;
    deploy)
        deploy_helm
        verify_deployment
        display_info
        ;;
    verify)
        verify_deployment
        display_info
        ;;
    *)
        main
        ;;
esac