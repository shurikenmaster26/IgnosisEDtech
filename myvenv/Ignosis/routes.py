import os
import secrets
from PIL import Image
from Ignosis.config import LEAGUES, REQUIRED_POINTS_FOR_PROMOTION
from flask import render_template, url_for, flash, redirect, request, current_app
from Ignosis import bcrypt,db
from Ignosis.models import User, UserProblems, UserBadges, Badges, PracticeProblems
from Ignosis.forms import RegistrationForm, LoginForm, UpdateaccountForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, url_for, flash, redirect, request

# Use current_app.proxy in place of directly importing 'app'
def init_routes(app: Flask):
    app.config['LEAGUES'] = LEAGUES
    app.config['REQUIRED_POINTS_FOR_PROMOTION'] = REQUIRED_POINTS_FOR_PROMOTION
    @app.route("/home")
    @app.route("/")
    def home():
        if current_user.is_authenticated:
            image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
            return render_template('home.html', image_file=image_file)
        else:
            return render_template('home.html')

    @app.route("/signup", methods=['GET','POST'])
    def register():
        form=RegistrationForm()
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user=User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Your account has been created! Please log in now', 'success')
            return redirect(url_for('home'))
        return render_template('signup.html',title='Sign up',form=form)

    @app.route("/login", methods=['GET','POST'])
    def login():
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('account'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template("login.html", title='Log in', form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route("/profile")
    @login_required
    def account():
        image_file=url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account-Profile.html', title='profile',image_file=image_file)

    @app.route("/account-settings")
    @login_required
    def account_settings():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('account-Settings.html', title='profile', image_file=image_file,)


    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn

    @app.route("/account-settings-Edit_profile", methods=['GET','POST'])
    @login_required
    def account_settings_edit_profile():
        form=UpdateaccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username=form.username.data
            current_user.email=form.email.data
            current_user.bio=form.bio.data

            print("Bio value to be updated:", form.bio.data)


            db.session.commit()
            flash('your account has been updated!','success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.bio.data=current_user.bio
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('account-ProfileSETTINGS.html', title='profile', image_file=image_file, form=form)


    def calculate_points(problem_id):
        # Fetch the problem from the database based on the problem_id
        problem = PracticeProblems.query.get_or_404(problem_id)

        # Example: Calculate points based on the difficulty of the problem
        if problem.ProblemClass == 'Olympian':
            points = 10
        elif problem.ProblemClass == 'Titan':
            points = 8
        elif problem.ProblemClass == 'Demigod':
            points = 6
        elif problem.ProblemClass == 'Hero':
            points = 4
        else:
            points = 2

        return points
    
    def get_next_league(current_league):
    # Assuming LEAGUES is defined in your configuration
        for league, required_points in LEAGUES.items():
            if required_points > User.total_points:
                return league
        return None

    @app.route('/solve_problem/<int:user_id>/<int:problem_id>')
    def solve_problem(user_id, problem_id):
    # ... (your logic for solving the problem and calculating points)
    
    # Example: Calculate points based on the solved problem
        points = calculate_points(problem_id)

        # Update user points
        UserProblems.update_user_points(user_id, points)

        # Check if the user has gained enough points for automatic promotion
        user = User.query.get(user_id)
        if user.total_points >= REQUIRED_POINTS_FOR_PROMOTION:
                current_league = user.skillset  # Assuming skillset represents the user's current league
                next_league = get_next_league(current_league)

                if next_league:
                    user.skillset = next_league
                    flash(f'Congratulations! You have been promoted to {next_league} league.', 'success')


        db.session.commit()
            
            # Implement logic for automatic promotion (e.g., change user's league)
            # ...

        # ... (rest of your route logic)
        return redirect(url_for('your_destination_route'))


    @app.route("/courses")
    def Courses():
        if current_user.is_authenticated:
            image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
            return render_template('courses.html', image_file=image_file)
        else:
            return render_template('courses.html')




    #C COURSES

    @app.route("/courses-C")
    @login_required
    def C():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C.html',image_file=image_file)

    @app.route("/C-Intro_to_C")  #1
    @login_required
    def C_intro():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C_Intro.html',image_file=image_file)

    @app.route("/C-Installation")  #2
    @login_required
    def C_install():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-Install.html',image_file=image_file)

    @app.route("/C-Variables") #3
    @login_required
    def C_variable():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-Variables.html',image_file=image_file)

    @app.route("/C-Operators") #4
    @login_required
    def C_operator():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C_Operator.html',image_file=image_file)

    @app.route("/C-InputOutput") #5
    @login_required
    def C_inputoutput():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-InputOutput.html',image_file=image_file)

    @app.route("/C-Loops") #6
    @login_required
    def C_loops():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-loops.html',image_file=image_file)

    @app.route("/C-IfElse") #7
    @login_required
    def C_ifelse():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-Ifelse.html',image_file=image_file)

    @app.route("/C-Functions") #8
    @login_required
    def C_functions():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-functions.html',image_file=image_file)

    @app.route("/C-Arrays") #9
    @login_required
    def C_arrays():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-arrays.html',image_file=image_file)

    @app.route("/C-Pointers")  #10
    @login_required
    def C_pointers():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-pointers.html',image_file=image_file)

    
    @app.route("/C-Recursion")  #11
    @login_required
    def C_recursion():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('courses-C-recursion.html',image_file=image_file)
    

    @app.route("/practise")
    @login_required
    def Practise():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('Practise.html',image_file=image_file)
    
    @app.route("/practise-C-Intro")
    @login_required
    def PractiseC1():
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('Practise-C-Intro.html',image_file=image_file)
    
    @app.route('/leaderboard')
    @login_required
    def leaderboard():
    # Fetch users ordered by total points (modify the query based on your model structure)
        users = User.query.order_by(User.total_points.desc()).all()
        image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
        return render_template('leaderboard.html', users=users, image_file=image_file)
    

def create_routes(app: Flask):
    init_routes(app)