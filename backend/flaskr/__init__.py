import json
import os
from unicodedata import category
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
  
  questions = [question.format() for question in selection]
  curr_questions = questions[start:end]
  return curr_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  # CORS(app, resources={r"*/api/*" : {origins: '*'}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response
  

  '''
  @TODO: 
  # * Create an endpoint to handle GET requests 
  # * for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    data = Category.query.all()
    categories = [category.format() for category in data]
    
    
    if len(categories) == 0:
      abort(404)
      
    return jsonify(
      {
        "success": True,
        "categories" : categories,
        "total_categories": len(Category.query.all())
      }
    )
  
  def get_category_list():
    categories = {}
    category_list = Category.query.all()
    
    for category in category_list:
      categories[category.id] = category.type
    
    return categories


  '''
  @TODO: 
  # * Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    curr_questions = paginate_questions(request, selection)
    
    # data = Category.query.all()
    # categories = [category.format() for category in data]
    
    if len(curr_questions) == 0:
      abort(404)
    
    return jsonify(
      {
        'success': True,
        'questions': curr_questions,
        'total_questions': len(selection),
        'categories': get_category_list(),
        'current_category': None
      }
    )
      
    
  
  '''
  @TODO: 
 # *  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
      
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      curr_questions = paginate_questions(request, selection)
      
      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': curr_questions,
        'total_questions': len(selection)
      })
    except:
      abort(422)
    
    
  
  '''
  @TODO: 
  # * Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  @TODO: 
  # * Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    new_question = body.get('question', None)
    
    search = body.get('search', None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection.all())
        })
      
      else:
        question = Question(
            question=new_question, 
            answer=new_answer, 
            category=new_category, 
            difficulty=new_difficulty
        )
        
        question.insert()
        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.all()
        current_questions = paginate_questions(request, selection)
        current_categories = [category.format() for category in categories]
        
            
        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'category': current_categories,
            'total_questions': len(current_questions)
        })
        
    except:
      abort(422)

  '''
  @TODO: 
  # * Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    selection = Question.query.order_by(Question.id).filter(Question.category == category_id)
    curr_questions = paginate_questions(request, selection)
    
    if len(curr_questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'category_id': category_id,
      'questions': curr_questions,
      'total_questions': len(curr_questions)
    })
    


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
  def play_quiz():
    body = request.get_json()
    
    previous_question = body.get('previous_question', [])
    category = body.get('category', None)
    
    try:
      if category == 0 or category is None:
        quiz_questions = Question.query.all()
      else:
        quiz_questions = Question.query.filter(Question.category == category).all()
        
      curr_questions = []
      
      for question in quiz_questions:
        if question.id not in previous_question:
          curr_questions.append(question.format())
      
      if len(curr_questions):
        question = random.choice(curr_questions)
        return jsonify({
          'question': question
        })
      else:
        abort(422)
        
    except:
      abort(404)
  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    
  @app.errorhandler(422)
  def unprocessable(error):
    return(
      jsonify(
        {
          'success': False,
          'error': 422,
          'message': 'unprocessable'
        }
      ), 422
    )
  
    
  
  return app

    