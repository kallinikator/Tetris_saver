# -*- coding: utf-8 -*-
"""
@author: Till Langbein
"""

import shutil
import os

def prepare(Path, Stores): # TODO Add reorder flag, more folders
    """ 
    Ensures that all date are provided and in the right format and 
    it is possible to copy them
    """
    # Create the Paths of all Files contained
    to_store = sum((list(map(lambda y: os.path.join(x[0], y), x[2])) 
            for x in os.walk(Path)),[])
    # Get the size of all files and order them by their size
    to_store = sorted(((os.path.getsize(x),x) for x in to_store))
    # Get the size of all stores and order them
    store_sizes = sorted([shutil.disk_usage(x)[2],x] for x in Stores)
    store_sizes.insert(0,(0, ""))
    # Be shure the files are smaller then the store
    assert (sum(x[0] for x in to_store) < sum(x[0] for x in store_sizes)) and \
            (to_store[-1][0] < store_sizes[-1][0])    
    # TODO BTW: this is logically wrong.
    return to_store, store_sizes

    
def order(to_store, store_sizes):
    """ 
    Tries to fill all files to stores recursively 
    """
    sum_to_store = sum(x[0] for x in to_store)
    # The recursion
    # If it is too big for one store, fill this store and then the next
    if sum_to_store > store_sizes[-1][0]:
        to_store = fill(to_store, store_sizes.pop())
        order(to_store, store_sizes)
    # If it fits in one, and is bigger then the next: fill the bigger
    elif store_sizes[-1][0] > sum_to_store > store_sizes[-2][0]:
        to_store = fill(to_store, store_sizes.pop())
    # and if is smaller the the first both: go to the next smaller
    else:
        store_sizes.pop()
        order(to_store, store_sizes)
    print("ready")


def fill(to_store, store):
    """ 
    While there is something to store, pops the first and tries to add it to 
    the store. If it is not possible, it will be stored and returned in rest
    """
    rest = []
    while to_store:
        file = to_store.pop()
        # If the file fits in the store, it is copied 
        if file[0] <= store[0]:
            shutil.copyfile(file[1], store[1]+"/"+file[1].split("\\")[-1])
            # the size of the store is reduced by the size of the file
            store[0] -= file[0]
        # else we try the next smaller
        else:
            rest.append(file)
    return rest
            

if __name__ == "__main__":
    PATH = "C:/Users/Piotr/Desktop/testpics"
    STORES = ["D://", "C://Users/Piotr/Desktop"]

    to_store, store_sizes = prepare(PATH, STORES)
    order(to_store, store_sizes)
    
    
    
    
    
    