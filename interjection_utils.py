def clean_interjections(interjection):
    interjection = interjection.strip()
    if interjection [0] != "(":
        return None
    else:
        interjection = interjection.replace(")(", ") (")
        interjection = interjection.replace(".", "")
        return interjection


def get_interjection_type(interjection):
  if interjection.find(") (") > -1:
    return 'double'
  elif interjection[0] == "(" and interjection.find(") ") > -1:
    return 'normal_plus'
  elif interjection[0] == "(" and interjection[-1] == ")":
     return 'normal'
  else:
    return 'other'


def clean_normal_plus_interjection(interjection):
  """
  Clean normal_plus interjection types:
  param: (INTERJECTION) OTHER
  ret: (INTERJECTION)
  """
  interjection = interjection['text'].split(")")
  interjection = str(interjection[0])+")"
  return interjection


def clean_double_interjection(interjection):
  """
  Clean double interjection types:
  param: (INTERJECTION) (INTERJECTION) OTHER
  ret: [(INTERJECTION), (INTERJECTION)]
  """
  interjection_list = interjection['text'].split(")")
  interjection_list = [i for i in interjection_list if i.find("(") > - 1]
  interjection_list = [str(i).strip()+")" for i in interjection_list if i.find(")") == - 1]
  return interjection_list


def get_cleaned_interjection_list(interjection_list):
    interjection_list = [clean_interjections(interjection) for interjection in interjection_list if clean_interjections(interjection)]
    interjection_dict = [{'text': interjection, 'type': get_interjection_type(interjection)} for interjection in interjection_list]
    interjection_list = [interjection['text'] for interjection in interjection_dict if interjection['type'] == 'normal']
    [interjection_list.append(clean_normal_plus_interjection(interjection)) for interjection in interjection_dict if interjection['type'] == 'normal_plus']
    [[interjection_list.append(j) for j in clean_double_interjection(interjection)] for interjection in interjection_dict if interjection['type'] == 'double']
    return interjection_list
