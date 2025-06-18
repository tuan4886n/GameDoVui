# 📁 Project Structure – Quiz Game DevOps 🚀

Below is the folder structure of the project along with a brief description of each section.:

C:.
├── .github/workflows/ # Contains CI/CD pipeline with GitHub Actions
├── assets/ # Frontend UI assets
│ ├── css/ # Stylesheets for game UI
│ ├── images/ # Game UI images
│ └── js/ # JavaScript for handling player interactions
├── auth/ # User authentication, using JWT
├── config/ # System configuration & database connection
├── eslint/ # JavaScript debugging & optimization tools
├── help_routes/ # Backend APIs to extend game functionality
├── k8s-manifests/ # Kubernetes manifests to deploy backend on cluster
├── routes/ # Flask's main API, handling requests from frontend
├── terraform-cloudwatch/ # Terraform sets up resource monitoring with AWS CloudWatch
├── terraform-ec2/ # Terraform manages AWS EC2 infrastructure automatically
├── tests/ # Unit tests, testing API with pytest
├── ssh-deploy.sh # automation deploy
