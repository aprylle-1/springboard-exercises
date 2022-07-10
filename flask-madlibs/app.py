from stories import stories
from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool12345"
debug =DebugToolbarExtension(app)

@app.route("/")
def root():
    return render_template('root.html')
@app.route("/form")
def madlib_form():
    story_num = int(request.args.get('stories'))
    story = stories[story_num]
    return render_template('madlib-form.html', prompts = story.prompts, story_num = story_num)

@app.route("/story")
def generate_story():
    story = stories[int(request.args.get('story_num'))]    
    answers = {}
    for prompt in story.prompts:
        answers[prompt] = request.args.get(prompt)
    generated_story = story.generate(answers)
    return render_template("story.html", story=generated_story)