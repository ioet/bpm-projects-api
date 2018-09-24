from flask_restplus import fields, Namespace

ns = Namespace('projects', description='Operations for projects of the BPM')

# Project property
metadata = ns.model('Metadata', {
    'id': fields.String(required=True, title="Key"),
    'content': fields.String(title="Value")
})

# Project model for the API
project = ns.model('Project', {
    'uid': fields.String(readOnly=True, required=True, title='Identifier',
                         description='The project generated unique identifier'),
    'short_name': fields.String(required=True, title='Short name', description='Unique name in the system'),
    'comments': fields.String(title='Comments', description='Comments about the project'),
    'properties_table': fields.List(fields.Nested(metadata)),
    'active': fields.Boolean(title='Is active?', description='Whether the project is active or not'),
})

search_model = ns.model('SearchCriteria', {
    'search_string': fields.String(title='Keywords',
                                   description='What you want to search for in the comments/the name'),
    'active': fields.Boolean(title='Is active?',
                             description='true=only active, false=only inactive, none=all'),
})