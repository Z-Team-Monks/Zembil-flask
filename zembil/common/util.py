from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() \
          in current_app.config['ALLOWED_EXTENSIONS']



def cleanNullTerms(d):
   clean = {}
   for k, v in d.items():
      if isinstance(v, dict):
         nested = cleanNullTerms(v)
         if len(nested.keys()) > 0:
            clean[k] = nested
      elif v is not None:
         clean[k] = v
   return clean