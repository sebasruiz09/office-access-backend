pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        CODECOV_TOKEN = credentials('codecov-token')
    }

    stages {

        stage('Verificar dependencias') {
            steps {
                sh '''
                    docker --version
                    docker-compose --version
                '''
            }
        }

        stage('Construir contenedores') {
            steps {
                sh 'docker-compose -p ci build'
            }
        }

        stage('Ejecutar pruebas unitarias con coverage') {
            steps {
                sh '''
                    docker-compose -p ci run --rm backend \
                    pytest -v \
                        --cov=backend \
                        --cov-branch \
                        --cov-report=xml:/app/coverage.xml \
                        --cov-report=term-missing
                '''
            }
        }

        stage('Copiar coverage.xml fuera del contenedor') {
            steps {
                sh '''
                    container=$(docker ps -aqf "name=ci_backend")
                    docker cp $container:/app/coverage.xml ./coverage.xml
                '''
            }
        }

        stage('Subir Coverage a Codecov') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh '''
                    curl -Os https://cli.codecov.io/latest/linux/codecov
                    chmod +x codecov
                    ./codecov upload-process -f coverage.xml -t "$CODECOV_TOKEN"
                '''
            }
        }

        stage('Desplegar') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh 'docker-compose -p ci up -d'
            }
        }
    }

    post {
        always {
            sh """
                docker-compose -p ci down --volumes --remove-orphans || true
            """
        }
    }
}

