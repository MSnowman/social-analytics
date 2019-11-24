from flask_restplus import Namespace, Resource, fields
from mlapp.main.service import nlp_services

ns_ml = Namespace('machine learning', description='Natural Language Processing Operations')

training_data = ns_ml.model('TrainingData', {
    'user_id': fields.String(required=True, description='User Id training the data.  Could be either an individual '
                                                        'or business account'),
    'topic_name': fields.String(required=True, decription='Topic name that was listening to search terms'),
    'data_cnx': fields.Raw(required=True, description='MySQL connection credentials'),
    'data_mongo': fields.Raw(required=True, description='MongoDB connection credentials'),
    'word_filter': fields.String(required=False, description='Enter a word to refine what training data to add.  '
                                                             'Used when not enough Relevant data is returned on your'
                                                             'initial request '),
    'number_records': fields.Integer(required=False, description='Number of training data records.  Default is 250')
})

record_annotations = ns_ml.model('RecordAnnotations', {
    'user_id': fields.String(required=True, description='User Id training the data.  Could be either an individual '
                                                        'or business account'),
    'topic_name': fields.String(required=True, decription='Topic name that was listening to search terms'),
    'data_cnx': fields.Raw(required=True, description='MySQL connection credentials'),
    'records': fields.List(fields.List(fields.String), required=True, description='List of listed pairs of '
                                                                                  '[unique_id, TRUE/FALSE]'),
    'annotator': fields.String(required=True, description='Name of annotator')
})

new_annotators = ns_ml.model('NewAnnotators', {
    'user_id': fields.String(required=True, description='User Id training the data.  Could be either an individual '
                                                        'or business account'),
    'topic_name': fields.String(required=True, decription='Topic name that was listening to search terms'),
    'data_cnx': fields.Raw(required=True, description='MySQL connection credentials'),
    'annotators': fields.List(fields.String, required=True, description='List of annotators to add.')
})

record_to_classify = ns_ml.model("RecordToClassify", {
    'user_id': fields.String(required=True, description='User Id training the data.  Could be either an individual '
                                                        'or business account'),
    'topic_name': fields.String(required=True, decription='Topic name that was listening to search terms'),
    'record_id': fields.String(required=True, description='unique ID of the record to classify'),
    'text': fields.String(required=True, description='text you want classified')
})


@ns_ml.route('setup_training_data')
class SetupTrainingData(Resource):
    @ns_ml.doc('setup_training_data')
    @ns_ml.expect(training_data, validate=True)
    @ns_ml.response(409, 'Training data already exists for topic.  Restore or delete existing Training Data.')
    def post(self):
        """Setup training data"""
        return nlp_services.setup_training_data(data=ns_ml.payload)


@ns_ml.route('get_more_training_data')
class GetMoreTrainingData(Resource):
    @ns_ml.doc('get_more_training_data')
    @ns_ml.expect(training_data, validate=True)
    def put(self):
        """Get more training data records to train the model with.  Requires "record_numbers" to be passed in model."""
        return nlp_services.get_more_training_data(data=ns_ml.payload)


@ns_ml.route('get_classified_training_data/<string:user_id>/<string:topic_name>')
class GetClassifiedTrainingData(Resource):
    @ns_ml.doc('get_classified_training_data')
    def get(self, user_id, topic_name):
        """Get only training data of a topic that has been classified for a given user_id"""
        return nlp_services.get_classified_data(user_id, topic_name)


@ns_ml.route('get_unclassified_training_data/<string:user_id>/<string:topic_name>')
class GetUnclassifiedTrainingData(Resource):
    @ns_ml.doc('get_unclassified_training_data')
    def get(self, user_id, topic_name):
        """Get only training data of a topic that has not yet been classified for a given user_id"""
        return nlp_services.get_unclassified_data(user_id, topic_name)


@ns_ml.route('get_all_training_data/<string:user_id>/<string:topic_name>')
class GetAllTrainingData(Resource):
    @ns_ml.doc('get_all_training_data')
    def get(self, user_id, topic_name):
        """ Get all training data of a topic for a given user_id"""
        return nlp_services.get_all_training_data(user_id, topic_name)


@ns_ml.route('get_list_training_data_topics/<string:user_id>')
class GetListTrainingDataTopics(Resource):
    @ns_ml.doc('get_list_training_data_topics')
    def get(self, user_id):
        """Get the list of training data topics for a given user_id"""
        return nlp_services.get_list_training_data_topics(user_id)


@ns_ml.route('add_annotators')
class AddAnnotators(Resource):
    @ns_ml.doc('add_annotators')
    @ns_ml.expect(new_annotators, validate=True)
    def put(self):
        """Add new annotators to the training data"""
        return nlp_services.add_annotators(data=ns_ml.payload)


@ns_ml.route('annotate_data')
class AnnotateData(Resource):
    @ns_ml.doc('annotate_data')
    @ns_ml.expect(record_annotations)
    def put(self):
        """Annotate training data as relevant or not relevant"""
        return nlp_services.annotate_training_data(data=ns_ml.payload)


@ns_ml.route('classify_data')
class ClassifyData(Resource):
    @ns_ml.doc('classify_data')
    @ns_ml.expect(record_to_classify)
    def post(self):
        """NLP Classification of Data"""
        return nlp_services.classify_data(data=ns_ml.payload)
