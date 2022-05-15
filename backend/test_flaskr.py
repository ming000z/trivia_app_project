import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "mingzhezhang", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            "answer": "abc",
            "category": 3,
            "difficulty": 1,
            "question": "What's your name?"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))
    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_404_get_questions(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # def test_delete_question(self):
    #     res = self.client().delete("/questions/5")
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 5)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(question, None)
        
    # def test_404_if_question_does_not_exist(self):
    #     res = self.client().delete("/questions/10000")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")    
    
    # def test_create_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(data['questions'])
        
    def test_search_question(self):
        res = self.client().post("/questions", json={"search": "Tim Burton"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data['questions']), 1)
        
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()