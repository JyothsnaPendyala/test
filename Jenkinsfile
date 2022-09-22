pipeline{
    agent any

    stages{
        stage("Checkout"){
            steps{
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'ef70b0d3-000a-4c42-a98f-d2c045e33251', url: 'https://github.com/JyothsnaPendyala/bank-term-deposit-prediction.git']]])
            }
        }
        stage("build"){
            steps{
                git branch: 'main', credentialsId: 'ef70b0d3-000a-4c42-a98f-d2c045e33251', url: 'https://github.com/JyothsnaPendyala/bank-term-deposit-prediction.git'
            }
        }
        stage("load_data"){
            steps{
                sh 'python3 load_data.py'
            }
        }
        stage("data_analysis"){
            steps{
                sh 'python3 data_analysis.py'
            }
        }
        stage("feature_engineering"){
            steps{
                sh 'python3 feature_engineering.py'
            }
        }
        stage("data_preprocess"){
            steps{
                sh 'python3 data_preprocess.py'
            }
        }
        stage("model_selection"){
            steps{
                sh 'python3 model_selection.py'
            }
        }
        
    }
    post{
       
        always {
            archiveArtifacts artifacts: 'finalised_model.pkl', onlyIfSuccessful: true
        }
    }
    
    stage('artifacts to s3'){
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'deploytos3', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
                sh "aws s3 ls"
                sh "aws s3 mb s3://mlops-storage1"
                sh "aws s3 cp addressbook_main/target/finalised_model.pkl s3://mlops-storage1"


}
