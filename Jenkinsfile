pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Checkout (SCM-backed)') {
      steps {
        checkout scm
      }
    }

    stage('Sanity: Env & Tools') {
      steps {
        bat '''
          echo === NODE and NPM VERSIONS ===
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
          if exist "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" (
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --version
          ) else (
            echo Chrome.exe not found at default path
          )
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
        TESTIM_RUN_TARGET = 'local'   // set to 'grid' if local Chrome is not available
      }
      steps {
        withCredentials([string(credentialsId: 'TESTIM_TOKEN', variable: 'TESTIM_TOKEN')]) {
          bat '''
            if "%TESTIM_TOKEN%"=="" (
              echo [ERROR] TESTIM_TOKEN is empty or missing. Ensure a Secret text credential with ID TESTIM_TOKEN exists.
              exit /b 1
            )

            setlocal ENABLEDELAYEDEXPANSION
            echo ==== START TESTIM RUN ====
            set TESTIM_ARGS=--token "%TESTIM_TOKEN%" --project "usw23BAJHoKZwqT8pHir81ZX" --branch "main" --test-plan "Wallet_transaction" --test-config "FHD 1920x1080"

            if /I "%TESTIM_RUN_TARGET%"=="local" (
              set TESTIM_ARGS=!TESTIM_ARGS! --mode "selenium" --use-local-chrome-driver
              echo Running with LOCAL Chrome driver...
            ) else (
              set TESTIM_ARGS=!TESTIM_ARGS! --grid "Testim-Grid" --mode "selenium"
              echo Running on TESTIM GRID...
            )

            echo.
            echo === Attempt 1: npx ===
            npx -y @testim/testim-cli testim !TESTIM_ARGS!
            if !ERRORLEVEL!==0 goto :done

            echo.
            echo === Attempt 2: npm exec ===
            npm exec -y @testim/testim-cli testim !TESTIM_ARGS!
            if !ERRORLEVEL!==0 goto :done

            echo.
            echo === Attempt 3: global install + PATH fix ===
            npm i -g @testim/testim-cli
            set "PATH=C:\\Windows\\system32\\config\\systemprofile\\AppData\\Roaming\\npm;%PATH%"
            where testim
            testim !TESTIM_ARGS!
            if !ERRORLEVEL!==0 goto :done

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
