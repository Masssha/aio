from aiohttp import web
app = web.Application()

# async def get_user(request: web.Request) -> web.Response:
#     # json_data = await request.json()
#     return web.json_response({'sss': 'ddd'})
#
# app.add_routes(
#     [web.get('/user', get_user)]
# )

@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(request: web.Request) -> web.Response:
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handled(err: HttpError):
    json_response = jsonify({'status': 'error', 'message': err.message})
    json_response.status_code = err.status_code
    return json_response


def validate(schema, json_data):
    try:
        return schema(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        error = err.errors()[0]
        error.pop('ctx', None)
        raise HttpError(400, error)


def get_user(user_id):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(status_code=404, message='user does not exists')
    return user


def add_user(user):
    try:
        request.session.add(user)
        request.session.commit()
        return user
    except IntegrityError as err:
        raise HttpError(status_code=409, message='user already existsss')


def get_post(post_id):
    post = request.session.query(Post).get(post_id)
    return post


def add_post(post):
    request.session.add(post)
    request.session.commit()
    return post



class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(user.dict)


    def post(self):
        user_data = request.json
        user = User(name=user_data['name'])
        add_user(user)
        return jsonify(user.dict)

class PostView(MethodView):

    def get(self, post_id: int):
        post = get_post(post_id)
        return jsonify(post.dict)


    def post(self):
        post_data = request.json
        new_post_data = validate(CreatePost, post_data)
        post = Post(title=post_data['title'], description=post_data['description'], owner_id=post_data['owner_id'], owner_name=post_data['owner_name'])
        add_post(post)
        return jsonify(post.dict)


    def patch(self, post_id: int):
        post_data = request.json
        # user_data = validate(UpdateUser, user_data)
        post = get_post(post_id)
        for field, value in post_data.items():
            setattr(post, field, value)
        add_post(post)
        return jsonify(post.dict)


    def delete(self, post_id: int):
        post = get_post(post_id)
        request.session.delete(post)
        request.session.commit()
        return jsonify({'status': 'deleted'})


app.add_routes(
    [web.post('/user/', user_view)],
    [web.get('/user/<int:user_id>', user_view)],
    [web.post('/post/', post_view)],
    [web.get('/post/<int:post_id>/', post_view)],
    [web.delete('/post/<int:post_id>/', post_view)],
    [web.patch('/post/<int:post_id>/', post_view)]
)

web.run_app(app)