import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def get_table(tbl, s):
  tbl = s.CASTable(tbl)
  return(tbl.to_frame())

def partition(s, tbl):
  s.loadActionSet("sampling")
  s.sampling.srs(table = {"name":tbl, "caslib":"casuser"},
                 samppct = 30,
                 partind = True,
                 output = {"casOut": {"name": tbl + "_part", "replace":True, "caslib":"casuser"}, "copyVars":'ALL'}
)

def score_model(model, model_tbl, target):
    score = dict(
        table      = model_tbl,
        modelTable = model + '_model',
        copyVars   = [target, '_PARTIND_'],
        assessOneRow=True,
        casOut     = dict(name = model + '_scored', replace = True)
    )
    return score

def assess_model(s, model, target):
    assess = s.percentile.assess(
        table    = dict(name = model + '_scored', caslib = "casuser", where = '_PARTIND_ = 1'),
        inputs   = '_' + model.upper() + '_P_           1',      
        response = target,
        event    = '1',
    )
    return assess

def measure_models(s, models, scores, model_names, model_tbl, target):
  [scores[i](**score_model(models[i], model_tbl, target)) for i in range(len(models))]

  roc_df  = pd.DataFrame()
  for i in range(len(models)):
      tmp = assess_model(s, models[i], target)
      tmp.ROCInfo['Model'] = model_names[i]
      roc_df = pd.concat([roc_df, tmp.ROCInfo])

  roc_df['Misclassification'] = 1 - roc_df['ACC']
  miss = roc_df[round(roc_df['CutOff'], 2) == 0.5][['Model', 'Misclassification']].reset_index(drop = True)
  miss.sort_values('Misclassification')

  fig = plt.figure(figsize = (7, 6))
  for key, grp in roc_df.groupby(['Model']):
      plt.plot(grp['FPR'], grp['Sensitivity'], label = key + ' (C = %0.2f)' % grp['C'].mean())
  plt.plot([0,1], [0,1], 'k--')
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.legend(loc='lower right')
  plt.title('ROC Curve (using validation data)')

  return miss, fig


def auto_ml(s, tbl_name, dt, rf, gb, nn):
  s.loadActionSet("decisionTree")
  s.loadActionSet("neuralNet")
  
  partition(s, tbl_name + "_TRANSFORMED")
  
  model_tbl = tbl_name + "_TRANSFORMED_part"
  colinfo = s.table.columnInfo(table = model_tbl).ColumnInfo.head(-1)

  print(colinfo)
  
  target = colinfo.Column[0]
  inputs = list(colinfo.Column[1:])
  nominals = [target] + list(colinfo[colinfo.Type == 'varchar'].Column.values)
  
  models, scores, model_names = [], [], []
  
  print("automl 1")
  print("target:")
  print(target)
  print("inputs:")
  print(inputs)
  
  if(dt):
    print("Executing decisiton tree...")
    s.decisionTree.dtreeTrain(
        table = {"name":model_tbl, "caslib":"casuser", "where":"_PartInd_ = 0"},
        target = target,
        inputs = inputs,
        nominals = nominals,
        casOut = {"name":"dt_model", "caslib":"casuser", "replace":True}
    )
    models.append("dt")
    scores.append(s.decisionTree.dtreeScore)
    model_names.append('Decision Tree')
    
  if(rf):
      print("Executing random forest ...")
      s.decisionTree.forestTrain(
          table = {"name":model_tbl, "caslib":"casuser", "where":"_PartInd_ = 0"},
          target = target,
          inputs = inputs,
          nominals = nominals,
          casOut = {"name":"rf_model", "caslib":"casuser", "replace":True}
      )
      models.append("rf")
      scores.append(s.decisionTree.forestScore)
      model_names.append('Random Forest')
    
  if(gb):
      print("Executing gradient boosting ...")
      s.decisionTree.gbtreeTrain(
          table = {"name":model_tbl, "caslib":"casuser", "where":"_PartInd_ = 0"},
          target = target,
          inputs = inputs,
          nominals = nominals,
          casOut = {"name":"gbt_model", "caslib":"casuser", "replace":True}
      )
      models.append("gbt")
      scores.append(s.decisionTree.gbtreeScore)
      model_names.append('Gradient Boosting')
      
  if(nn):
      print("Executing neural network...")
      s.neuralNet.annTrain(
          table = {"name":model_tbl, "caslib":"casuser", "where":"_PartInd_ = 0"},
          target = target,
          inputs = inputs,
          nominals = nominals,
          casOut = {"name":"nn_model", "caslib":"casuser", "replace":True}
      )
      models.append("nn")
      scores.append(s.neuralNet.annScore)
      model_names.append('Neural Network')

  print("automl 2")
  
  print("models:")
  print(models)
  
  print("model_names")
  print(model_names)
  
  return(measure_models(s, models, scores, model_names, model_tbl, target))

def app():
    st.title('Modeling')
    if 'session' in st.session_state:
        with st.form("my_form1"):
            dt = st.checkbox('Decision Tree')
            rf = st.checkbox('Random Forest')
            gb = st.checkbox('Gradient Boosting')
            nn = st.checkbox('Neural Network')
            submitted = st.form_submit_button("Train Models")
            if submitted:
                if 'tbl_name' in st.session_state:
                    s = st.session_state.session
                    miss, fig = auto_ml(s, st.session_state.tbl_name, dt, rf, gb, nn)
                    st.dataframe(miss)
                    st.pyplot(fig)