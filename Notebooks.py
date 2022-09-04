from random import randint


class Notebook:
    def __init__(self, sb_list):
        self.subjects_list = sb_list

    def set_subjects_list(self, subjects):
        self.subjects_list = subjects

    def get_subjects_list(self):
        return self.subjects_list


class Notebooks:
    def __init__(self, N, schedule,IGNORE_TO_NOTEBOOKS,params):
        self.params = params# , notebooks_amount):
        self.nb_amount = N
        self.schedule = schedule
        self.IGNORE_TO_NOTEBOOKS = IGNORE_TO_NOTEBOOKS

        #Schedule to list proccesing..
        a = [i for i in schedule.values()]
        b = []
        for i in a:
            b += i

        self.whole_subjects_list = list(set(b))#whole_subjects_list
        self.nb_list = []
        self.generate_random_notebooks()
#        self.score = self.get_score()

    def update_score(self,SUBJECTS_PLACE_NEED_DICT):
        self.score = self.get_score(SUBJECTS_PLACE_NEED_DICT, params=self.params)#[LARGE_FINE,SMALL_FINE, LIMIT_FOR_NBS_IN_DAY,LIMIT_FOR_SBS_IN_NB])
        return self
    def find(self, subject_name):
        #        print(len(self.nb_list))
        for i in range(len(self.nb_list)):
            #           print(len(i.get_subjects_list()))
            for j in range(len(self.nb_list[i].get_subjects_list())):
                #              print(j)
                if self.nb_list[i].get_subjects_list()[j] == subject_name:
                    return i, j

    def generate_random_notebooks(self, limit=2):
        whole_subjects_list = self.whole_subjects_list.copy()
        for nb_index in range(self.nb_amount - 1):
            nb_sb_amount = randint(0, len(whole_subjects_list))

            new_sb_list = []
            sb_counter = 0
            for sb_index in range(nb_sb_amount):
                sb_counter += 1
                sb_to_add_index = randint(0, len(whole_subjects_list) - 1)
                if whole_subjects_list[sb_to_add_index] not in self.IGNORE_TO_NOTEBOOKS:
                    new_sb_list.append(whole_subjects_list[sb_to_add_index])
                    del whole_subjects_list[sb_to_add_index]
                #if sb_counter == 2:
                 #   break
            new_nb = Notebook(new_sb_list)
            self.nb_list.append(new_nb)
        new_nb = []
        for i in whole_subjects_list:
            if i not in self.IGNORE_TO_NOTEBOOKS:
                new_nb.append(i)
#                print(i)
        if new_nb!= [] : self.nb_list.append(Notebook(new_nb))

    def mutate(self):
        rnd_nb_index = randint(0, len(self.nb_list) - 1)
        try:
            rnd_sb_index = randint(0, len(self.nb_list[rnd_nb_index].get_subjects_list()) - 1)
            rnd_sb = self.nb_list[rnd_nb_index].get_subjects_list()[rnd_sb_index]
            new_sb_list = self.nb_list[rnd_nb_index].get_subjects_list()
            del new_sb_list[rnd_sb_index]
            self.nb_list[rnd_nb_index].set_subjects_list(new_sb_list)
        except ValueError:
            return
        print(rnd_sb)

        new_rnd_nb_index = randint(0, len(self.nb_list) - 1)
        new_sb_list = self.nb_list[new_rnd_nb_index].get_subjects_list()
        self.nb_list[new_rnd_nb_index].set_subjects_list(new_sb_list + [rnd_sb])
    def get_score(self,SUBJECTS_PLACE_NEED_DICT, params):
        LARGE_FINE = params[0]#10000
        SMALL_FINE = params[1]#10
        LIMIT_FOR_NBS_IN_DAY = params[2]#5#Включая физру(множитель 2)
        LIMIT_FOR_SBS_IN_NB = params[3]#3 #суммарно три занятия мб. 1 - сем, 1 - лек
        score = 1000 #Чем больше скор, тем лучше

        #Weight FINE
        self.info = ""

        for day in self.schedule.keys():
            ignore_to_nb_counter = 0
            nbs_for_day = []
            for sb_in_day in self.schedule[day]:

                if sb_in_day in self.IGNORE_TO_NOTEBOOKS:# "Физра":
                     ignore_to_nb_counter+=1#print("wtf1",nbs_for_day)
                else:
                   nbs_for_day.append(self.find(sb_in_day)[0])
            #print(ignore_to_nb_counter,2)
            nbs_for_day = list(set(nbs_for_day))
            if len(nbs_for_day) + ignore_to_nb_counter*2>LIMIT_FOR_NBS_IN_DAY:#Если за день берется больше 3ех тетрадей . Тетрадь - коэф 1, физра - коэф2
                self.info += f"{nbs_for_day.__str__()} {ignore_to_nb_counter} {LIMIT_FOR_NBS_IN_DAY} Если за день берется больше 3ех тетрадей . Тетрадь - коэф 1, физра - коэф2 \n"
                score-=LARGE_FINE#SMALL_FINE*(len(nbs_for_day) + ignore_to_nb_counter*2)
            else:
                if len(nbs_for_day)<=1:
                    score += LARGE_FINE
                score+=0#SMALL_FINE*(1/len(nbs_for_day))*10
        for nb in self.nb_list:     # Если в одной тетради больше двух предметов*
            nb_place_sb = 0
            for sb in nb.get_subjects_list():
                nb_place_sb+=SUBJECTS_PLACE_NEED_DICT[sb]
                if nb_place_sb>LIMIT_FOR_SBS_IN_NB:
                    score-=LARGE_FINE*(nb_place_sb)
                    self.info += f'{nb_place_sb} Если в одной тетради больше двух предметов \n'
                    #print(nb.get_subjects_list())
        #print(score)
        return score
    def __str__(self):
        str = ""
        iter = 0
        for nb in self.nb_list:     # Если в одной тетради больше двух предметов*
            iter+=1
            nb_place_sb = 0
            str += f'Notebook{iter} - { nb.get_subjects_list()} \n'
        str+='\n'
        for day in self.schedule.keys():
            str+=day+": "
            ignore_to_nb_counter = 0
            nb_counter = 0
            nbs_for_day = []
            for sb_in_day in self.schedule[day]:

                if sb_in_day in self.IGNORE_TO_NOTEBOOKS:# "Физра":
                    str += ' Физра,'
                else:
                   if self.find(sb_in_day)[0] +1 not in nbs_for_day:
                        nbs_for_day.append(self.find(sb_in_day)[0] +1)

                        nb_counter += 1
                        str+= f' nb{self.find(sb_in_day)[0] +1}, '
            str+=f'Итого тетрадей {nb_counter} \n'
#            str+=nbs_for_day#print(ignore_to_nb_counter,2)
 #           if ignore_to_nb_counter>0:str += ' Физра'
        return str+'\n'+self.info
if __name__ == '__main__':
    SUBJECTS_PLACE_NEED_DICT = {"Электротехника": 2, "Физика": 2, "Модели динамических объектов": 2,
                                "Иностранный язык": 1, "Методы вычислений": 2}

    nbs = Notebooks(3, list(SUBJECTS_PLACE_NEED_DICT.keys()))
    nbs.generate_random_notebooks()
    print(nbs.nb_list[0].get_subjects_list())
    print(nbs.nb_list[1].get_subjects_list())
    print(nbs.nb_list[2].get_subjects_list())
    print("MUTATE")
    nbs.mutate()
    print("END OF MUTATE")
    print(nbs.nb_list[0].get_subjects_list())
    print(nbs.nb_list[1].get_subjects_list())
    print(nbs.nb_list[2].get_subjects_list())
    # print(nbs.whole_subjects_list)
