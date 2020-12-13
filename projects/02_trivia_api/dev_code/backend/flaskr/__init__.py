#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from logging import error
import os
from flask import Flask, request, abort, jsonify
from flask.globals import session 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (func,
                        inspect)
from flask_cors import CORS
import random
from sqlalchemy.sql.elements import Null
from models import (setup_db, Question, Category)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
#----------------------------------------------------------------------------#
# Constants
#----------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10
db = SQLAlchemy()
#----------------------------------------------------------------------------#
# New Functions
#----------------------------------------------------------------------------#
'''
Questions Format
Parameters: query of selected questions
Return: List of questions formated as defined in models.py file
'''
def format_questions(selection):
    questions_formt = [Question.format() for Question in selection]
    return questions_formt

'''
Categories Format
Parameters: query of selected categories
Return: List of categories formated as defined in models.py file
'''
def format_categories(selection):
   categories_formt = [Category.format() for Category in selection]
   return categories_formt

'''
Paginate Questions
Parameters: HTTP request, query of selected questions 
Return: Questions formated in list max (QUESTIONS_PER_PAGE) questions per page
'''
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = format_questions(selection)
    paginated_questions = questions[start:end]

    return paginated_questions

'''
Display Error Default Description Msgs
Parameters: error code, error default description
Return: err_default_desc default error text if not description available
'''
def get_err_msg(error, err_default_desc):
    try:
      return error.description["message"]
    except TypeError:
      return err_default_desc
#----------------------------------------------------------------------------#
# API Setup
#----------------------------------------------------------------------------#
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app) #, resources={r"*/api/*": {'origins': '*'}})
       
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response
  
#----------------------------------------------------------------------------#
# Endpoints / Routes
#----------------------------------------------------------------------------#
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    selection = Category.query.order_by(Category.id).all() 
      
    if len(selection) == 0:
      abort(404)
         
    return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in selection }
    })
  '''
  TEST: GET /categories
        Pass: test_get_categories
        Fail: test_405_post_categories
  '''
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions(): 
    selection = Question.query.order_by(Question.id).all()
    
    current_questions = paginate_questions(request, selection)
    
    categories = Category.query.order_by(Category.id).all()
      
    if len(selection) == 0:
          abort(404)

    
    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_category': None,
        'categories': {category.id: category.type for category in categories}
    })
  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  '''
  TEST: GET /questions
        Pass: test_get_questions_per_page
        Fail: test_404_sent_requesting_not_valid_page
  '''
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
          abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
          'success': True,
          'deleted:': question_id,
          'questions': current_questions,
          'total_questions': len(selection)
      })
    except:
      abort(422)
  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  '''
  TEST: GET /questions
        Pass: test_get_questions_per_page
        Fail: test_404_sent_requesting_not_valid_page
  '''
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
  
    if (new_question is None) or (new_answer is None):
      abort(400, {'message': 'Question/ Answer can not be blank'})  
      
    try:
        question = Question(question=new_question, answer=new_answer, category=new_category,
                          difficulty=new_difficulty)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)


        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(selection)
            
          })
    except:
      db.session.rollback()
      abort(400)
    finally:
      db.session.close()

  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  TEST: POST /questions
        Pass: test_create_new_question
        Fail: test_400_create_new_question
  '''
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search = body.get('searchTerm', None)
    
    selection = Question.query.order_by(Question.id).filter(
        Question.question.ilike('%{}%'.format(search))).all()

    if len(selection) == 0:
        # abort(404, {'message': 'No questions contains "{}" found.'.format(search)})
        abort(404, {'message': 'No questions contains found.' })
    else:   
      current_questions = paginate_questions(request, selection)
      categories = Category.query.all()
      current_categories = format_categories(categories)
      
      return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection),
          'current_category': current_categories
        })
  '''
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  '''
  TEST: POST /questions/search
        Pass: test_search_questions
        Fail: test_404_search_questions
  '''
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  '''
  @app.route('/categories/<string:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    selection = (Question.query
                   .filter(Question.category == category_id)
                   .order_by(Question.id)
                   .all())
      
    current_questions = paginate_questions(request, selection)
    current_category = Category.query.filter(
        Category.id == int(category_id)).all()
    if len(selection) == 0:
      # abort(400, {'message': 'No questions with category {} found.'.format(category_id)})
      abort(400, {'message': 'No questions with category id found.'})

    if current_questions is None:
      abort(404, {'message': 'No questions in selected page.'})
      
    return jsonify({
    'success': True,
    'questions': current_questions,
    'total_questions': len(selection),
        'current_category': {category.id: category.type for category in current_category}
                })

  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  '''
  TEST: GET /categories/<string:category_id>/questions
        Pass: test_get_questions_by_category
        Fail: test_400_get_questions_by_category
  '''
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    
    body = request.get_json()
    
    if not body:
      abort(400, {'message': 'Please provide quiz data.'})
      
    previous_questions = body.get('previous_questions', None)
    current_category = body.get('current_category', None)
    
    if not previous_questions:
      if current_category:
        # if no previous questions is given, but category given then get any question from this category.
        questions = (Question.query
                         .filter(Question.category == str(current_category['id']))
                         .all())
      else:
        # if no previous questions is given and also no category , just get any random one.
        questions = (Question.query.all())
    else:
      if current_category:
          # if previous questions is given and also a category, query questions in same category list differ than given list in previous questions
        questions = (Question.query
                         .filter(Question.category == str(current_category['id']))
                         .filter(Question.id.notin_(previous_questions))
                         .all())
      else:
        # if previous questions is given but no category, query questions which are not contained in previous list of questions.
        questions = (Question.query
                     .filter(Question.id.notin_(previous_questions))
                         .all())

    # Format questions and choose random one
    questions_formatted = format_questions(questions)
    # random.randint(low, high=None)
    # Return random integers from low(inclusive) to high(exclusive).
    random_question = questions_formatted[random.randint(0, len(questions_formatted))]

    return jsonify({
        'success': True,
        'question': random_question
    })
  '''
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  '''
   TEST: POST '/quizzes'
        Pass: test_play_quiz_with_category
        Fail: test_400_play_quiz_with_category
  '''
#----------------------------------------------------------------------------#
# Error Handlers
#----------------------------------------------------------------------------#
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422.
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message":  get_err_msg(error, "bad request")
    }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": get_err_msg(error, "resource not found")
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": get_err_msg(error, "unprocessable")
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

  return app


    
