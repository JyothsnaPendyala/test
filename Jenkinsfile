pipeline{
    agent any

    stages{
        
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
        
       
    }
        post{
       
        always {
            archiveArtifacts artifacts: 'bank_term_deposit_prediction_clean_data.csv', onlyIfSuccessful: true
        }
            }
}
