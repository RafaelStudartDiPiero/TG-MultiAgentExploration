
# Auxiliary function to concatenate to add only new elements to array
def concatenate_new_elements(main_list, vector):
        for e in vector:
            if e not in main_list:
                main_list.append(e)