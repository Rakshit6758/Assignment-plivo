pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE = 'rakshitkapoor2345/message_service'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-credentials'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh 'python -m unittest discover -s app/tests'
                    }
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        docker.image(DOCKER_IMAGE).push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f kubernetes/deployment.yaml'
                    sh 'kubectl apply -f kubernetes/service.yaml'
                    sh 'kubectl apply -f kubernetes/ingress.yaml'
                    sh 'kubectl apply -f kubernetes/prometheus-monitor.yaml'
                    sh 'kubectl apply -f kubernetes/fluentd-config.yaml'
                    sh 'kubectl apply -f kubernetes/fluentd-daemonset.yaml'
                    sh 'kubectl apply -f kubernetes/mysql-statefulset.yaml'
                    sh 'kubectl apply -f kubernetes/hpa.yaml'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
