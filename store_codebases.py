from tinydb import TinyDB, Query
from codebase_rag import clone_repo, create_pinecone_namespace,remove_pinecone_index
import time
import shutil
import os
db = TinyDB('codebases.json')

codebase = Query()
def store_codebase(codebase_name,codebase_path):
    #clone the database into directory and then create pinecone index. After creating pineconex index we can remove the clones directory, to not take up space.
    clone_path_cwd = clone_repo(codebase_path)
    create_pinecone_namespace(clone_path_cwd,codebase_path)
    db.insert({'codebase_name':codebase_name,'codebase_path':codebase_path})

def get_codebases():
    return db.all()
def get_codebase(code_base_name):
    return db.search(codebase.codebase_name == code_base_name)
def remove_codebase(namespace):
    #we will remove the pinecone index as well
    remove_pinecone_index(namespace)
    
    db.remove(codebase.codebase_path == namespace)


print(get_codebases())