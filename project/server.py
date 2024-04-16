import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.create_user_service
import project.fetch_webpage_content_service
import project.update_profile_service
import project.user_login_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-url-preview-api",
    lifespan=lifespan,
    description="Based on the user's requirements for webpage content extraction and metadata retrieval, the task will involve creating an endpoint that accomplishes several key functions: it will accept a URL from the user, retrieve the webpage content at that URL, extract relevant metadata, generate a preview snippet that includes the page's title, description, and a thumbnail image, and return structured preview data for use in link sharing and embedding. The project will utilize a specific tech stack consisting of Python as the programming language, FastAPI for the API framework to ensure high performance and easy async tasks handling, PostgreSQL for the database to store and manage extracted metadata efficiently, and Prisma as the ORM for seamless database integration and querying. The process will include parsing the webpage content with robust tools capable of handling various content structures, including dynamic content loaded through JavaScript. For preview snippet generation, the system will extract metadata such as HTML <title>, <meta name='description'> tags, Open Graph, and Schema.org metadata. These extracted elements will form the basis of the preview snippet, which will be structured and returned in a uniform format suitable for embedding or link sharing on social platforms or other web applications. Best practices for content extraction and metadata retrieval that have been considered include the ethical scraping respecting robots.txt, utilizing HTML parsing libraries for content extraction, and performance optimization to provide high-quality previews while minimizing load on servers and target websites.",
)


@app.put(
    "/user/profile/update",
    response_model=project.update_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_profile(
    email: Optional[str],
    username: Optional[str],
    bio: Optional[str],
    profile_picture_url: Optional[str],
) -> project.update_profile_service.UpdateUserProfileResponse | Response:
    """
    Allows authenticated users to update their profile.
    """
    try:
        res = await project.update_profile_service.update_profile(
            email, username, bio, profile_picture_url
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/content/retrieve",
    response_model=project.fetch_webpage_content_service.FetchWebpageContentResponse,
)
async def api_post_fetch_webpage_content(
    url: str,
) -> project.fetch_webpage_content_service.FetchWebpageContentResponse | Response:
    """
    Retrieve webpage content for the provided URL.
    """
    try:
        res = await project.fetch_webpage_content_service.fetch_webpage_content(url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register", response_model=project.create_user_service.CreateUserResponse
)
async def api_post_create_user(
    email: str, username: str, password: str
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Endpoint to register a new user.
    """
    try:
        res = await project.create_user_service.create_user(email, username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    username_or_email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Endpoint for user authentication and login.
    """
    try:
        res = await project.user_login_service.user_login(username_or_email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
