import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from config import database_setup
from sqlalchemy import desc

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('postgres', '','localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', '', 'localhost:5432', self.database_name)
        
        setup_db(self.app, self.database_path)

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
#----------------------------------------------------------------------------#
# Test # 1 GET /categories
#----------------------------------------------------------------------------#  
    def test_get_categories(self):
        # Response for specific route
        res = self.client().get('/categories')
        # Load the data
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        
    def test_405_post_categories(self):
        """Wrong method POST"""
        res = self.client().post('/categories')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)
#----------------------------------------------------------------------------#
# Test # 2 GET /questions?page=1
#----------------------------------------------------------------------------#
    def test_get_questions_per_page(self):
        # Response for specific route
        res = self.client().get('/questions?page=2',json={'category:': 'art'})
        # Load the data
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_not_valid_page(self):
        res = self.client().get('/books?page=500',json={'category:': 'science'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#----------------------------------------------------------------------------#
# Test # 2 POST /questions
#----------------------------------------------------------------------------#
    def test_create_new_question(self):
        new_question = {
            'question': 'Question #1 ?',
            'answer': 'Answer #1',
            'category': '3',
            'difficulty': 4
        }

        res = self.client().post('/questions', json= new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
 
    def test_400_create_new_question(self):
        new_question = {
            'question': None,
            'answer': 'Answer #1',
            'category': '3',
            'difficulty': 4
        }

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Question/ Answer can not be blank')
#----------------------------------------------------------------------------#
# Test # 3 POST /questions/search
#----------------------------------------------------------------------------#
    def test_search_questions(self):
        search = {
            'searchTerm': 'ancient Egyptians'
        } 

        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_search_questions(self):
        search = {
            'searchTerm': 'Kuwait'
        } 
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No questions contains found.')
#----------------------------------------------------------------------------#
# Tests #4 GET /categories/<string:category_id>/questions
#----------------------------------------------------------------------------#
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_400_get_questions_by_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No questions with category id found.')     
#----------------------------------------------------------------------------#
# Tests #5 POST /quizzes
#----------------------------------------------------------------------------#
    def test_play_quiz_with_category(self):
        quiz_data = {
            'previous_questions': [17, 18, 19],
            'quiz_category': {
                'type': 'Art',
                'id': '2'
            }
        }
        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['id']not in quiz_data['previous_questions'])
        
    def test_400_play_quiz_with_category(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Please provide quiz data.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
