# ML Model Deployment Using AWS EC2 and ECR

This repository provides a comprehensive guide for deploying an ML model using Docker, GitHub Actions, and AWS services (EC2 and ECR). By following the steps outlined below, you can set up a seamless CI/CD pipeline and host your application on AWS.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Prepare the Docker Image](#step-1-prepare-the-docker-image)
- [Step 2: Build and Run the Docker Image](#step-2-build-and-run-the-docker-image)
- [Step 3: Configure CI/CD Workflow in GitHub](#step-3-configure-cicd-workflow-in-github)
- [Step 4: Push Code to GitHub](#step-4-push-code-to-github)
- [Step 5: Create an IAM User in AWS](#step-5-create-an-iam-user-in-aws)
- [Step 6: Create a Private Repository in ECR](#step-6-create-a-private-repository-in-ecr)
- [Step 7: Launch an EC2 Instance](#step-7-launch-an-ec2-instance)
- [Step 8: Install Docker on EC2](#step-8-install-docker-on-ec2)
- [Step 9: Configure GitHub Self-Hosted Runner on EC2](#step-9-configure-github-self-hosted-runner-on-ec2)
- [Step 10: Integrate GitHub Actions with AWS](#step-10-integrate-github-actions-with-aws)
- [Step 11: Configure EC2 Security Group](#step-11-configure-ec2-security-group)
- [Step 12: Execute the CI/CD Workflow](#step-12-execute-the-cicd-workflow)
- [Step 13: Test and Validate Deployment](#step-13-test-and-validate-deployment)

## Prerequisites
Before proceeding, ensure you have:
- A GitHub repository for your project.
- An AWS account with permissions for EC2 and ECR.
- AWS CLI installed and configured.
- Docker installed locally.

## Step 1: Prepare the Docker Image
Create a `Dockerfile` with the following content:

```dockerfile
FROM python:3.12.7-slim
WORKDIR /app
COPY . /app/
RUN apt-get update -y && apt-get install -y awscli
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python3", "app.py"]
```

## Step 2: Build and Run the Docker Image
Build and run the Docker container locally to test:
```sh
docker build -t awspoc .
docker run -d -p 5000:5000 awspoc
```

## Step 3: Configure CI/CD Workflow in GitHub
1. Navigate to the **Actions** tab in your GitHub repository.
2. Select **Deploy to Amazon ECS** workflow and configure it.
3. Add the following GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `ECR_REPOSITORY_NAME`
   - `AWS_ECR_LOGIN_URI`
4. Set up the workflow to:
   - Build and test the Docker image.
   - Push the image to ECR.
   - Deploy to EC2 using a self-hosted runner.

## Step 4: Push Code to GitHub
```sh
git add .
git commit -m "Add Dockerfile and CI/CD workflow"
git push origin main
```

## Step 5: Create an IAM User in AWS
1. Open the **IAM Console**.
2. Create a new user with programmatic access.
3. Attach permissions for EC2 and ECR.
4. Generate an access key and secret key.

## Step 6: Create a Private Repository in ECR
1. Open the **ECR Console**.
2. Create a new private repository and note its URL.

## Step 7: Launch an EC2 Instance
1. Open the **EC2 Console**.
2. Launch an Ubuntu-based instance.
3. Connect to the instance using SSH.

## Step 8: Install Docker on EC2
Run the following commands on your EC2 instance:
```sh
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

## Step 9: Configure GitHub Self-Hosted Runner on EC2
```sh
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.308.0/actions-runner-linux-x64-2.308.0.tar.gz
tar xzf actions-runner-linux-x64.tar.gz
./config.sh --url https://github.com/<owner>/<repository> --token <your_token>
./run.sh
```
Replace `<owner>`, `<repository>`, and `<your_token>` with your actual GitHub details.

## Step 10: Integrate GitHub Actions with AWS
Store the required AWS secrets in the **GitHub repository**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REPOSITORY_NAME`
- `AWS_ECR_LOGIN_URI`

## Step 11: Configure EC2 Security Group
1. Go to the **EC2 Console**.
2. Edit the security group attached to your instance.
3. Add an inbound rule to allow traffic on port 5000.

## Step 12: Execute the CI/CD Workflow
Push changes to GitHub to trigger the workflow. The workflow will:
1. Build the Docker image.
2. Push it to ECR.
3. Deploy the container on EC2.

## Step 13: Test and Validate Deployment
Access your application using the **EC2 public IP** or domain:
```sh
http://<EC2_PUBLIC_IP>:5000
```

## Summary
This guide outlines how to deploy an ML model using Docker, GitHub Actions, and AWS services. By following these steps, you can achieve a fully automated CI/CD pipeline and deploy your ML model efficiently on AWS EC2.

## Author
[Gaurav Shrivastava]

## License
This project is licensed under the MIT License.

