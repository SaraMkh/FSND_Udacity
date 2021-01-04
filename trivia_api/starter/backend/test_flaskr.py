import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    # add a timporory dtabase here
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
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
    Write at least one test for each test for successful
     operation and for expected errors.
    """

    def test_get_categories(self):
        """Test categories page """
        responsei = self.client().get('/categories')
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """Test questions page """
        responsei = self.client().get('/questions')
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['totalQuestions'], 10)
        self.assertEqual(data['currentCategory'], '')
        self.assertTrue(data['categories'])

    def beyond_valid_page(self):
        """Test beyond valid page """
        responsei = self.client().get('/questions?page=10000')
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resourse not found')

    def test_delete_questions(self):
        """Test delete questions operation"""
        responsei = self.client().delete('/questions/14')
        data = json.loads(responsei.data)
        question = Question.query.filter(Question.id == 14).first()
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "The question Deleted Successfully")
        self.assertEqual(question, None)

    def test_valid_delete_questions(self):
        """Test valid delete questions operation"""
        responsei = self.client().delete('/questions/1000')
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

    def test_create_questions(self):
        """Test create questions operation"""
        newquestion = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 3,
            'category': 2,
        }
        responsei = self.client().post('/questions', json=newquestion)
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'], "The question Created Successfully")

    def test_valid_create_questions(self):
        """Test valid create questions operation"""
        newquestion = {
            'question': '',
            'answer': '',
            'difficulty': 0,
            'category': 0,
        }
        responsei = self.client().post('/questions/50', json=newquestion)
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Method Not Allowed')

    def test_search_questions(self):
        """Test search questions operation"""
        searchTerm = {'searchTerm': 'title'}
        responsei = self.client().post('/questions/search', json=searchTerm)
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['Total_questions'])

    def test_valid_search_questions(self):
        """Test valid search questions operation"""
        searchTerm = {'searchTerm': '45634654fgh56456'}
        responsei = self.client().post('/questions/search', json=searchTerm)
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Internal Server Error')

    def test_search_categories(self):
        """Test search categories operation"""
        # try the categories id =1
        responsei = self.client().get('/categories/1/questions')
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        # becouse the total questions in "categories id =1 " are equal to 4

        self.assertEqual(data['Total_questions'], 4)
        self.assertTrue(data['currentCategory'])

    def test_valid_search_categories(self):
        """Test valid search categories operation"""
        # try the categories id =765
        responsei = self.client().get('/categories/765/questions')
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

    def test_play_quizzes(self):
        """Test play quizzes"""
        # try the categories id = 2
        quizzes = {
            'previous_questions': [16, 17],
            'quiz_category': {
                'type': 'Art',
                'id': 2
            }
        }
        responsei = self.client().post('/quizzes', json=quizzes)
        data = json.loads(responsei.data)
        """Test search categories operation"""
        self.assertEqual(responsei.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        # make sure that there are id 2 in quiz_category
        self.assertEqual(data['quiz_category']['id'], 2)
        # make sure that there are id 16 , 17 in prevoise questions
        self.assertNotEqual(data['question']['id'], 16)
        self.assertNotEqual(data['question']['id'], 17)

    def test_play_valid_quizzes(self):
        """Test play valid quizzes"""
        # try the categories id =2
        quizzes = {
            'previous_questions': [40, 50],
            'quiz_category': {
                'type': 'Computer Science',
                'id': 12
            }
        }
        responsei = self.client().post('/quizzes', json=quizzes)
        data = json.loads(responsei.data)
        """Test search categories operation"""
        data = json.loads(responsei.data)
        self.assertEqual(responsei.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()