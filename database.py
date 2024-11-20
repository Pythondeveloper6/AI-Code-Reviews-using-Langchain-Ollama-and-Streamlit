# database functions
from datetime import datetime
from peewee import SqliteDatabase , TextField , DateTimeField , CharField , Model , FloatField

# create sqlite db
db = SqliteDatabase('code_reviews.db')


# define models : tables 
class CodeReview(Model):
    question = TextField()
    language = CharField()
    answer = TextField()
    score = FloatField()
    created_at = DateTimeField(default=datetime.now) # store date & time at creation (server)

    class Meta:
        database = db

    def get_review_data(self):
        return {
            'id' : self.id,
            'question': self.question , 
            'language': self.language ,
            'answer': self.answer , 
            'score': self.score,
            'time': self.created_at
        }


# intialize db
def init_database():
    db.connect()
    db.create_tables([CodeReview],safe=True)


# define functions 

def get_all_reviews():
    data = CodeReview.select().order_by(CodeReview.created_at.desc())
    return [r.get_review_data() for r in data]


def create_code_review(question,language,answer,score):
    review = CodeReview.create(
        question=question , 
        language = language , 
        answer = answer , 
        score = score
    )