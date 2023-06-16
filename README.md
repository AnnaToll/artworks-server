# A fully functional Backend

A fully working backend for a CMS (content management system) functioning as a REST API, with Djangos own Sessions and CSRF-protection tweaked to work with an external frontend-application. It is hosted on Heroku with HostUp as Domain registar. Github actions is used to create a CI/CD-pipeline, and it uses a PostreSQL database hosted on Railway.

## Distinctiveness and Complexity

With the goal of making something different and more complex than previous projects, I chose to make a backend application for a CMS, that is part of a larger project. I wanted to make something real. To take that final step, remove the training wheels, and create an application with proper security, hosted in the cloud and with a real domain. When coming across different web applications, I have often found that the frontend is separate from one or more backends. So in the spirit of creating something "real" as well as something complex and difficult, I set out on the journey to make my very own and fully functional backend application communcicating with a separate frontend. I also added a index.html file, some Javascript, React and CSS to make sure to fulfill the requirements for passing this assignment. This single view is responsive with the help of media queries and flexbox, and looks nice and offers great functionality on both laptops and mobile devices.

The project communicates with a frontend application by my own design, built with React and Typescript. I realize however that you can not take the frontend into consideration when grading the project. I will leave a link to the frontend repo and app all the same, in case you are curious.

Some of the most complex problems I had to solve was to make CSRF-protection, User permissions, authorization and Sessions work properly. The default settings are set up to work together with server-side rendering, so as expected, nothing worked when I first started connecting the frontend with the backend. I started with going through Djangos entire documentation regarding these subjects, but after adjusting the settings it still didn't work, so I had to deep dive into all I could find on MDN web docs on cookies, headers, CORS, and request/response objects. After three days of headches, despair and frustrations I finally got it to work properly.

The solution was to install django-cors-headers, give the user all necessary permissions, add the correct settings for CSRF and Sessions, allow credentials, defining allowed origins as well as the required Access-Control-Expose-Headers and Access-Control-Allow-Headers.

Another aspects of adding complexity is that I use a PostreSQL-database hosted on Railway. The reason I didn't want to use the default database is to prevent accidental overrides as well as making the progress of deploying the project to Heroku easier and safer. To make this work I created a database on Railway, and configured "DATABASES" in settings.py with the required variables. To prevent sensitive information about the database from becoming public I have also installed django-environ so that I can use environmental variables in the project. They are stored locally in a .env file as well as on Heroku.

I also run the code in different environments, locally and in production. Since some settings should change depending on the environment I set some settings conditionally.

In views, when it comes to distinctiveness, instead av returning render or redirect functions, I return almost all bodies in the response object as JSON strings. In working with JSON strings I came across the challenge of first having to turn all data from Django Query sets (with foriegn keys and many-to-many fields), to Python dicts or lists, and finally to JSON strings.

To conclude this section I will specify some additional features that speaks to both the complexity and distinctinvess of the project.

To make deploying to Heroku possible I installed Gunicorn with a Procfile that specifies how to start the application with Gunicorn, as well as a requirements.txt file.

I also created a CI/CD-pipeline using Github actions to automatically deploy to Heroku on push to the main branch. This makes the deployment both easy and fast.

The final step towards creating my real, and fully functional backend was to connect it to a domain name. I use HostUp as a Domain registar, and connected it through a CNAME to Heroku.

I realize this project might not be of the kind you are used to. But as you can see described above, it is complex and unique, compared to our previous assignments. And in building it I have gained a great deal of valuable knowledge.


## Files

### requirements.txt

A file that includes all packages used in the project. I will explain more about some of the packages below.

1. django-cors-headers: Used to handle CORS, and allows me to define how and to whom the application communicates.
2. django-environ: Used to handle environmental variables in Django. Needed to protect sensitive data from being exposed.
3. Gunicorn: A HTTP server for WSGI applications that increases performance.

### Procfile

Heroku uses this file to get information on what command to run to start the application.

### .github/workflows/deploy.yml

A simple CI/CD-pipeline that uses a heroku action to deploy automatically to Heroku when I push to the branch main. I have added the Heroku Api Key as an evironmental to my Github repo.

### portfolios/urls.py

In this file the path to admin is defined. Included is also a line to add all urls from the "artworks" application.

### portfolios/settings.py

This is where all settings for the Django project is configured.

1. Set SECRET_KEY, DEBUG and HOST differently depending on evironment
2. INSTALLED_APPS includes all apps that are used in the project. I have added "artworks" and "corsheaders".
3. MIDDLEWARE is a list of middleware that runs sometime in the request/response cycle. The CorsMiddleware is at the top so that it will filter requests before it can be blocked by another middleware (for inctance the SecurityMiddleware).
4. app_origins is a list of allowed origins.
5. CORS: I have specified the allowed origins, allowed the use of credentials (which includes cookies), as well as specified allow headers for pre-flight request and expose headers to allow cross-origin sharing.
6. CSRF: The backend is connected to a subdomain to the domain the frontend is using. This means I can use same-origin cookies (even though CORS sees this as cross origin). I have set the CSRF_COOKIE_DOMAIN to the domain name, which means it can be accessed by both frontend and backend. The CSRF cookie is set on the backend, and accessed on the frontend, to be sent back via the required "X-CSRFToken" header. I also specified the trusted origins.
7. SESSION: The session cookie is both set and accessed on the backend. It has httponly set to true, which is a security measure to prevent it from being accessed via javascript on the frontend.
8. DATABASES: I configured it with Railways variables. The sensitive data is placed in hidden environmental variables for security reasons.
9. LOGGING: I added logging so that it would be easier to solve bugs and develop in a faster pace.

### portfolios/.gitignore

A file that tells git which files not to add when commiting. I have added ".env" in this file to prevent the sensitive environmental variables to be uploaded and exposed.

### portfolios/.env

Contains environmental variables for the secret key, as well as password, user and name for the database.

### artworks/views.py

Here you can find all my functions to handle requests and responses. 

### artworks/urls.py

This file specifies all paths, as well as the corresponding function that should run when a request to a specific path is made.

### artworks/models.py

Contains all my Models. The application is the backend for an artwork gallery. I have built the entire project to work as a smaller and simpler version of a CMS, so you can find models for users, page types, images, pages, categories and artworks.

### artworks/admin.py

This is where I have specified all Models that should be added to djangos Admin interface.

### artworks/templates/artworks/index.html

A simple html file, linking to React and Babel in the head, with a simple div with the id "root" that is connected to my React code. This is also where I link to my stylesheet and React and Javascript file.

### artworks/static/artworks/styles.css

This is my stylesheet. I have linked to a google font, bootstraps icons, and I have also added some media queries make the page more responsive. I have added different classes that toggle between using javascript to hide and show elements.

### artworks/static/artworks/app.js

In this file I have created some React components, pieced them together and rendered them to the div in index.html with the id "root". I have also added som plain Javascript to change classes which results in content being visible or hidden when other content is clicked on.

## How to run the application

```
python manage.py runserver
```




