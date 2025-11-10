pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install Dependencies') {
      steps { bat 'npm ci' }
    }
    stage('Run Testim Suite') {
      steps {
        withCredentials([string(credentialsId: 'TESTIM_TOKEN', variable: 'TESTIM_TOKEN')]) {
          bat '''
            npx -y @testim/testim-cli testim ^
              --token "%TESTIM_TOKEN%" ^
              --project "usw23BAJHoKZwqT8pHir81ZX" ^
              --use-local-chrome-driver ^
              --user "OfxKgEkfQ3tkh8uGiyTc" ^
              --mode "selenium" ^
              --branch "main" ^
              --test-plan "Wallet_transaction" ^
              --test-config "FHD 1920x1080"
          '''
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: '**/test-results/**/*.*, **/*.log', allowEmptyArchive: true
    }
  }
}
