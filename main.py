from random import randint
SUBJECTS_PLACE_NEED_DICT = {"Электротехника":2,"Физика":2,"Модели динамических объектов":2,"Иностранный язык":1,"Методы вычислений":2}
class Notebook:
 #   def __init__(self):
  #      pass
    def __init__(self, sb_list):
        self.subjects_list = sb_list
      #self.subjects_list = subjects_list
#    def generate_random_subject_list(self):
#       SUBJECTS_PLACE_NEED_DICT.keys()
 #       pass
    def set_subjects_list(self, subjects):
        self.subjects_list = subjects
    def get_subjects_list(self):
        return self.subjects_list

class Notebooks:
    def __init__(self,N):#, notebooks_amount):
        self.nb_amount = N
        self.nb_list = []
        #pass#self.notebooks_amount = notebooks_amount
        #self.generate_N_notebooks(self.notebooks_amount)

    def generate_random_notebooks(self,whole_subjects_list):
#        whole_subjects_list = whole_sb_list.copy()
        for nb_index in range(self.nb_amount-1):
            nb_sb_amount = randint(0, len(whole_subjects_list))

            new_sb_list = []
            for sb_index in range(nb_sb_amount):
                sb_to_add_index = randint(0,len(whole_subjects_list)-1)
                new_sb_list.append(whole_subjects_list[sb_to_add_index])
                print(nb_index,sb_to_add_index, nb_sb_amount)
                del whole_subjects_list[sb_to_add_index]
            new_nb = Notebook(new_sb_list)
            self.nb_list.append(new_nb)
        self.nb_list.append(Notebook(whole_subjects_list))

       # while len(whole_subjects_list)!=0:
       #     notebook_index = randint(0,len(whole_subjects_list))

        #new_notebook = Notebook(subjects_list)

    def generate_N_notebooks(self, N):
        pass
#print(__name__)
if __name__ == '__main__':
    nbs = Notebooks(3)
    nbs.generate_random_notebooks(list(SUBJECTS_PLACE_NEED_DICT.keys()))
    print(nbs.nb_list[0].get_subjects_list())
    print(nbs.nb_list[1].get_subjects_list())
    print(nbs.nb_list[2].get_subjects_list())
#    print(nbs[2])