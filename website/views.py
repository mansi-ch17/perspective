from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user
from .models import User,Post,Comment,Saved
from . import db


views = Blueprint("views", __name__)


@views.route("/")
 
 
def home():
    return render_template("perspective.html")

#directs to the latest feed page
@views.route("/homefeed")
@views.route("/homefeed.html")

@login_required
def homefeed():
     posts=Post.query.order_by(Post.date_created.desc())
     #posts=Post.query.all()
     return render_template("homefeed.html",user=current_user,posts=posts)

#directs to the login/signup option
@views.route("/second.html")
def second():
    return render_template("second.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/about.html")
def about():
    return render_template("about.html")

 

@views.route("/terms.html")
def terms():
    return render_template("terms.html")

 
#directs to the my profile page where the user can see their own profile
@views.route("/myprofile.html")
@login_required
def myprofile():
    user=current_user
    return render_template("myprofile.html",user=current_user,posts=user.posts)

#directs to the search by tags page
@views.route("/search.html", methods=['GET','POST'])
@login_required
def search():
    
    if request.method=='POST':
        tags=request.form.get('tags').strip()
        if not tags:
            flash('Search item cannot be empty', category='error') 
        else:
            posts=Post.query.all()
            return render_template("search.html",user=current_user,posts=posts,tags=tags)
    
    return render_template("search.html",user=current_user)

#directs to write page

@views.route("/write.html", methods=['GET','POST'])
@login_required 
def write():
    if request.method=='POST':
        heading=request.form.get('heading')
        text=request.form.get('text')
    #user can choose bold,italics or none for text formatting
        formatting=request.form.get('formatting')
    #tags will be needed for searching posts and adding images
        tags=request.form.get('tags').strip()
     #heading and text are required fields   
        if not heading:
            flash('Heading cannot be empty', category='error')
        if not text:
            flash('Post cannot be empty', category='error')
        if not tags:
            flash('Tag cannot be empty', category='error')
        else:
        #the post is added to the database if all criteria are met
            post=Post(heading=heading, text=text,formatting=formatting, tags=tags, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('New post created!', category='success')
            return redirect(url_for('views.homefeed'))



    return render_template("write.html",user=current_user)

 

@views.route("/<name>",methods=['GET','POST'])
#this particular function is used to add comments and view profile 
def manythings(name):
    #we deal with adding comments first. Since only the comment feature can send a POST request, the following lines of code
    #have been written to enable comments
        if request.method=='POST':
            text=request.form.get('text')
            if not text:
                flash('Comment cannot be empty', category='error')

            else:
                posts=Post.query.filter_by(heading=name).first()
                id2=posts.id
                comment=Comment(text=text,author=current_user.id,post_id=id2)
                db.session.add(comment)
                db.session.commit()
                posts=Post.query.all()
                comments=Comment.query.all()
                 
                user=User.query.filter_by(name=name).first()
                flash('Comment added', category='success')
                return render_template("post.html",user=user,posts=posts,heading=name,comments=comments )
            
     # to view user profile, we check if any user of this name exists. If they do, then we redirect to their profile 
        user=User.query.filter_by(name=name).first()
    
        if name==current_user.name:
            return render_template("myprofile.html",user=current_user,posts=user.posts)
        # else the name is a post name- we send it to the html template 
        elif user is None:
            posts=Post.query.all()
            comments=Comment.query.all()
             
         
            return render_template("post.html",user=current_user,posts=posts,heading=name,comments=comments )
        else:
        
           posts=user.posts
           return render_template("profile.html",user=user,posts=posts)

@views.route("/tosave/<name>")
@login_required
def save(name):

        posts=Post.query.filter_by(heading=name).first()
        id2=posts.id
        saveds=Saved.query.filter_by(author=current_user.id,post_id=id2).first()
        # if the user hasn't already saved, the post will now simply get saved to his database
        if saveds is None:
            
            flash('Post Saved',category='success')
           
        else:
        # if the user has saved the post before, then the last saved data will be deleted and a new entry will be created to keep their last saved posts on the top
            db.session.delete(saveds)
            db.session.commit()
            flash("Post is already saved",category='success')
        
        saveds=Saved(author=current_user.id,post_id=id2)
        db.session.add(saveds)
        db.session.commit()
         
        return redirect(url_for('views.saved'))
# directs to the saved list of the user   
@views.route("/saved.html")
def saved():
    saveds=Saved.query.order_by(Saved.date_created.desc())
    
    return render_template("saved.html",saveds=saveds,user=current_user)


