from main import app, db, ProductModel
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, ProductModel=ProductModel)