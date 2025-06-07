# 🎮 Quiz Game – DevOps Fresher Portfolio

## 🚀 Demo Game

🔗 **Play Now:** [Game Do Vui](https://gamedovui.pages.dev)  
💡 **Experience the challenge!** Answer 15 questions inspired by the show _"Who Wants to Be a Millionaire?"_ and test your knowledge!

---

## 📌 Project Description

**Quiz Game** is a 15-question trivia game inspired by the popular show _"Who Wants to Be a Millionaire?"_.  
This project is more than just a game—it applies **DevOps principles** to optimize deployment automation, cloud infrastructure management, containerization, and system monitoring to ensure smooth cloud operations.

### ✅ **Overview**

- Players can **register, log in, save their scores**, and view **leaderboards**.
- **Flask API** retrieves quiz data from OpenDB and authenticates players using JWT.
- **PostgreSQL (Supabase)** stores scores and rankings for efficient database management.

### ✅ **Project Objectives**

- **Build a complete system** applying DevOps best practices.
- **Automate deployment** using Terraform for easy cloud infrastructure management (EC2 & database).
- **CI/CD pipeline** with GitHub Actions to test, build Docker containers, and deploy the API.
- **Monitor system performance** using AWS CloudWatch to track EC2 health.
- **Containerize backend Flask API**, supporting scalability.
- **Connect frontend with backend** via Cloudflare Pages for speed and security.

🔥 **Key Highlights:**

- The project is not just about **building a quiz game**, but also experimenting with **real-world cloud deployment**, enhancing DevOps skills.
- **All deployment processes are free**, leveraging AWS Free Tier, Cloudflare, and Supabase to minimize costs.

🚀 **Try the game now:** [Game Do Vui](https://gamedovui.pages.dev)

## 🌍 Technologies Used

- **Backend:** Flask API + PostgreSQL (Supabase)
- **Frontend:** JavaScript, HTML, CSS (Deployed on Cloudflare Pages)
- **CI/CD:** GitHub Actions for automated testing & deployment
- **Infrastructure:** AWS EC2 (Hosting Flask API backend)
- **Monitoring:** AWS CloudWatch to track EC2 performance
- **Containerization:** Dockerized Flask API backend
- **Kubernetes (K3s):** Successfully deployed locally, scalable to cloud environments
- **Infrastructure as Code (IaC):** Terraform manages AWS EC2 infrastructure, Supabase database, and CloudWatch monitoring

📌 **Screenshots**  
🔥 (Add gameplay screenshots here)

![](assets/images/screenshot.jpg)

## 📁 Project Structure

Projects are organized into separate folders for easy management:

- **Backend**: Flask API handles game logic.
- **Frontend**: JavaScript, HTML, CSS interface.
- **CI/CD & Infrastructure**: GitHub Actions for automated testing & deployment.
- **Kubernetes**: Configuration files to deploy backend on K3s.

🔥 **More details 👉 [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)**

## 📌 Database & Frontend Hosting

The system uses [Cloudflare Pages](https://developers.cloudflare.com/pages) for hosting the frontend and [Supabase](https://supabase.com/docs/guides/database) for managing the PostgreSQL database.

✅ **Frontend** – Deployed for free on Cloudflare Pages, ensuring fast performance and global CDN distribution.  
✅ **Database** – Supabase manages PostgreSQL with **RESTful APIs**, offering real-time capabilities and secure queries.

📌 **Setting up the `.env` file**  
Before running the project, create a `.env` file and configure the database connection according to your environment.

📌 **A sample `.env.example` file is provided**, which you can use as a reference to set up your own `.env`:

```env
DATABASE_URL=postgresql://postgres:your_password@your_host:your_port/your_database
DATABASE_HOST=your_host
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_database
```

## 🚀 CI/CD Pipeline – Automated Testing & Deployment

The CI/CD system utilizes **GitHub Actions**, including:

- **ci.yml** – Performs code validation, security checks, builds containers, verifies database connections, and tests APIs.
- **deploy.yml** – Manages server deployment, pushes Docker image to Docker Hub, and provisions AWS EC2 for the Flask backend.

### ✅ **Deployment Process:**

1️⃣ **Build & Push Docker Image:**

- The workflow **logs into Docker Hub**, **builds the Flask API image**, and **pushes it to Docker Hub** (`tuan4886/flask-api:latest`).
  🔗 **Docker Hub Image:** [tuan4886/flask-api:latest](https://hub.docker.com/r/tuan4886/flask-api)

2️⃣ **Provision AWS EC2:**

- Terraform applies infrastructure changes, ensuring the backend is deployed properly.

🔥 **For more details, check the `.github/workflows/` directory.**

## 🔹 Setup & Run the Project

### ✅ **Pre-requisites**

Ensure the following dependencies are installed before proceeding:

- **Python** → Install Python ([Download](https://www.python.org/downloads/)) & dependencies (`pip install -r requirements.txt`)
- **Docker** → Install Docker & Docker Compose ([Download](https://docs.docker.com/get-docker/))
- **Terraform** → Install Terraform ([Download](https://developer.hashicorp.com/terraform/downloads))
- **AWS CLI** → Configure AWS credentials (`aws configure`)

### ✅ **Start Flask Backend**

Run the Flask API using:

```bash
python app.py
```

🔹 Access API at: `http://your-local-ip:8080`

### ✅ Start Frontend Locally

If you want to test the frontend before deployment, run a local HTTP server:

```bash
python -m http.server 8080
```

🔹 Access the frontend at: `http://localhost:8080/`

### ✅ **Deploy Containers with Docker**

Initialize Docker containers to run the **Flask backend** (not frontend):

```bash
docker-compose up -d
```

🔹 The Flask API runs inside a container, eliminating manual startup.

### ✅ **Provision AWS Infrastructure with Terraform**

Execute Terraform to set up **AWS EC2 for the Flask backend** (frontend is hosted separately):

```bash
terraform apply -auto-approve
```

🔹 Once deployment is complete, the API will be accessible at: `http://your-ec2-ip:8080`.

## 🏗️ Kubernetes Deployment

Although this project primarily runs in **Docker**, Kubernetes manifests (`deployment.yaml`, `service.yaml`, `ingress.yaml`) are included to demonstrate container orchestration and scalability best practices.

### ✅ **Kubernetes Configuration Files**

- `deployment.yaml` → Defines how the Flask API is deployed within Kubernetes pods.
- `service.yaml` → Manages internal networking between pods.
- `ingress.yaml` → Configures external access to the API.

### ✅ **Local Kubernetes Deployment (K3s)**

Apply the Kubernetes configuration using the following commands:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

🔹 Verify system status:

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
```

💡 These Kubernetes manifests provide a foundation for future scalability and cloud-based deployment strategies.

## 📊 **AWS CloudWatch – System Monitoring for EC2**

### 🔍 **Overview**

The system utilizes **AWS CloudWatch** for real-time EC2 performance monitoring, automatic alerts, and log storage for analysis.

✅ **CloudWatch Log Group** → Stores **Flask API logs** (`flask-api-log-group`), allowing debugging and system analysis (**retains logs for 5 days**).  
✅ **IAM Role for EC2** → EC2 is granted permissions via `CloudWatchEC2Role`, manually attached via the AWS Console (not automated in Terraform).  
✅ **High CPU Alarm** → If **EC2 CPU exceeds 80% for 5 minutes**, the system triggers **EC2-High-CPU Alarm**, sending alerts via SNS.  
✅ **CloudWatch Dashboard** → Provides real-time visualization of **CPU, Network, and Disk Usage,** displaying alarms for easier monitoring.

### 📌 **How to Access the CloudWatch Dashboard**

To monitor EC2 performance and track alerts:

1️⃣ **Go to AWS CloudWatch Console**  
2️⃣ Navigate to **Dashboards** → Search for `DevOps-EC2-Monitoring`  
3️⃣ Monitor **CPU, Network, Disk Usage,** and view alerts when resource thresholds are exceeded.

🔥 **CloudWatch helps optimize resources, detect anomalies early, and maintain system reliability.**

## 🎯 **Conclusion**

This project showcases **core DevOps practices**, integrating **automation, cloud deployment, monitoring, and containerization** into a practical implementation.

- **Cloud infrastructure** provisioned using Terraform for AWS EC2.
- **Automated testing and deployment** via GitHub Actions.
- **Containerized architecture** with Docker, ensuring flexibility.
- **Cloud monitoring** implemented through AWS CloudWatch for real-time insights.

This project applies **key DevOps practices** to improve **deployment efficiency and system reliability.** By integrating **automation, cloud infrastructure, monitoring, and containerization,** it demonstrates how DevOps can streamline software deployment and operations.
