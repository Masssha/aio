from aiohttp import web
from models import User, Post, Session, engine, Base
import json
from sqlalchemy.exc import IntegrityError


app = web.Application()

async def orm_context(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app.cleanup_ctx.append(orm_context)


def get_http_error(error_class, message):
    response = json.dump({'error': message})
    http_error = error_class(text=response, content_type='application/json')
    return http_error


async def get_user_by_id(session, user_id):
    user = await session.get(User, user_id)
    if user is None:
        error = get_http_error(web.HTTPNot.Found, f'user with id {user_id} is not found')
        raise error
    return user


async def add_user(session, user):
    try:
        session.add(user)
        await session.commit()
        return user
    except IntegrityError as err:
        await session.rollback()
        raise get_http_error(web.HTTPConflict, message=f'user with name {user.name} already exists')


@web.middleware
async def session_mmiddleware(request, handler):
    async with Session() as session:
        request.session = session
        response = handler(request)
        return response

web.middleware.append(session_mmiddleware)


async def get_post_by_id(session, post_id):
    post = await session.get(Post, post_id)
    if post is None:
        error = get_http_error(web.HTTPNot.Found, f'post with id {post_id} is not found')
        raise error
    return post


async def add_post(session, post):
    session.add(post)
    await session.commit()
    return post



class UserView(web.View):


    @property
    def user_id(self):
        return int(self.request.match_info('user_id'))


    async def get_user(self):
        user = get_user_by_id(self.request.sesson, self.user_id)
        return user


    async def get(self):
        user = await self.get_user()
        return web.json_response(user.dict)


    async def post(self):
        user_data = self.request.json()
        user = User(name=user_data['name'])
        await add_user(self.session, user)
        return web.json_response(user.dict)



class PostView(web.View):

    @property
    def post_id(self):
        return int(self.request.match_info('post_id'))


    async def get_post(self):
        post = get_post_by_id(self.request.sesson, self.post_id)
        return post


    async def get(self):
        post = await self.get_post()
        return web.json_response(post.dict)


    async def post(self):
        post_data = self.request.json()
        post = Post(title=post_data['title'], description=post_data['description'], owner_id=post_data['owner_id'], owner_name=post_data['owner_name'])
        await add_post(self.session, post)
        return web.json_response(post.dict)


    async def patch(self):
        post_data = self.request.json()
        post = await self.get_post()
        for field, value in post_data.items():
            setattr(post, field, value)
        await add_post(self.session, post)
        return web.json_response(post.dict)


    async def delete(self):
        post = await self.get_post()
        await self.session.delete(post)
        await self.session.commit()
        return web.json_response({'status': 'deleted'})


app.add_routes(
[web.post('/user/', UserView),
web.get('/user/{user_id:\d+}', UserView),
web.post('/post/', PostView),
web.get('/post/{post_id:\d+}/', PostView),
web.delete('/post/{post_id:\d+}/', PostView),
web.patch('/post/{post_id:\d+}/', PostView)])


web.run_app(app)