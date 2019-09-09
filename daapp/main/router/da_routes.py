from flask_restplus import Namespace, Resource, fields
from mlapp.main.service import nlp_services

ns_da = Namespace('data analysis', description='Access the different types of data analyses')
