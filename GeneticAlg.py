from Notebooks import Notebooks
from random import randint

NOTEBOOKS_IN_INDIVID_AMOUNT = 3

GENS_AMOUNT = 100
INDIVID_IN_GEN_AMOUNT = 4000

LARGE_FINE = 1000
SMALL_FINE = 10
LIMIT_FOR_NBS_IN_DAY = 4#Включая физру(множитель 2)
LIMIT_FOR_SBS_IN_NB = 3 #суммарно три занятия мб. 1 - сем, 1 - лек
params = [LARGE_FINE,SMALL_FINE, LIMIT_FOR_NBS_IN_DAY,LIMIT_FOR_SBS_IN_NB]
#MUTATE_CHANCE = 0.5  # Т.к в угоду скорости выполнения программы, метод mutate сам по себе уменьшает шанс мутации

#CROSSING_CHANCE = 0.1


SCHEDULE = {"пн2": ["Физра","Методы вычислений", "Физика", "Методы вычислений"],
            "вт2": ["Физра","Электротехника", "Теория вероятностей и математическая статистика", "Иностранный язык"],
            "ср2": ["Модели динамических объектов","Модели динамических объектов", "Теория вероятностей и математическая статистика","Теория вероятностей и математическая статистика"],
            "пт2": ["Физра","Физика", "Электротехника"],
            "пн1": ["Физра","Методы вычислений", "Физика", "Методы вычислений"],
            "вт1": ["Физра","Электротехника", "Электротехника", "Иностранный язык"],
            "ср1": ["Модели динамических объектов","Модели динамических объектов", "Теория вероятностей и математическая статистика","Теория вероятностей и математическая статистика"],
            "пт1": ["Физра","Физика","Физика"],
            }

SUBJECTS_PLACE_NEED_DICT = {"Физра":0,"Электротехника": 2, "Физика": 2, "Модели динамических объектов": 2, "Иностранный язык": 1,
                            "Методы вычислений": 2, "Теория вероятностей и математическая статистика":2}
IGNORE_TO_NOTEBOOKS = ["Физра"]
SUBJECTS_LIST = list(SUBJECTS_PLACE_NEED_DICT.keys())
SUBJECTS_AMOUNT = len(SUBJECTS_LIST)


class GeneticAlgorithm:
    def __init__(self):
        pass

    def generate_ind(self):
        self.ind_list = [Notebooks(NOTEBOOKS_IN_INDIVID_AMOUNT, SCHEDULE,IGNORE_TO_NOTEBOOKS,params=params) for _ in
                         range(INDIVID_IN_GEN_AMOUNT)]

    def cross_by_index(self, ind1_index, ind2_index):
        ind1 = self.ind_list[ind1_index]
        ind2 = self.ind_list[ind2_index]
        sb_index = randint(0, SUBJECTS_AMOUNT - 1)
        sb_to_cross_by = SUBJECTS_LIST[sb_index]
        # print(sb_to_cross_by)
        sb_ind1_index = ind1.find(sb_to_cross_by)[0]  # Это номер ноутбука в первом индивиде
        sb_ind2_index = ind2.find(sb_to_cross_by)[0]
        #print(sb_to_cross_by)
        # DELETING

        new_ind1_nb_list = ind1.nb_list[sb_ind1_index].get_subjects_list()
        #print(new_ind1_nb_list)
        new_ind1_nb_list.remove(sb_to_cross_by)
        #print(new_ind1_nb_list)
        ind1.nb_list[sb_ind1_index].set_subjects_list(new_ind1_nb_list)

        new_ind2_nb_list = ind2.nb_list[sb_ind2_index].get_subjects_list()
        #print(new_ind2_nb_list)
        new_ind2_nb_list.remove(sb_to_cross_by)
        #print(new_ind2_nb_list)
        ind2.nb_list[sb_ind2_index].set_subjects_list(new_ind2_nb_list)

        # CHANGING
        new_ind1_nb_list = ind1.nb_list[sb_ind2_index].get_subjects_list()
        new_ind1_nb_list.append(sb_to_cross_by)
        ind1.nb_list[sb_ind2_index].set_subjects_list(new_ind1_nb_list)

        new_ind2_nb_list = ind2.nb_list[sb_ind1_index].get_subjects_list()
        new_ind2_nb_list.append(sb_to_cross_by)
        ind2.nb_list[sb_ind1_index].set_subjects_list(new_ind2_nb_list)

        #print(ind1.nb_list[sb_ind1_index].get_subjects_list(),"-", ind1.nb_list[sb_ind2_index].get_subjects_list())

       # print(ind2.nb_list[sb_ind2_index].get_subjects_list(),"-", ind2.nb_list[sb_ind1_index].get_subjects_list())
        # SAVING
        self.ind_list[ind1_index] = ind1
        self.ind_list[ind2_index] = ind2

    def cross(self):
        ind1_index = randint(0, INDIVID_IN_GEN_AMOUNT - 1)
        ind2_index = randint(0, INDIVID_IN_GEN_AMOUNT - 1)
        if ind1_index != ind2_index:
            self.cross_by_index(ind1_index, ind2_index)
        else:
            self.cross()

    def mutate(self):
        ind_index = randint(0, INDIVID_IN_GEN_AMOUNT - 1)
        self.ind_list[ind_index].mutate()
    def create_new_generarion(self):#Из 5 случайных выбирать 1ого лучшего и добавлять его копию(чтобы одна и та же ссылка не передавалась). Возвращать итоговый список.
        pass
    def calc_scores(self):
        self.ind_list = [ind.update_score(SUBJECTS_PLACE_NEED_DICT) for ind in self.ind_list]
#        self.ind_list[0].get_score(SUBJECTS_PLACE_NEED_DICT)
    def get_best(self):
        best_score = self.ind_list[0].score
        best_ind = self.ind_list[0]
        for ind in self.ind_list:
            if ind.score>best_score:
                best_score = ind.score
                best_ind = ind
        return best_ind
    def to_next_gen(self):#После отбора сделать кроссинговер и мутацию
        pass
    def gens_proccesing(self):
        for gen_index in GENS_AMOUNT:
            self.to_next_gen()


if __name__ == '__main__':
    ga = GeneticAlgorithm()
    ga.generate_ind()
    #ga.cross()
    ga.calc_scores()
    best = ga.get_best()
    print(best)
    print(best.score)
 #   print(best.)
#    # print("wtf")
