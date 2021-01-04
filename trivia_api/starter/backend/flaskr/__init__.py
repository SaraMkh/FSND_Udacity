import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    paginated_questions = formatted_questions[start:end]
    return paginated_questions


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
      @TODO:
      Use the after_request decorator to set Access-Control-Allow
    '''


    @app.after_request
    def after_request(response):
            response.headers.add(
                'Access-Control-Allow-Headers',
                'Content-Type,Authorization,true')
            response.headers.add(
                'Access-Control-Allow-Methods',
                'GET,PATCH,POST,DELETE,OPTIONS')
            return response
            '''
              @TODO:
              Create an endpoint to handle GET requests
              for all available categories.
            '''


    @app.route('/categories', methods=['GET'])
    def get_categories():
            try:
                # get all available categories
                categories = Category.query.all()
                categories_Type = {}
                # create array to build the categories_type list
                for categoryi in categories:
                    categories_Type[categoryi.id] = categoryi.type
                return jsonify({
                  'success': True,
                  'categories': categories_Type
                }), 200
            except:
                abort(500)
    '''
      @TODO:
      Create an endpoint to handle GET requests for questions,
      including pagination (every 10 questions).
      This endpoint should return a list of questions,
      number of total questions, current category, categories.

      TEST: At this point, when you start the application
      you should see questions and categories generated,
      ten questions per page and pagination
      at the bottom of the screen for three pages.
      Clicking on the page numbers should update the questions.
    '''


    @app.route('/questions', methods=['GET'])
    def get_questions():
            # get all available categories
            categories = Category.query.all()
            categories_Type = {}
            # create array to build the categories_type list
            for categoryi in categories:
                    categories_Type[categoryi.id] = categoryi.type
                    currentCategory = ''
            # get all available questions
            questions = Question.query.all()
            # paginate all available questions
            paginate_questions_list = paginate_questions(request, questions)
            paginate_questions_len = len(paginate_questions_list)
            if (paginate_questions_len == 0):
                    abort(404)
            return jsonify({
              'success': True,
              'questions': paginate_questions_list,
              'totalQuestions': paginate_questions_len,
              'currentCategory':  currentCategory,
              'categories':  categories_Type
            }), 200
    '''
      @TODO:
      Create an endpoint to DELETE question using a question ID.

      TEST: When you click the trash icon next to a question,
      the question will be removed.
      This removal will persist in the database and when you refresh the page.
    '''


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
            try:
                    # get question with the id =question_id
                    question = Question.query.filter(
                            Question.id == question_id
                            ).first()
                    if question is None:
                        abort(404)
                    question.delete()
                    # selection = Question.query.order_by(Question.id).all()
                    # current_questions=paginate_questions(request,selection)
                    return jsonify({
                            'success': True,
                            'message': "The question Deleted Successfully"
                            }), 200
            except:
                abort(500)
    '''
      @TODO:
      Create an endpoint to POST a new question,
      which will require the question and answer text,
      category, and difficulty score.

      TEST: When you submit a question on the "Add" tab,
      the form will clear and the question will appear at the end of the last page
      of the questions list in the "List" tab.
    '''


    @app.route('/questions', methods=['POST'])
    def create_questions():
            # get all the entered data to create the new question
            body = request.get_json()
            new_question = body.get('question', None)
            new_answer_text = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty_score = body.get('difficulty', None)

            try:
                    # start creating the new question
                    question = Question(
                            question=new_question, answer=new_answer_text,
                            category=new_category, difficulty=new_difficulty_score
                            )
                    question.insert()
                    # selection = Question.query.order_by(Question.id).all()
                    # current_questions=paginate_questions(request,selection)

                    return jsonify({
                            'success': True,
                            'message': "The question Created Successfully"
                            }), 200
            except:
                    abort(500)
    '''
      @TODO:
      Create a POST endpoint to get questions based on a search term.
      It should return any questions for whom the search term
      is a substring of the question.

      TEST: Search by any phrase. The questions list will update to include
      only question that include that string within their question.
      Try using the word "title" to start.
    '''


    @app.route('/questions/search', methods=['POST'])
    def search_questions():
            # get the searchTerm to look for the simalrity
            currentCategory = ''
            question_list = {}
            body = request.get_json()
            search_words = body.get('searchTerm', None)
            search_words = str(search_words).lower()

            if body is None or search_words == ' ':
                abort(422)
            else:
                try:
                    # search if the searchterm  is a substring of any question.
                    results = Question.query.filter(
                            Question.question.ilike(f'%{search_words}%')
                            ).all()
                    if results is None or len(results) == 0:
                        abort(404)
                    else:
                        questions = paginate_questions(request, results)
                        return jsonify({
                          'success': True,
                          'questions': questions,
                          'Total_questions': len(results),
                          'currentCategory': currentCategory
                        }), 200
                except:
                    abort(500)
    '''
      @TODO:
      Create a GET endpoint to get questions based on category.

      TEST: In the "List" tab / main screen, clicking on one of the
      categories in the left column will cause only questions of that
      category to be shown.
    '''


    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def search_questions_by_category_id(id):
            # get the category_id to look for the simalrity
            category_id = id
            try:
                question_list = {}
                if category_id is None:
                    abort(422)
                else:
                    # search if there any questions has a category id= category_id.
                    results = Question.query.filter(
                            Question.category == category_id
                            ).all()
                    currentCategory = Category.query.filter(
                            Category.id == category_id
                            ).first()
                    if results is None:
                        abort(404)
                    else:
                        questions = paginate_questions(request, results)
                        return jsonify({
                          'success': True,
                          'questions': questions,
                          'Total_questions': len(results),
                          'currentCategory': currentCategory.type
                        }), 200
            except:
                abort(500)

    '''
      @TODO:
      Create a POST endpoint to get questions to play the quiz.
      This endpoint should take category and previous question parameters
      and return a random questions within the given category,
      if provided, and that is not one of the previous questions.

      TEST: In the "Play" tab, after a user selects "All" or a category,
      one question at a time is displayed, the user is allowed to answer
      and shown whether they were correct or not.
    '''


    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
            # get the previous_questions and
            # quiz_category_id to guess the next  question
            question_list = {}
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            quiz_category_id = quiz_category.get('id', None)
            if body is None:
                abort(400)
            else:
                try:
                  if quiz_category_id['id'] == 0:
                    results = Question.query.all()
                  else:
                    if previous_questions is None:
                        '''
                        search if there any questions
                        has a category id= quiz_category_id
                        only becouse there no quizzes before.
                        '''
                        results = Question.query.filter(
                                    Question.category == quiz_category_id
                                    ).all()
                    else:
                        '''
                        search if there any questions has a
                        category id= quiz_category_id but
                        not one of the previous_questions.
                        '''
                        results = Question.query.filter(
                                Question.category == quiz_category_id,
                                Question.id.notin_(previous_questions)
                                ).all()
                  currentCategory = Category.query.filter(
                          Category.id == quiz_category_id
                          ).first()
                  if results is None:
                      abort(404)
                  else:
                      # return a random questions within the given category
                      questionI = secrets.choice(results)
                      return jsonify({
                        'success': True,
                        'question': questionI
                      }), 200
                except:
                    abort(500)
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': '404',
          'message': 'Not Found'
        }), 404


    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
          'success': False,
          'error': '422',
          'message': 'Unprocessable Entity'
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'success': False,
          'error': '400',
          'message': 'Bad Request '
        }), 400


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
          'success': False,
          'error': '405',
          'message': 'Method Not Allowed'
        }), 405


    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({
          'success': False,
          'error': '500',
          'message': 'Internal Server Error'
        }), 500

    return app

