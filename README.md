# Flask-Generate

Flask-Generate is a Flask extension that allows you to create web applications faster by creating models, routes and forms from console.
It also generates scaffolds with CRUD operations.

## Usage

### Installation

```shell
pip install Flask-Generate
```

### Generate a new Flask app

With Flask-Generate you can start a new project that contains base code to start working with

```shell
flask-generate app <my-app-name>
```

The flask-generate app command comes with two optional flags.

* --type: Indicates the app structure
    * options: MVC and Blueprint
    * default: mvc
* --orm: The ORM option to generate models based on it
    * options: SQLAlchemy and Peewee
    * default: SQLAlchemy

Example:

```shell
flask-generate app <app-name> --type blueprint --orm sqlalchemy
```

## Generators

Once you have the Flask-Generate extension installed, you have access to the generate commands group and start working with models, forms and blueprints.

### Blueprint

Blueprint generation will depend on the chosen app structure, if the chosen structure it's `MVC` the new blueprint will be saved on the blueprints folder as a Python module, else, the blueprint will be a Python package, similar to a Django app.

Arguments:
* name: Generates a Python file or package with this param

Example:

```shell
flask generate blueprint posts
```

Dest for mvc-like apps: `my-app/blueprints/posts.py`
Dest for blueprint-like apps: `my-app/posts`


### Models

Flask-Generate takes the `GENERATE_ORM` constant from settings to create models depending on the chosen ORM

Arguments:
* name: The model name, must be in PascalCase
* fields: List of model fields, must be declared as follows; field_name:type
* -d | --dest: File or Blueprint name where the model will be saved.


Example:

``` shell
flask generate model Post title:str body:text --dest posts
```

Generated models should be saved on `models/posts.py` for mvc-like apps and `posts/models.py` for blueprint-like apps

### Forms

Same as model command it takes the same parameters, but generates a form using the WTForms library.

Arguments:
* name: The model name, must be in PascalCase
* fields: List of model fields, must be declared as follows; field_name:type
* -d | --dest: File or Blueprint name where the model will be saved

Example:

```shell
flask generate form Post title:str body:text --dest posts
```

Generated forms should be saved on `forms/posts.py` for mvc-like apps and `posts/forms.py` for blueprint-like apps.


### scaffolds

Flask-Generate can create a fully functional scaffold with CRUD operations; the scaffold generates all the necessary code to start faster (model, forms, routes and templates)

Arguments:
* name: This will be used to generate the related scaffolding files or a full package
* model: Model name that generates a SQLAlchemy/Peewee class to work with
* fields: Model fields that also will be used to generate the form

Example:

```shell
flask generate scaffold posts Post title:str body:text
```
