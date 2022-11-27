import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging, sys


def get_db_connection():
    """Function connects to database with the name `database.db`"""
    try:
        connection = sqlite3.connect('file:database.db?mode=rw', uri=True)
    except:
        app.config['db_health']=False
    connection.row_factory = sqlite3.Row
    app.config['connection_counter'] += 1
    return connection
   
def get_post(post_id):
    """Function to get a post using its ID"""
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close() 
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['connection_counter']=0
app.config['posts_number']=0
app.config['db_health']=True

# Define the main route of the web application 
@app.route('/')
def index():
    # global posts_number
    connection = get_db_connection()
    try:
        posts = connection.execute('SELECT * FROM posts').fetchall()
    except:
        app.config['db_health']=False
    app.config['posts_number']=len(posts)
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info('A non-existing article is accessed and a 404 page is returned')
        return render_template('404.html'), 404
    else:
        app.logger.info('An existing article "'+post['title']+'" is retrieved')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('The "About Us" page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('A new article "'+title+'" is created')
            return redirect(url_for('index'))

    return render_template('create.html')

# Define endpoint for the  application health check
@app.route('/healthz')
def healthz():
    #Standout Suggestion 1: Dynamic Healthcheck endpoint
    if app.config['db_health']:
        result_value='OK - healthy'
        status_int=200
    else:
        result_value='ERROR - unhealthy'
        status_int=500

    response=app.response_class(
        response=json.dumps({'result':result_value }),
        status=status_int,
        mimetype='application/json'
            )
    return response

# Define endpoint for application metrics
@app.route('/metrics')
def metrics():
    response=app.response_class(
            response=json.dumps({'db_conection_count':app.config['connection_counter'], 'post_count':app.config['posts_number']}),
        status=200,
        mimetype='application/json'
            )
    return response
    
# start the application on port 3111
if __name__ == "__main__":
    loglevel = logging.DEBUG
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    log_file_handler=logging.FileHandler("debug.log")
    handlers = [stderr_handler, stdout_handler, log_file_handler]
    format_output='%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    logging.basicConfig(
        format=format_output,
        level=loglevel,
        handlers=handlers
     ) 
    app.run(host='0.0.0.0', port='3111', debug=True)
