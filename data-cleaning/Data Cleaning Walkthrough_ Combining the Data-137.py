## 3. Condensing the Class Size Data Set ##

class_size = data['class_size']
class_size = class_size[class_size['GRADE '] == '09-12']
class_size = class_size[class_size['PROGRAM TYPE'] == 'GEN ED']
class_size.head()

## 5. Computing Average Class Sizes ##

import numpy

class_by_dbn = class_size.groupby('DBN')
#pd.groupby(class_by_dbn)

class_size = class_by_dbn.agg(numpy.mean)
class_size.reset_index(inplace=True)
data['class_size'] = class_size
print(data['class_size'].head())
