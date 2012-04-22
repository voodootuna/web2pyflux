# coding: utf8
#TODO Sorting methods
@service.run
def comments():
    if request.args(0):
        t = db(db.article.id==request.args(0)).select(db.article.title, db.article.content, db.article.created_on, db.article.author).first()
        article = request.args(0)
        cmtdb = db(db.comments.article == article).select()
        cmts = []
        comment_mapping = {}
        top_level = []

        for r in cmtdb:
            cmts.append({'id':r.id, 'author':r.author, 'created_on':r.created_on, 'body':r.body, 'parent':r.parent_node, 'children':[]})
        
        for c in cmts:
            pid = c['parent']       
            cid = c['id']    
            comment_mapping[cid] = c
            if pid:
                comment_mapping[pid]['children'].append(c)
            else:
                top_level.append(c)
      

    return dict(children=top_level, article=t)
