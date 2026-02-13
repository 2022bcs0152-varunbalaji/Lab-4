pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "svarunbalaji2022bcs0152/wine-api:latest"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/2022bcs0152-varunbalaji/Lab-4.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python scripts/train.py 
                echo "Name: Varun Balaji"
                echo "Roll No: 2022BCS0152"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_PASS')]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u svarunbalaji2022bcs0152 --password-stdin
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }
    }
}
