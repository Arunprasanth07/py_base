// pipeline {
//   agent any
//   options { timestamps() }

//   stages {
//     stage('Checkout') {
//       steps { checkout scm }
//     }
//     stage('Install Dependencies') {
//       steps { bat 'npm ci' }
//     }
//     stage('Run Testim Suite') {
//       steps {
//         withCredentials([string(credentialsId: 'TESTIM_TOKEN', variable: 'TESTIM_TOKEN')]) {
//           bat '''
//             npx -y @testim/testim-cli testim ^
//               --token "%TESTIM_TOKEN%" ^
//               --project "usw23BAJHoKZwqT8pHir81ZX" ^
//               --use-local-chrome-driver ^
//               --user "OfxKgEkfQ3tkh8uGiyTc" ^
//               --mode "selenium" ^
//               --branch "main" ^
//               --test-plan "Wallet_transaction" ^
//               --test-config "FHD 1920x1080"
//           '''
//         }
//       }
//     }
//   }

//   post {
//     always {
//       archiveArtifacts artifacts: '**/test-results/**/*.*, **/*.log', allowEmptyArchive: true
//     }
//   }
// }


pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Checkout (SCM-backed)') {
      steps {
        // 'checkout scm' works only for Pipeline-from-SCM jobs (which you now use)
        checkout scm
      }
    }

    stage('Sanity: Env & Tools') {
      steps {
        bat '''
          echo === NODE & NPM VERSIONS ===
          node -v
          npm -v
          echo.
          echo === WHERE Binaries ===
          where node
          where npm
          where npx
          echo.
          echo === PATH ===
          echo %PATH%
          echo.
          echo === Chrome Presence (optional) ===
          where chrome || echo Chrome not found on PATH
          "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --version || echo Chrome.exe not found at default path
          echo.
          echo === NPM REGISTRY/PROXY (if corporate network) ===
          npm config get proxy
          npm config get https-proxy
          npm config get registry
        '''
      }
    }

    stage('Run Testim (multi-strategy)') {
      environment {
        // flip this to 'grid' if local Chrome is not available or flaky
        TESTIM_RUN_TARGET = 'local'   // 'local' or 'grid'
      }
      steps {
        withCredentials([string(credentialsId: 'TESTIM_TOKEN', variable: 'TESTIM_TOKEN')]) {
          // Try NPX first, then NPM EXEC, then global install + PATH fix.
          bat '''
            setlocal ENABLEDELAYEDEXPANSION
            echo ==== START TESTIM RUN ====
            set TESTIM_ARGS=--token "%TESTIM_TOKEN%" --project "usw23BAJHoKZwqT8pHir81ZX" --branch "main" --test-plan "Wallet_transaction" --test-config "FHD 1920x1080"

            if /I "%TESTIM_RUN_TARGET%"=="local" (
              set TESTIM_ARGS=%TESTIM_ARGS% --mode "selenium" --use-local-chrome-driver
              echo Running with LOCAL Chrome driver...
            ) else (
              set TESTIM_ARGS=%TESTIM_ARGS% --grid "Testim-Grid" --mode "selenium"
              echo Running on TESTIM GRID...
            )

            echo.
            echo === Attempt 1: npx ===
            npx -y @testim/testim-cli testim %TESTIM_ARGS%
            if %ERRORLEVEL%==0 goto :done

            echo.
            echo === Attempt 2: npm exec ===
            npm exec -y @testim/testim-cli testim %TESTIM_ARGS%
            if %ERRORLEVEL%==0 goto :done

            echo.
            echo === Attempt 3: global install + PATH fix ===
            npm i -g @testim/testim-cli
            REM Add SYSTEM user global npm bin to PATH for this step
            set "PATH=C:\\Windows\\system32\\config\\systemprofile\\AppData\\Roaming\\npm;%PATH%"
            where testim
            testim %TESTIM_ARGS%
            if %ERRORLEVEL%==0 goto :done

            echo.
            echo *** ALL ATTEMPTS FAILED ***
            echo If network is restricted, set npm proxy:
            echo   npm config set proxy http://USER:PASS@HOST:PORT
            echo   npm config set https-proxy http://USER:PASS@HOST:PORT
            echo Or switch TESTIM_RUN_TARGET=grid to avoid local Chrome.
            exit /b 1

            :done
            echo ==== TESTIM RUN COMPLETE ====
            endlocal
          '''
        }
      }
    }
  }

  post {
    always {
      // stash whatever output you have (adjust patterns if you emit reports)
      archiveArtifacts artifacts: '**/*.log, **/test-results/**/*.*', allowEmptyArchive: true
    }
    failure {
      echo '❌ Pipeline failed. Check the "Sanity: Env & Tools" stage and Testim attempts.'
    }
    success {
      echo '✅ Pipeline passed.'
    }
  }
}
