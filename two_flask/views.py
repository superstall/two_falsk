from two_flask import app,db
from flask import request,redirect,url_for,flash,render_template
from flask_login import login_user,logout_user,login_required,current_user
from two_flask.models import User,Movie,Ariticles

import datetime


# 首页
@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单的数据
        title = request.form.get('title')
        content = request.form.get('content')
        name = request.form.get('name')

        # 验证title，year不为空，并且title长度不大于60，year的长度不大于4
        if not title or not content or not name :
            flash('输入错误')  # 错误提示
            return redirect(url_for('index'))  # 重定向回主页
        
        movie = Ariticles(title=title,content=content,author=name)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()   # 提交数据库会话
        flash('数据创建成功')
        return redirect(url_for('index'))

    movies = Ariticles.query.all()

    return render_template('index.html',movies=movies)

#查看详情
@app.route('/thisone/<int:movie_id>',methods=['GET'])
@login_required
def this_one(movie_id):
    movie = Ariticles.query.get_or_404(movie_id)
    return render_template('this_one.html', movie=movie)
# 编辑电影信息页面
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Ariticles.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')


        if not title or not content:
            flash('输入错误')
            return redirect(url_for('edit'),movie_id=movie_id)
        
        movie.title = title
        movie.content = content

        db.session.commit()
        flash('信息已经更新')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        
        current_user.name = name
        db.session.commit()
        flash('设置name成功')
        return redirect(url_for('index'))

    return render_template('settings.html')

# 删除信息
@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
@login_required    
def delete(movie_id):
    movie = Ariticles.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))

# 用户登录 flask提供的login_user()函数
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录用户
            flash('登录成功')
            return redirect(url_for('index'))  # 登录成功返回首页
        flash('用户名或密码输入错误')
        return redirect(url_for('login'))
    return render_template('login.html')

# 用户登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('index'))