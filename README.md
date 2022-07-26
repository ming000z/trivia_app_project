# Full Stack API Final Project


## Full Stack Trivia

### Set up Instruction
#### Backend Setup
1. with postgres runnin, create a trivia database
  ```
  createdb trivia
  ```
2. fron the backend folder in terminal, populate the databse using trivia.psql file:
  ```
  cd backend
  psql trivia < trivia.psql
  ```
3. install the required dependencies by navigating to the /backend directory and running:
  ```
  cd backend
  pip install -r requirements.txt
  ```
4. start the backend server
  ```
  cd backend
  export FLASK_APP=flaskr
  export FLASK_ENV=development
  flask run 
  ```
#### Frontend Setup
1. install dependencies
  ```
  cd frontend
  npm install
  ```
2. run the frontend server
  ```
  cd frontend
  npm start
  ```


